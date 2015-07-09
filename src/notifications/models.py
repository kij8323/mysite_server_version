#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from .signals import notify
# Create your models here.

class NotificationQuerySet(models.query.QuerySet):
	#返回属于recipient的消息
	def get_user(self, recipient):
		return self.filter(recipient=recipient)

	def mark_targetless(self, recipient):
		qs = self.unread().get_user(recipient)
		qs_no_target = qs.filter(target_object_id=None)
		if qs_no_target:
			qs_no_target.update(read=True)

	#将所有属于recipient的消息更新成已读
	def mark_all_read(self, recipient):
		qs = self.unread().get_user(recipient)
		qs.update(read=True)

	#将所有属于recipient的消息更新成未读
	def mark_all_unread(self, recipient):
		qs = self.read().get_user(recipient)
		qs.update(read=False)
	#返回未读的消息
	def unread(self):
		return self.filter(read=False)
	#返回已读的消息
	def read(self):
		return self.filter(read=True)
	#返回最近的5个未读消息
	def recent(self):
		return self.unread()[:5]

class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def all_unread(self, user):
		return self.get_queryset().get_user(user).unread()

	def all_read(self, user):
		return self.get_queryset().get_user(user).read()

	#返回所有属于user的消息,并按生成的时间反排序，即后生成的在数组前面
	def all_for_user(self, user):
		self.get_queryset().mark_targetless(user)
		return self.get_queryset().get_user(user).order_by('-timestamp')


class Notification(models.Model):
	#发送消息的对象
	sender_content_type = models.ForeignKey(ContentType, related_name='nofity_sender')
	sender_object_id = models.PositiveIntegerField()
	sender_object = GenericForeignKey("sender_content_type", "sender_object_id")
	
	verb = models.CharField(max_length=255)
	#执行动作的对象
	action_content_type = models.ForeignKey(ContentType, related_name='notify_action', 
		null=True, blank=True)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_object = GenericForeignKey("action_content_type", "action_object_id")

	#目标对象
	target_content_type = models.ForeignKey(ContentType, related_name='notify_target', 
		null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = GenericForeignKey("target_content_type", "target_object_id")
	#用户
	recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
	#是否已读
	read = models.BooleanField(default=False)
	#消息发送时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	# reply_content_type = models.ForeignKey(ContentType, related_name='reply_object', 
	# 	null=True, blank=True)
	# reply_object_id = models.PositiveIntegerField(null=True, blank=True)
	# reply_object = GenericForeignKey("reply_content_type", "reply_object_id")


	objects = NotificationManager()


	def __unicode__(self):
		#是否有目标对象
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = None
		#内容
		context = {
			#"sender": self.sender_object,
			"verb": self.verb,
			"action": self.action_object,
			"target": u'请浏览',
			"verify_read": reverse("notifications_read", kwargs={"id": self.id}),
			"target_url": target_url,
			"word": u'您关心的留言'
		}

		if self.target_object:
			#如果目标对象地址与动作对象同时有，则返回读消息的地址
			#回复就是这一个**************************
			if self.action_object and target_url:
				return "%(verb)s%(word)s<a href='%(verify_read)s?next=%(target_url)s'>%(target)s</a> " %context
			#如果只有动作对象，没有目标对象，则返回时间信息
			if self.action_object and not target_url:
				return "%(sender)s %(verb)s %(target)s with %(action)s" %context
			#其他情况返回发送对象
			return "%(sender)s %(verb)s %(target)s" %context
		return "%(sender)s %(verb)s" %context

	@property	
	def get_link(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = reverse("notifications_all")
		
		context = {
			"sender": self.sender_object,
			"verb": self.verb,
			"action": self.action_object,
			"target": self.target_object,
			"verify_read": reverse("notifications_read", kwargs={"id": self.id}),
			"target_url": target_url,
		}
		if self.target_object:
			return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s %(target)s with %(action)s</a>" %context
		else:
			return "<a href='%(verify_read)s?next=%(target_url)s'>%(sender)s %(verb)s</a>" %context


#消息函数
def new_notification(sender, **kwargs):
	kwargs.pop('signal', None)
	#该评论的父评论的用户
	recipient = kwargs.pop("recipient")
	#动作'replied to'
	verb = kwargs.pop("verb")
	#print verb
	#获得所有同一父评论的所有子评论用户
	affected_users = kwargs.pop('affected_users', None)
	#如果该父评论有子评论
	if affected_users is not None:
		for u in affected_users:
			#如果affected_users中的某个用户==发表该子评论的用户则pass（该子评论正在浏览新的回复，所以不许要生成新的消息）
			if u == sender:
				pass
			#如果affected_users中的用户不是发表该子评论的用户则生成一个新的notification
			else:
				#生成新消息，该消息recipient==同属于一个父评论，但并非当下子评论的发表人；verb=='replied to' ； content_type=发表用户的类型（myuser）
				new_note = Notification(
					recipient=u,
					verb = verb, # smart_text
					sender_content_type = ContentType.objects.get_for_model(sender),
					sender_object_id = sender.id,
					)
				##当optin="target"obj是父评论的实例，当optin="action"，obj是当下评论的子评论的实例
				for option in ("target", "action"):
					#obj = kwargs.pop(option, None)
					try:
						obj = kwargs[option]
						if obj is not None:
							# new_note.target_content_type=父评论的类型
							# new_note.target_object_id=父评论的id
							# new_note.action__content_type=当下评论的类型
							# new_note.action__object_id=当下评论的id
							setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
							setattr(new_note, "%s_object_id" %option, obj.id)
					except:
						pass
				#保存新生成的实例
				new_note.save()
				print new_note

	#如果父评论没有子评论，及发送的消息本身是一个父评论，这里不做讨论
	else:
		new_note = Notification(
			recipient=recipient,
			verb = verb, # smart_text
			sender_content_type = ContentType.objects.get_for_model(sender),
			sender_object_id = sender.id,
			)
		#print "111111111111111111111111111111111111"
		for option in ("target", "action"):
			obj = kwargs.pop(option, None)
			if obj is not None:
				setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
				setattr(new_note, "%s_object_id" %option, obj.id)
		new_note.save()



notify.connect(new_notification)

