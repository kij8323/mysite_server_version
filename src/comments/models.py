#coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils.text import Truncator

# Create your models here.
from accounts.models import MyUser
from videos.models import Video
#from django.db.models.signals import post_save
#from notifications.signals import notify_reply

class CommentManager(models.Manager):
	#返回所有的激活的父评论（非子评论）
	def all(self):
		return super(CommentManager, self).filter(active=True).filter(parent=None)
	#返回最近的6个评论
	def recent(self):
		try:
			limit_to = settings.RECENT_COMMENT_NUMBER
		except:
			limit_to = 6
		return self.get_queryset().filter(active=True).filter(parent=None)[:limit_to]
	#创建一个评论
	def create_comment(self, user=None, text=None, path=None, video=None, parent=None, reponse=None):
		if not path:
			raise ValueError("Must include a path when adding a Comment")
		if not user:
			raise ValueError("Must include a user when adding a Comment")

		comment = self.model(
			user = user,
			path = path, 
			text = text
		)
		if video is not None:
			comment.video = video
		if parent is not None:
			comment.parent = parent	
		if reponse is not None:
			comment.reponse = reponse			
		comment.save(using=self._db)
		return comment

#评论
class Comment(models.Model):
	#发表评论用户
	user = models.ForeignKey(MyUser)
	#评论的父评论
	parent = models.ForeignKey("self", null=True, blank=True)
	#路径
	path = models.CharField(max_length=350)
	#评论的视频
	video = models.ForeignKey(Video, null=True, blank=True)
	#评论内容
	text = models.TextField()
	#评论发表时间
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	#评论修改时间
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	#评论是否激活
	active = models.BooleanField(default=True)
	#自定义查询
	objects = CommentManager()
	#回复的评论用户
	reponse = models.CharField(max_length=255)


	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return self.user.username
	#该评论主页
	def get_absolute_url(self):
		return reverse('comment_thread', kwargs={"id": self.id})
	#评论路径
	@property 
	def get_origin(self):
		return self.path
	#返回评论的前120个字符
	@property
	def get_preview(self):
		#return truncatechars(self.text, 120)
		return Truncator(self.text).chars(120)
	#返回评论内容
	@property
	def get_comment(self):
		return self.text
	#判断评论是否为一个子评论
	@property
	def is_child(self):
		if self.parent is not None:
			return True
		else:
			return False
	#如果评论是一个父评论，则返回该评论的所有子评论,并按时间顺序重新排列子评论，即下面的回复是最新的回复
	def get_children(self):
		if self.is_child:
			return None
		else:
			return Comment.objects.filter(parent=self).reverse()

	#返回父评论
	@property
	def get_parent(self):
		if self.parent is not None:
			return self.parent
		else:
			return False

	#返回评论回复的评论用户
	@property
	def get_reponse(self):
		if self.reponse is not None:
			return self.reponse
		else:
			return False

	#返回该评论中所有发表子评论的用户列表（该功能只使用于有子评论的父评论）
	def get_affected_users(self):
		""" 
		it needs to be a parent and have children, 
		the children, in effect, are the affected users.
		"""
		comment_children = self.get_children()
		if comment_children is not None:
			users = []
			for comment in comment_children:
				if comment.user in users:
					pass
				else:
					users.append(comment.user)
			return users
		return None


#当有一个新用户注册，就会发送一条消息给notifications这个app
# def Comment_receiver(sender, instance, created, *args, **kwargs):
# 	if created:
# 		notify_reply.send(sender, 
# 				recipient=instance.user,
# 				comment=instance, 
# 				action=created)


# post_save.connect(Comment_receiver, sender=Comment)