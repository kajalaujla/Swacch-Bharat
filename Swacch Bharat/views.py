# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from datetime import datetime
from forms import *
from django.contrib.auth.hashers import *
from .models import *
from imgurpython import ImgurClient
from myproject.settings import BASE_DIR
from django.contrib.auth import logout
from email.mime.text import MIMEText
import smtplib



# create all controllers
def sign_up(request):

    '''
    1.create controller for signup pass request as parameter
    2.render sign_up.html for get request from user
    3.check validations for Post request of form a user
    4.save user to dbase
    5.if user is valid redirect to success page
    :param request:
    :return:
    '''
    today = datetime.now()

    if request.method=="POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            if len(username)<4:
                print "too short"
                return redirect('/signup')
            name = signup_form.cleaned_data['name']
            if len(name)<4:
                return redirect('/signup')
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            if len(password)<5:
                print "password too short"
                return redirect('/signup')
            user = UserModel(name = name , password = make_password(password) , email = email , username = username)
            user.save()
            content = 'Hey there !   ** welcome to swacch bharat WebApp **'
            mail = smtplib.SMTP('smtp.gmail.com',587)
            mail.ehlo()
            mail.starttls()
            mail.login('rajatbangar786@gmail.com','rajat@786')
            mail.sendmail('rajatbangar786@gmail.com',email,content)
            mail.close()
            return redirect('/success')
    elif request.method == 'GET':
        signup_form = SignUpForm()
        return render(request , 'sign_up.html',{'signup_form':SignUpForm})

def login_view(request):

    '''
    1.create controller for loginview and pass request
    2.render login_view.html for get request
    3.check validity of login form
    4.if form is valid save user and create a sesion token
    5.and redirect to post url as response
    :param request:
    :return:
    '''
    if request.method=="GET":
        form = LoginForm()
        return render(request , 'login_view.html',{'form':form})
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserModel.objects.filter(username = username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                    print "User is valid"

            else:
                print 'Invalid User'
                response = redirect('/signup')
                return response



def check_validation(request):
    '''
    1.create controller for validity of user from COOKIES
    2.if user is available in session return user
    :param request:
    :return:
    '''
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token = request.COOKIES.get('session_token')).first()
        if session:
            return session.user
        else:
            return None

def post_view(request):

    '''
    1.create controller for postview
    2.check for valid user
    3.if invalid user redirect to login page
    4.if valid user redirect to post_view.html for get request
    5.for post request take inputs and save to dbase
    6.create url for image with ImgurClient
    7.save image url to dbase
    8.redirect to feed
    :param request:
    :return:
    '''
    user = check_validation(request)
    if user:
        if request.method == "GET":
            form = PostForm()
            return render(request , 'post_view.html',{'form':form})
        elif request.method == "POST":
            form = PostForm(request.POST , request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user = user , image = image ,caption = caption)
                post.save()
                path = str(BASE_DIR +"\\"+ post.image.url)
                client = ImgurClient("e4e6a033caced69","a6e35cb737899081fc506ee554f73153918996c2")
                post.image_url = client.upload_from_path(path , anon=True)['link']
                post.save()
                return redirect('/feed')


    else:
        return redirect('/login')



def feed(request):
    '''
    1.create controller for feed
    2.check for valid user
    3.redirect to login invalid users
    4.for valid users show post according to created_on time
    5.logut for logout request
    6.return invalid users to login
    :param request:
    :return:
    '''
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        log_out = logout_view(request)
        return render(request , 'feed.html',{'posts':posts,'log_out':log_out})
    else:
        return redirect('/login')


def like_view(request):
    '''
    1.create controller for like
    2.check for valid
    3.redirect to login invalid users
    4.check if user already liked post
    5.if liked then delete like
    6.else like post
    7.redirect to feed
    :param request:
    :return:
    '''
    user = check_validation(request)
    if user and request.method == "POST":
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get("post").id
            existing_like = LikeModel.objects.filter(post_id=post_id , user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id = post_id , user = user)
                umail = user.email
                print umail
                content = ' hey! ** you just successfully liked a post **'
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('rajatbangar786@gmail.com', 'rajat@786')
                mail.sendmail('rajatbangar786@gmail.com', umail, content)
                mail.close()

            else:
                existing_like.delete()
            return redirect('/feed')
    else:
        return redirect('/login')

def comment_view(request):

    '''
    1.create controller function for comment on post
    2.check for valid user
    3.redirect to login invalid users
    4.for post request check for valid form
    5.save comment to dbase
    6.redirect to feed
    :param request:
    :return:
    '''
    user = check_validation(request)
    if user and request.method == 'POST':
        form= CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user = user , post_id = post_id , comment_text = comment_text)
            comment.save()
            umail = user.email
            content = '    hey! ** you just successfully commented on a post **'
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login('rajatbangar786@gmail.com', 'rajat@786')
            mail.sendmail('rajatbangar786@gmail.com', umail , content)
            mail.close()
            return redirect('/feed')
        else:
            return redirect('/feed')
    else:
        return redirect('/login')

def logout_view(request):
    '''
    1.write controller to logout user
    :param request:
    :return:
    '''
    logout(request)
    return redirect('/login')
def success(request):
    if request.method=='GET':
        return render(request,'success.html')

