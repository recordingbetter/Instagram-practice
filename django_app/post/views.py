from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

# from member.models import User
from .models import Post, Comment

# 자동으로 Django에서 인증에 사용하는 User 모델클래스를 불러온다.
User = get_user_model()


def post_list(request):
    # 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용한다.
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post = Post.objects.get(pk=post_pk)
    # 가져오는 과정에서 예외처리
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        return redirect('post:post_list')
        # return HttpResponseNotFound('Post not found, detail: {}'.format(e))
    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
        'post_pk': post_pk,
    }
    # return render(request, 'post/post_detail.html', context)
    # template에 인자로 주어진 context, request를 render 함수를 사용해서 해당 template을 string으로 변환
    rendered_string = template.render(context=context, request=request)
    # 변환된 string을 HttpResponse 형태로 돌려준다.
    return HttpResponse(rendered_string)
    # 아래 2줄과 같다.
    # url = reverse('post:post_list')
    # return HttpResponseRedirect(url)

def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 post_list페이지로 redirect
    if request.method == "GET":
        return render(request, 'post/post_create.html')
    elif request.method == "POST":
        # data = request.POST
        photo = request.FILES['photo']
        author = User.objects.first()
        # tags = data['tags']
        post = Post.objects.create(
            photo=photo,
            author=author,
            # tags=tags,
        )
        # comment 키의 값이 없을 경우''빈값을 반환
        comment_string = request.POST.get('comment', '')
        # 빈문자열이나 None 모두 False이므로 데이터가 존재하는지 검사 가능
        if comment_string:
            # comment 값이 있을경우 Comment 객체 생성
            post.comment_set.create(
                author=author,
                content=comment_string,
            )
            #post 값이 없을 경우
            # Comment.objects.create(
            #     post=post,
            #     author=author,
            #     content=comment_string,
            # )

        return redirect('post:post_detail', post_pk=post.pk)


def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    if request.method == "GET":
        context = {
            'post': post,
        }
        return render(request, 'post/post_modify.html', context)
    elif request.method == "POST":
        # data = request.POST
        photo = request.FILES['photo']
        # tags = data['tags']
        post.photo = photo
        # tags=tags,
        post.save()
        return redirect('post:post_detail', post_pk)


def post_delete(request, post_pk):
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료후에는 post_list페이지로 redirect
    if request.method == "POST":
        post = Post.objects.get(pk=post_pk)
        post.delete()
        return redirect('post:post_list')
    else:
        return HttpResponse('not allowed')


def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    if request.method == "POST":
        data = request.POST
        Comment.objects.create(
            content=data['comment'],
            author=User.objects.get(pk=2),
            post_id=data['post_pk'],
        )
        return redirect('post:post_list')
    else:
        return HttpResponse('not allowed')


def comment_modify(request, post_pk):
    # 수정
    pass


def comment_delete(request, post_pk, comment_pk):
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    pass
