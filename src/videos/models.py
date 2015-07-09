#coding=utf-8
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from .utils import get_vid_for_direction
# Create your models here.

class VideoQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	#是否首页视频
	def featured(self):
		return self.filter(featured=True)

	#当前视频是否有链接地址
	def has_embed(self):
		return self.filter(embed_code__isnull=False).exclude(embed_code__exact="")


class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQuerySet(self.model, using=self._db)

	#是否首页视频+视频是否激活
	def get_featured(self):
		return self.get_queryset().active().featured()

	#当前视频是否有链接地址+视频是否激活
	def all(self):
		return self.get_queryset().active().has_embed()
	

DEFAULT_MESSAGE = "Check out this awesome video."

#video数据库
class Video(models.Model):
	#视频名称
	title = models.CharField(max_length=120)
	#视频链接
	embed_code = models.CharField(max_length=500, null=True, blank=True)
	#视频是否激活
	active = models.BooleanField(default=True)
	#视频顺序
	order = models.PositiveIntegerField(default=1)
	#是否首页视频
	featured = models.BooleanField(default=False)
	#视频是否免费
	free_preview = models.BooleanField(default=False)
	share_message = models.TextField(default=DEFAULT_MESSAGE)
	#视频上传时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
	#视频更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
	#视频属于什么类别
	category = models.ForeignKey("Category", default=1)
	#视频slug
	slug = models.SlugField(null=True, blank=True)
	#视频标签
	tags = GenericRelation("TaggedItem", null=True, blank=True)
	#自定义查询语句
	objects = VideoManager()
	
	class Meta:
		unique_together = ('slug', 'category')
		ordering = ['order', 'timestamp']
		
	def __unicode__(self):
		return self.title

	#返回当前视频的地址，返回的格式方便tamplate使用
	def get_absolute_url(self):
		return reverse("video_detial", kwargs={"vid_slug": self.slug, "cat_slug": self.category.slug})

	#返回当前视频的后一个视频的url地址
	def get_next_url(self):
		video = get_vid_for_direction(self, "next")
		if video is not None:
			return video.get_absolute_url()
		return None

	#返回当前视频的前一个视频的url地址
	def get_previous_url(self):
		video = get_vid_for_direction(self, "previous")
		if video is not None:
			return video.get_absolute_url()
		return None

	#当前视频是否免费
	@property 
	def has_preview(self):
		if self.free_preview:
			return True
		return False


#每当一个视频实例生成，就为该视频生成一个新的slug
def video_post_save_receiver(sender, instance, created, *args, **kwargs):
	print "signal sent"
	if created:
		#将该视频名称转化成slug格式
		slug_title = slugify(instance.title)
		#将视频名称，视频所属分类的slug，视频id组合成视频的新slug
		new_slug = "%s %s %s" %(instance.title, instance.category.slug, instance.id)
		try:
			#如果slug已经有其他视频占用，则为新生成的视频生成新的slug
			obj_exists = Video.objects.get(slug=slug_title, category=instance.category)
			instance.slug = slugify(new_slug)
			instance.save()
			print "model exists, new slug generated"
		except Video.DoesNotExist:
			#如果slug没有被占用，则用视频名称为当前视频的slug
			instance.slug = slug_title
			instance.save()
			print "slug and model created"
		except Video.MultipleObjectsReturned:
			#如果有多个视频占用了名称slug，则为新生成的视频生成新的slug
			instance.slug = slugify(new_slug)
			instance.save()
			print "multiple models exists, new slug generated"
		except:
			pass
	
post_save.connect(video_post_save_receiver, sender=Video)



class CategoryQuerySet(models.query.QuerySet):
	#类别是否被激活
	def active(self):
		return self.filter(active=True)
	#类别是否是首页
	def featured(self):
		return self.filter(featured=True)


class CategoryManager(models.Manager):
	def get_queryset(self):
		return CategoryQuerySet(self.model, using=self._db)

	#激活+首页
	def get_featured(self):
		#Video.objects.get_featured(user, kabc="something")
		#Video.objects.filter(featured=True)
		#return super(VideoManager, self).filter(featured=True)
		return self.get_queryset().active().featured()

	#激活
	def all(self):
		return self.get_queryset().active()


#视频类别数据库
class Category(models.Model):
	#类别名称
	title = models.CharField(max_length=120)
	#类别描述
	description = models.TextField(max_length=5000, null=True, blank=True)
	#类别图标
	image = models.ImageField(upload_to='images/', null=True, blank=True)
	#类别slug
	slug = models.SlugField(default='abc', unique=True)
	#类别是否被激活
	active = models.BooleanField(default=True)
	#类别是否首页
	featured = models.BooleanField(default=False)
	#类别生成时间
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	#类别更新时间
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	#类别标签
	tags = GenericRelation("TaggedItem", null=True, blank=True)
	#自定义查询
	objects = CategoryManager()

	class Meta:
		ordering = ['title', 'timestamp']

	def __unicode__(self):
		return self.title

	#返回当前类别的地址，返回的格式方便tamplate使用
	def get_absolute_url(self):
		return reverse("project_detail", kwargs={"cat_slug": self.slug})
	
	#返回类别图标地址
	def get_image_url(self):
		return "%s%s" %(settings.MEDIA_URL, self.image)


#标签数据库中tag的选项
TAG_CHOICES = (
	("python", "python"),
	("django", "django"),
	("css", "css"),
	("bootstrap", "bootstrap"),
)


#标签数据库
class TaggedItem(models.Model):
	#标签的slug
	tag = models.SlugField(choices=TAG_CHOICES)
	#标签外键数据类型
	content_type = models.ForeignKey(ContentType)
	#标签外键id
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	def __unicode__(self):
		return self.tag