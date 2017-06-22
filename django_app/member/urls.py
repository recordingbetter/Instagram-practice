from django.conf.urls import url

from . import views

app_name = 'member'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='my_profile'),
    url(r'^profile/(?P<user_pk>\d+)/$', views.profile, name='profile'),
    url(r'^follow/(?P<user_pk>\d+)/$', views.follow_toggle_view, name='follow'),
    url(r'^block/(?P<user_pk>\d+)/$', views.block_toggle_view, name='block'),
    ]
