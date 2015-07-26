#coding=utf-8
'''
主页函数
'''
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count

from accounts.forms import RegisterForm, LoginForm
from accounts.models import MyUser
from comments.models import Comment
from analytics.signals import page_view
from analytics.models import PageView
from videos.models import Video, Category


#http://127.0.0.1:8000/
def home(request):
	#向signal函数page_view发送本次事件的参数
	page_view.send(
		request.user,
		page_path=request.get_full_path()
		)
	#访问者是否是注册用户
	if request.user.is_authenticated():
		#用户最近浏览过的6个视频
		page_view_objs = request.user.pageview_set.get_videos()[:6]
		recent_videos = []
		#将最近浏览过的视频添加到列表recent_videos里
		for obj in page_view_objs:
			if not obj.primary_object in recent_videos:
				recent_videos.append(obj.primary_object)
		#最近的6个评论
		recent_comments = Comment.objects.recent()

		video_type = ContentType.objects.get_for_model(Video)
		#点击次数最多的4个视频
		popular_videos_list = PageView.objects.filter(primary_content_type=video_type)\
		 .values("primary_object_id")\
		 .annotate(the_count=Count("primary_object_id"))\
		 .order_by("-the_count")[:4]
		popular_videos = []
		for item in popular_videos_list:
			try:
				new_video = Video.objects.get(id=item['primary_object_id'])
				popular_videos.append(new_video)
			except:
				pass
		#随机的6个视频
		random_videos = Video.objects.all().order_by('?')[:6]

		context = {
			"random_videos": random_videos,
			"recent_videos": recent_videos,
			"recent_comments": recent_comments,
			"popular_videos": popular_videos,
			}
		template = "accounts/home_logged_in.html"
	else:
		#有代表性的视频类别
		featured_categories = Category.objects.get_featured()
		#有代表性的视频
		featured_videos = Video.objects.get_featured()
		login_form = LoginForm()
		#注册表
		register_form = RegisterForm()
		template = "accounts/home_visitor.html"
		queryset = Category.objects.all()

		context = {
				"register_form": register_form, 
				"login_form": login_form, 
				"featured_videos": featured_videos,
				"featured_categories": featured_categories,	
				"queryset": queryset,			
				}
	
	return render(request,template,context)







'''
@login_required(login_url='/staff/login/')
def staff_home(request):
	context = {
		
	}
	return render(request, "home.html", context)
'''

