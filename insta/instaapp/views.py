from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User
from instaapp.models import Post,Profile,Likes,Follow,Comment
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime,timezone
from django.core.mail import get_connection,EmailMessage
from django.conf import settings
import random,razorpay


# Create your views here.
def index(request):
    
    return render(request,'index.html')

def register(request):
    if request.method == 'GET': 
        return render(request,'register.html')
    else:
        username = request.POST['username']
        request.session['username']= username
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            u = User.objects.create(username=username,first_name=first_name,last_name=last_name,email=email)
            u.set_password(password)
            u.save()
            return redirect('/profile')
        else:
            context = {}
            context['error']= 'password and confirm password are not match'
            return redirect('/register')
        
        
        
        9
   
def u_login(request):
    if request.method == 'GET':
     return render(request,'login.html')
 
    else:
        
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(username=username,password=password)
         if user is not None:
             login(request,user)
             return redirect('/')
         else:
             context = {}
             context['error'] = 'username and password incorrect'
             return render(request,'login.html',context)
@login_required(login_url="/login")        
def u_logout(request):
    logout(request)
    return redirect('/u_login')


def forgot_password(request):
    
    if request.method == "GET":
        
        return render(request, "forgot_password.html")
    
    else:
        
        email = request.POST['email']
        
        request.session['email'] = email
        
        user = User.objects.filter(email = email).exists()
        
        if user:
        
            otp = random.randint(1000, 9999)
            
            request.session['otp'] = otp
            
            with get_connection(
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                user_tls = settings.EMAIL_USE_TLS
            ) as connection :
                
                subject = "OTP Verification"
                email_from = settings.EMAIL_HOST_USER
                reciption_list = [email]
                message = f"OTP is {otp}"
                
                EmailMessage(subject, message, email_from, reciption_list, connection = connection).send()
            return redirect('/otp_verification')
        
        else:
            
            context = {}
            
            context['error'] = "User Not a Found"
            
            return render(request, 'forgot_password.html', context)
        
    
def otp_verification(request):
    
    if request.method == "GET":
        
        return render(request, 'otp.html')
    
    else:
        
        otp = int(request.POST['otp'])
        
        email_otp = int(request.session['otp'])
        
        if otp == email_otp:
            
            return redirect("/new_password")
        
        else:
            
            context = {}
            
            context['error'] = "OTP does not match"
            
            return render(request, 'forgot_password.html', context)
        
        
def new_password(request):
    
    if request.method == "GET":
        
        return render(request, 'new_password.html')
    
    else:
        
        email = request.session['email']
        
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        user = User.objects.get(email = email)
        
        if password == confirm_password:
            
            user.set_password(password)
            
            user.save()
            
            return redirect("/u_login")
        
        else:
            
            context ={}
            
            context['error'] = "Password and confirm Password does not match"
            
            return render(request, 'new_password.html', context)


def profile(request):
    if request.method == 'GET':
        return render(request,'create_profile.html')
    else:
        Username = request.session.get('username')
        user = User.objects.get(username = Username)
        if user:
            bio = request.POST['bio']
            profile_img = request.FILES['profile_img']
            birth_date = request.POST['birth_date']
           
            p = Profile.objects.create(bio=bio,profile_img=profile_img,birth_date=birth_date,user=user)
            p.save()
            return redirect('/u_login')
        else:
            return redirect('/register')

@login_required(login_url="/login")        
def read_profile(request):
    # Get the currently logged-in user
    user = request.user
    
    # Retrieve the user's profile or return a 404 if it doesn't exist
    profile = get_object_or_404(Profile, user=user)
    
    # Pass the profile to the template
    return render(request, 'read_profile.html', {'profile': profile})


    
    # user = User.objects.all()
    
    p = Profile.objects.all().exclude(user = request.user)
    
    context = {}
    
    context['data'] = p
    
    return render(request, 'show_users.html', context)


def show_detail_users(request, rid):
    
    p = Profile.objects.get(id = rid)
    profile = Profile.objects.filter(id = rid)
    
   
    # Get the currently logged-in user
    user = User.objects.get(username = request.user.username)
    
    
    follower = Follow.objects.filter(follower=p.user) #The result is stored in followers, representing all users who follow the profile's user.
    following = Follow.objects.filter(following=p.user) #The result is stored in following, representing all users that the profile's user is following.
    
    user_has_followed = Follow.objects.filter(follower=user, following=p.user).exists()
    
    print(user_has_followed)
    
    context = {
                        'data': profile,
                        'following': follower,
                        'followers': following,
                        'user_has_followed': user_has_followed
                        }
    
    
    # Pass the profile to the template
    
    return render(request, 'show_detail_users.html', context)

@login_required(login_url="/login") 
def follow_user(request,rid):
    user_follow = User.objects.get(username = request.user.username)
    profile = Profile.objects.get(id = rid)
    follow_relation = Follow.objects.filter(follower=user_follow, following = profile.user).first()
    
    
    if follow_relation is None:
        Follow.objects.create(following = profile.user, follower = user_follow)
        profile.no_of_followers += 1
        profile.save()
        
        
        
        user_profile = Profile.objects.get(user = user_follow)
        user_profile.no_of_following += 1
        user_profile.save()
    
    else:
        follow_relation.delete()
        
        profile.no_of_followers -= 1
        profile.save()
        
        user_profile = Profile.objects.get(user = user_follow)
        user_profile.no_of_following -= 1
        user_profile.save()
    
    
    return redirect('/show_users')
    
    


def create_post(request):
    
    if request.method == "GET":
        
        return render(request, 'create_post.html')
    
    else:
        
        user = request.user
        image = request.FILES['image']
        caption = request.POST['caption']
        
        
        if image:
            
            p = Post.objects.create(user = user, caption = caption, image = image)
            
            p.save()
            return redirect('/read_post')
        
        else:
            
            context = {}
            
            context["error"] = "Image is reqired to create post"
            
            return render(request, 'create_post.html', context)

def read_post(request):
        p = Post.objects.filter(user = request.user)
        context = {}
        context['data'] = p
        return render(request,'read_post.html',context)
    
    
def delete_post(request,rid):
    p = Post.objects.filter(id = rid)
    p.delete()
    return redirect('/read_post')

def update_post(request,rid):
    if request.method == 'GET':
        p = Post.objects.filter(id = rid)
        context = {}
        context['data'] = p
        return render(request,'update_post.html',context)
    else:
        caption = request.POST['caption']
        p = Post.objects.filter(id = rid)
        p.update(caption = caption, updated_at = datetime.now())
        return redirect('/read_post')
    
    
def read_post_detail(request, rid):
    
    log = Post.objects.filter(id = rid)  #use for to send in html
    c = Post.objects.get(id = rid)
    p = Profile.objects.filter(id = rid)
    c = Comment.objects.filter(post_id = c).order_by('-created_at')
    context = {}
    
    context['data'] = log
    context['profile'] = p
    context['comment'] = c 
    if request.method == 'GET':
        

        return render(request, 'read_post_detail.html', context)
    else:
        comments = request.POST['comments']
        post = Post.objects.get(id = rid)
        c= Comment.objects.create(post_id = post,user = request.user,comments = comments)
        c.save()
        return render(request,'read_post_detail.html',context)



def likes_count(request, post_id):
    username = User.objects.get(username =request.user.username)
    post = Post.objects.get(id = post_id)
    
    
    
    like_filter = Likes.objects.filter(post_id=post, username=username).first()
    
    if like_filter is None:
        new_like = Likes.objects.create(post_id=post, username=request.user)
        post.no_of_likes += 1
        new_like.save()
        
    else:
        like_filter.delete()
        post.no_of_likes -= 1
    
    post.save()
    return redirect('/read_post')   


 



        
      

    
        

