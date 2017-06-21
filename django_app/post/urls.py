from django.conf.urls import url

from . import views

# url() 사용법
# https://docs.djangoproject.com/en/1.11/ref/urls/#url

app_name = 'post'
urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<post_pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_pk>[0-9]+)/modify/$', views.post_modify, name='post_modify'),
    url(r'^(?P<post_pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<post_pk>[0-9]+)/comment/create/$', views.comment_create, name='comment_create'),
    url(r'^comment/(?P<comment_pk>[0-9]+)/modify/$', views.comment_modify, name='comment_modify'),
    url(r'^comment/(?P<comment_pk>[0-9]+)/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.hashtag_post_list, name='hashtag_post_list'),
    url(r'^(?P<post_pk>[0-9]+)/like/$', views.post_like, name='post_like'),

    ]
