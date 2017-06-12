from django.http import HttpResponse
from django.shortcuts import render

from .models import Post


def index(request):
    # Hello, world!를 출력해주는 index 함수
    return HttpResponse('Hello, world!')


def post_list(request):
    # 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용한다.
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'post/post_list.html', context)
