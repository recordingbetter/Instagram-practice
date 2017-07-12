from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.PostLikeCreateView.as_view()),
    url(r'^(?P<post_pk>\d+)/like-toggle$', apis.PostLikeToggleView.as_view()),
    ]
