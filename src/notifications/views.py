#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.shortcuts import render, Http404, HttpResponseRedirect,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Notification
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
@login_required
def all(request):
	#返回所有与已回复相关的消息
	notifications = Notification.objects.all_for_user(request.user).\
	filter(verb=u"回复了")
	paginator = Paginator(notifications, 10)
	page = request.GET.get('page')
	try:
		contacts = paginator.page(page)
	except PageNotAnInteger:
		contacts = paginator.page(1)
        # If page is not an integer, deliver first page.
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
		   # If page is out of range (e.g. 9999), deliver last page of results.

	count = notifications.count()
	context = {
		"notifications":contacts,
		"count":count,
	}
	return render(request, "notifications/all.html", context)


@login_required
def read(request, id):
	notification = get_object_or_404(Notification, id=id)
	try:
		next = request.GET.get('next', None)
		if notification.recipient == request.user:
			notification.read = True
			notification.save()
			if next is not None:
				return HttpResponseRedirect(next)
			else:
				return redirect("notifications_all")
		else:
			raise Http404
	except:
		raise redirect("notifications_all")



@login_required
# 收件箱ajax模块
def hello(request):
	#返回所有已回复并且未读的消息
	if request.is_ajax():
		notifications = Notification.objects.all_unread(request.user).\
		filter(verb=u"回复了")
		count = notifications.count()
		data = {
			"count": count,
		}
		json_data = json.dumps(data)
		print 'json_data'
		print json_data
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404