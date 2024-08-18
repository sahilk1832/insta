
from django.urls import path
from instaapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('u_login',views.u_login),
    path('u_logout',views.u_logout),
    path('forgot_password', views.forgot_password),
    path('otp_verification', views.otp_verification),
    path('new_password', views.new_password),
    path('likes_count/<post_id>', views.likes_count),
    path('profile',views.profile),
    path('read_profile',views.read_profile),
    path('show_users', views.show_users),
    path('show_detail_users/<rid>', views.show_detail_users),
    path('create_post',views.create_post),
    path('read_post',views.read_post),
    path('read_post_detail/<rid>',views.read_post_detail),
    path('delete_post/<rid>',views.delete_post),
    path('update_post/<rid>',views.update_post),
    path('follow_user/<rid>', views.follow_user),
   
   
]
urlpatterns  += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
