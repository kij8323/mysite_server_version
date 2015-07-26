#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404
from .models import Video, Category, TaggedItem
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from analytics.signals import page_view
from notifications.signals import notify
#from notifications.signals import notify_reply

#视频具体页，地址http://127.0.0.1:8000/projects/guo-guang/slug-1/
def video_detail(request, cat_slug, vid_slug):
	#如果能接受到POST消息
	if request.method == "POST" :
		#并且是注册用户
		if request.user.is_authenticated():
			#某子评论的父评论的id
			parent_id = request.POST.get('parent_id')
			#评论视频id
			video_id = request.POST.get("video_id")
			#被评论视频的地址
			origin_path = request.POST.get("origin_path")

			reponse_id = request.POST.get("reponse_id")

			reponse = None
			if reponse_id is not None:
				try:
					reponse = Comment.objects.get(id=reponse_id).user
				except:
					reponse = None

			try:
				video = Video.objects.get(id=video_id)
			except:
				video = None
			#如果该评论有父评论，则获得评论的实例
			parent_comment = None
			if parent_id is not None:
				try:
					parent_comment = Comment.objects.get(id=parent_id)
				except:
					parent_comment = None

			form = CommentForm(request.POST)
			#如果评论表格有效则获得填写的内容
			if form.is_valid():
				comment_text = form.cleaned_data['comment']
				#如果该评论是子评论
				if parent_comment is not None:
					#生成新的评论实例
					new_comment = Comment.objects.create_comment(
						user=request.user, 
						path=parent_comment.get_origin, 
						text=comment_text,
						video = video,
						parent=parent_comment,
						reponse=reponse
						)

					#获得所有同一父评论的所有子评论用户以及该评论父评论的用户
					affected_users = parent_comment.get_affected_users()
					if parent_comment.user in affected_users:
						pass
					else:
						affected_users=affected_users.append(parent_comment.user)
					notify.send(
							request.user, 
							action=new_comment, 
							target=parent_comment, 
							recipient=parent_comment.user, 
							affected_users = affected_users,
							verb=u'回复了')
					messages.success(request, "感谢您的评论!")
					return HttpResponseRedirect(origin_path)

				#如果该评论是父评论
				else:
					#生成新的评论实例
					new_comment = Comment.objects.create_comment(
						user=request.user, 
						path=origin_path, 
						text=comment_text,
						video = video
						)
					messages.success(request, "感谢您的评论!")
					return HttpResponseRedirect(origin_path)
		#如果不是注册用户则提议登录
		else:
			messages.success(request, "登录就能与同学们一起讨论课程了！")
			return HttpResponseRedirect(origin_path)



	#从视频地址中的cat_slug解析视频所属的类
	cat = get_object_or_404(Category, slug=cat_slug)
	#从视频地址中的vid_slug解析视频具体地址
	obj = get_object_or_404(Video, slug=vid_slug, category=cat)
	#类别中的所有视频
	queryset = cat.video_set.all()
	#当进入视频页就会发送消息到analytics.signals.page_view，通知最近浏览视频
	page_view.send(request.user, 
			page_path=request.get_full_path(), 
			primary_obj=obj,
			secondary_obj=cat)
	#如果浏览用户是注册用户或者视频是免费的
	if request.user.is_authenticated() or obj.has_preview:
		#视频所有的父评论
		comments = obj.comment_set.all()
		#评论的子评论
		for c in comments:
			c.get_children()
		comment_form = CommentForm()
		context = {"obj": obj, 
			"queryset": queryset,
			"comments":comments, 
			"comment_form": comment_form}
		return render(request, "videos/video_detail.html", context)
	else:
		#如果登录后则重定向到之前需要登录浏览的视频
		next_url = obj.get_absolute_url()
		return HttpResponseRedirect("%s?next=%s"%(reverse('login'), next_url))


#http://127.0.0.1:8000/projects/
def category_list(request):
	#所有视频类别
	queryset = Category.objects.all()
	context = {
		"queryset": queryset,
	}
	return render(request, "videos/category_list.html", context)

#@login_required
def category_detail(request, cat_slug):
	#从视频地址中的cat_slug解析视要浏览的类
	obj = get_object_or_404(Category, slug=cat_slug)
	#类别中的所有视频
	queryset = obj.video_set.all()
	#当进入视频类别页就会发送消息到analytics.signals.page_view，通知最近浏览视频类别
	page_view.send(request.user, 
			page_path=request.get_full_path(), 
			primary_obj=obj)
	return render(request, "videos/video_list.html", {"obj": obj, "queryset": queryset})