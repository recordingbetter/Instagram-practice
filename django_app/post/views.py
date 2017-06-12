from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.models import User
from .models import Post


def post_list(request):
    # 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용한다.
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴, 보여줌
    post = Post.objects.get(pk=post_pk)
    context = {
        'post': post,
        'post_pk': post_pk,
    }
    return render(request, 'post/post_detail.html', context)


def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 post_list페이지로 redirect
    if request.method == "GET":
        return render(request, 'post/post_create.html')
    elif request.method == "POST":
        data = request.POST
        photo = request.FILES['photo']
        author = User.objects.first()
        # tags = data['tags']

        post = Post.objects.create(
            photo=photo,
            author=author,
            # tags=tags,
        )
        return redirect('post_detail', post_pk=post.pk)


def post_modify(request, post_pk):
    # 수정
    pass


def post_delete(request, post_pk):
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료후에는 post_list페이지로 redirect


    pass


def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    pass


def comment_modify(request, post_pk):
    # 수정
    pass


def comment_delete(request, post_pk, comment_pk):
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    pass
