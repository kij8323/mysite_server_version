#coding=utf-8
'''
页面与函数映射关系
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


#主页
urlpatterns = patterns('',
    #联系我
    url(r'^contact/$', TemplateView.as_view(template_name='company/contact_us.html'), name='contact_us'),
    #主页
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^dashboardcomment/$', 'srvup.views.dashboardcomment', name='dashboardcomment'),
    #url(r'^staff/$', 'srvup.views.staff_home', name='staff'),
    #管理员页面
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#视频页面
urlpatterns += patterns('videos.views',
    url(r'^projects/(?P<cat_slug>[\w-]+)/$', 'category_detail', name='project_detail'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'video_detail', name='video_detial'), 
    url(r'^projects/$', 'category_list', name='projects'), 
)

#账单页面（暂时不涉及）
urlpatterns += patterns('billing.views',
    url(r'^upgrade/$', 'upgrade', name='account_upgrade'),
)

#用户账户页面
urlpatterns += patterns('accounts.views',
    #用户登录
    url(r'^login/$', 'auth_login', name='login'),
    #用户登出
    url(r'^logout/$', 'auth_logout', name='logout'),
    #用户注册
    url(r'^register/$', 'auth_register', name='register'),
)

#视频评论页面
urlpatterns += patterns('comments.views',
    #评论编辑具体页面
    url(r'^comment/(?P<id>\d+)$', 'comment_thread', name='comment_thread'),
    #评论增加函数
    url(r'^comment/create/$', 'comment_create_view', name='comment_create'),
)


#通知页面（在主页暂时隐去）
urlpatterns += patterns('notifications.views',
    url(r'^notifications/$', 'all', name='notifications_all'),
    url(r'^notifications-unread/$', 'unreadmessage', name='notifications_unread'),
    url(r'^notifications/(?P<id>\d+)/$', 'read', name='notifications_read'),
    url(r'^hello/$', 'hello', name='hello'),
)

