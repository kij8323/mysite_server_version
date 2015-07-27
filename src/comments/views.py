#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404

# Create your views here.

from videos.models import Video

from .models import Comment
from .forms import CommentForm
from notifications.signals import notify

#http://127.0.0.1:8000/comment/1
#显示该评论的所有子评论
def comment_thread(request, id):
	comment = get_object_or_404(Comment, id=id)
	form = CommentForm()
	context = {
	"form": form,
	"comment": comment,
	}
	return render(request, "comments/comment_thread.html", context)


@login_required
def comment_create_view(request):
	#如果能接受到POST消息，并且是注册用户
	if request.method == "POST" and request.user.is_authenticated():
		#某子评论的父评论的id
		parent_id = request.POST.get('parent_id')
		#评论视频id
		video_id = request.POST.get("video_id")
		#被评论视频的地址
		origin_path = request.POST.get("origin_path")
		#获得被评论视频
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

			if parent_comment is not None and parent_comment.video is not None:
				video = parent_comment.video


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
				#发送消息说明生成一个新的评论
				notify.send(
						request.user, 
						action=new_comment, 
						target=parent_comment, 
						recipient=parent_comment.user, 
						affected_users = affected_users,
						verb=u'回复了')
				messages.success(request, "感谢您的回复.", extra_tags='safe')
				#返回父评论的主页
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			#如果该评论是父评论
			else:
				#生成新的评论实例
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=origin_path, 
					text=comment_text,
					video = video
					)
				messages.success(request, "Thank you for the comment.")
				#返回评论的主页
				return HttpResponseRedirect(new_comment.get_absolute_url())
		#如果表格填写错误，则停留在本页
		else:
			messages.error(request, "您填写的内容有问题.")
			return HttpResponseRedirect(parent_comment.get_absolute_url())
			

	else:
		raise Http404