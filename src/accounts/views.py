#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from .forms import LoginForm, RegisterForm
from .models import MyUser

def auth_logout(request):
	logout(request)
	return HttpResponseRedirect('/')


#http://127.0.0.1:8000/login
def auth_login(request):
	form = LoginForm(request.POST or None)
	#重定向：由videos.view传来的next_url地址
	next_url = request.GET.get('next')
	print "I am next_url"
	print next_url
	#如果登录成功则回到主页
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		#验证输入的用户名和密码是否为注册用户
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if next_url is not None:
				return HttpResponseRedirect(next_url)
			return HttpResponseRedirect("/")
	#否则停留在本页
	action_url = reverse("login")
	title = "登录"
	submit_btn = title
	submit_btn_class = "btn-success btn-block"
	extra_form_link = None 
	Register_now = True
	#"Upgrade your account today <a href='%s'>here</a>!" %(reverse("account_upgrade"))
	context = {
		"form": form,
		"action_url": action_url,
		"title": title,
		"submit_btn": submit_btn,
		"submit_btn_class": submit_btn_class,
		"extra_form_link":extra_form_link,
		"Register_now": Register_now
		}
	return render(request, "accounts/account_login_register.html", context)
	
#http://127.0.0.1:8000/register
def auth_register(request):
	form = RegisterForm(request.POST or None)
	#如果注册成功则进入欢迎页
	if form.is_valid():
		human = True
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password2']
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password) #RIGHT
		new_user.save()
		print username, password
		template = "accounts/account_register_succeed.html"
		context = {}
		return render(request,template,context)
	#如果不成功则停留在本页
	action_url = reverse("register")
	title = "注册"
	submit_btn = "创建用户"
	context = {
		"form": form,
		"action_url": action_url,
		"title": title,
		"submit_btn": submit_btn
		}
	#return HttpResponseRedirect("/")
	return render(request, "accounts/account_login_register.html", context)

