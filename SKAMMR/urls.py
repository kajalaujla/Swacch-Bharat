from django.conf.urls import url
from django.contrib import admin
from .views import *


urlpatterns = [

    #list of all the urls for navigation

    url(r'login',login_view),
    url(r'signup',sign_up),
    url(r'feed',feed),
    url(r'post',post_view),
    url(r'like',like_view),
    url(r'comment',comment_view),
    url(r'log_out',logout_view),
    url(r'success',success),
]