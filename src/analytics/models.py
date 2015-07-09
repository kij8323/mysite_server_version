#coding=utf-8
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from videos.models import Video, Category

from .signals import page_view

class PageViewQuerySet(models.query.QuerySet):
	def videos(self):
		content_type = ContentType.objects.get_for_model(Video)
		return self.filter(primary_content_type=content_type)

	def categories(self):
		content_type = ContentType.objects.get_for_model(Category)
		return self.filter(primary_content_type=content_type)


class PageViewManager(models.Manager):
	def get_queryset(self):
		return PageViewQuerySet(self.model, using=self._db)
	#返回浏览过的所有视频
	def get_videos(self):
		return self.get_queryset().videos()
	#返回浏览过的所有类别
	def get_categories(self):
		return self.get_queryset().categories()

#浏览过的内容数据库
class PageView(models.Model):
	#浏览过的实例路径
	path = models.CharField(max_length=350)
	#用户
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	#主要浏览过的内容
	primary_content_type = models.ForeignKey(ContentType, related_name='primary_obj',\
											null=True, blank=True)
	primary_object_id = models.PositiveIntegerField(null=True, blank=True)
	primary_object = GenericForeignKey("primary_content_type", "primary_object_id")
	#第二浏览过的内容
	secondary_content_type = models.ForeignKey(ContentType, related_name='secondary_obj',\
								null=True, blank=True)
	secondary_object_id = models.PositiveIntegerField(null=True, blank=True)
	secondary_object = GenericForeignKey("secondary_content_type", "secondary_object_id")

	timestamp = models.DateTimeField(default=timezone.now())
	#自定义查询
	objects = PageViewManager()

	def __unicode__(self):
		return self.path

	class Meta:
		ordering = ['-timestamp']

def page_view_received(sender, **kwargs):
	kwargs.pop('signal', None)
	page_path = kwargs.pop('page_path')
	primary_obj = kwargs.pop('primary_obj', None)
	secondary_obj = kwargs.pop('secondary_obj', None)
	user = sender
	#如果用户不是注册用户则生成的浏览对象没有用户名，反之有用户名
	if not user.is_authenticated():
		new_page_view = PageView.objects.create(path=page_path, timestamp=timezone.now())
	else:
		new_page_view = PageView.objects.create(path=page_path, user=user, timestamp=timezone.now())
	#如果浏览的是视频类别那么生成的实例是类别实例
	if primary_obj:
		new_page_view.primary_object_id = primary_obj.id
		new_page_view.primary_content_type = ContentType.objects.get_for_model(primary_obj)
		new_page_view.save()
	#如果浏览的视频是视频，那么生成的实例是视频实例
	if secondary_obj:
		new_page_view.secondary_object_id = secondary_obj.id
		new_page_view.secondary_content_type = ContentType.objects.get_for_model(secondary_obj)
		new_page_view.save()



page_view.connect(page_view_received)