"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # 내장된 클래스를 사용하여 만들어져있는 url로 리다이렉트.(view 만들 필요 없음)
    # url(r'^$', RedirectView.as_view(pattern_name='post:post_list')),

    url(r'^admin/', admin.site.urls),
    # post앱의 urls.py모듈을 include시킨다
    url(r'^post/', include('post.urls')),
    url(r'^member/', include('member.urls')),
    ]
# static 함수는 리스트를 반환하므로 기존 urlpatterns 에 더해준다.
# ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
# 위 내용과 같다.
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
    )
