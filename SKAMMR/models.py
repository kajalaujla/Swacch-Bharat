# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

class User(models.Model):
    '''
    1.create variables to save data in MySql
    2.make migrations
    '''
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)
    age = models.IntegerField(default=0)
    has_varified_mobile = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

class UserModel(models.Model):
    '''
    1.create variables to save data in MySql
    2.make migrations
    '''
    email = models.EmailField()
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
class SessionToken(models.Model):
    '''
    1.create variables to save data in MySql
    2.make user variable with ForeignKey from UserModel
    2.make migrations
    '''
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    def create_token(self):
        '''
        1.session token
        '''
        self.session_token = uuid.uuid4()

class PostModel(models.Model):
    '''
    1.create PostModel to save post
    2.save image to local dbase
    3.save image_url to dbase
    '''
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    @property
    def like_count(self):
        '''
        1. create function to count number of likes
        :return:
        '''
        return len(LikeModel.objects.filter(post = self))
    @property
    def comments(self):
        '''
        1.create comment and create list by order of created on
        :return:
        '''
        return CommentModel.objects.filter(post=self).order_by('created_on')

class LikeModel(models.Model):
    '''
    1.create LikeModel for Likes on post
    '''
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
    '''
    1.create Model for Comments on posts
    '''
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_in = models.DateTimeField(auto_now=True)
