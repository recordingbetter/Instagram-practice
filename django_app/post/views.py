from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse

# from member.models import User
from django.views.decorators.http import require_POST

from .decorators import post_owner, comment_owner
from .forms import PostForm, CommentForm
from .models import Post, Comment

# 자동으로 Django에서 인증에 사용하는 User 모델클래스를 불러온다.
#   https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.get_user_model
User = get_user_model()


def post_list(request):
    # 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용한다.
    context = {
        'posts': Post.objects.all(),

        }
    return render(request, 'post/post_list.html', context)


# @login_required
def post_detail(request, post_pk):
    # Model(DB)에서 post_pk에 해당하는 Post객체를 가져와 변수에 할당
    # ModelManager의 get메서드를 사용해서 단 한개의 객체만 가져온다
    # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#get
    # post = Post.objects.get(pk=post_pk)
    # 가져오는 과정에서 예외처리
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # 1. 404 Notfound를 띄워준다
        # return HttpResponseNotFound('Post not found, detail: {}'.format(e))

        # 2. post_list view로 돌아간다
        # 2-1. redirect를 사용
        #   https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#redirect
        # return redirect('post:post_list')
        # 2-2. HttpResponseRedirect
        #   https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpResponseRedirect
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

    # request에 대해 response를 돌려줄때는 HttpResponse나 render를 사용가능
    # template을 사용하려면 render함수를 사용한다
    # render함수는
    #   django.template.loader.get_template함수와
    #   django.http.HttpResponse함수를 축약해 놓은 shortcut이다
    #       https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#render

    # ! 이 뷰에서는 render를 사용하지 않고, 전체 과정(loader, HttpResponse)을 기술
    # Django가 템플릿을 검색할 수 있는 모든 디렉토리를 순회하며
    # 인자로 주어진 문자열값과 일치하는 템플릿이 있는지 확인 후,
    # 결과를 리턴 (django.template.backends.django.Template클래스형 객체)
    # get_template()메서드
    #   https://docs.djangoproject.com/en/1.11/topics/templates/#django.template.loader.get_template
    template = loader.get_template('post/post_detail.html')
    # dict형 변수 context의 'post'키에 post(Post객체)를 할당
    context = {
        'post': post,
        # 'post_pk': post_pk,
        }
    # return render(request, 'post/post_detail.html', context)
    # template에 인자로 주어진 context, request를 render 함수를 사용해서 해당 template을 string으로 변환
    rendered_string = template.render(context=context, request=request)
    # 변환된 string을 HttpResponse 형태로 돌려준다.
    return HttpResponse(rendered_string)


@login_required
def post_create(request):
    # 로그인하지 않은 상태라면 로그인 페이지로 이동
    # if not request.user.is_authenticated:
    #     return redirect('member:login')
    # POST요청을 받아 Post객체를 생성 후 post_list페이지로 redirect
    if request.method == "GET":
        form = PostForm()
    else:
        # # data = request.POST
        # # request.FILES에서 파일 가져오기
        # #   https://docs.djangoproject.com/en/1.11/topics/http/file-uploads/#basic-file-uploads
        # # 가져온 파일을 ImageField에 넣도록 설정
        # # 'file'은 POST요청시 input[type="photo"]이 가진 name속성
        # photo = request.FILES['photo']
        # author = User.objects.first()
        # # tags = data['tags']
        # post = Post.objects.create(
        #     photo=photo,
        #     author=author,
        #     # tags=tags,
        # )
        # # POST요청시 name이 'comment'인 input에서 전달된 값을 가져옴
        # # dict.get()
        # #   https://www.tutorialspoint.com/python/dictionary_get.htm
        # # comment 키의 값이 없을 경우''빈값을 반환
        # comment_string = request.POST.get('comment', '')
        # # 빈문자열이나 None 모두 False이므로 데이터가 존재하는지 검사 가능
        # if comment_string:
        #     # comment 값이 있을경우 Comment 객체 생성
        #     post.comment_set.create(
        #         author=author,
        #         content=comment_string,
        #     )
        #     # 역참조로 가져온 RelatedManager를 사용하지 않을경우엔 아래와 같이 작업함
        #     # Comment.objects.create(
        #     #     post=post,
        #     #     author=author,
        #     #     content=comment_string,
        #     # )
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # ModelForm의 save() 매서드를 이용해서 Post 객체를 가져옴
            post = form.save(
                author=request.user,
                )
            # post.comment = request.comment
            # post.author = request.user
            # post.save()

            # comment 확인한 내용으로 저장 ( views 에서 comment를 저장하는 방법)
            # comment_string = form.cleaned_data['comment']
            # if comment_string:
            #     post.comment_set.create(
            #         author=post.author,
            #         content=comment_string,
            #         )
            return redirect('post:post_detail', post_pk=post.pk)

        # post/post_create.html을 render해서 리턴
    context = {
        'form': form,
        }
    return render(request, 'post/post_create.html', context)


@post_owner
@login_required
def post_modify(request, post_pk):
    # 수정하고자하는 Post 객체
    post = Post.objects.get(pk=post_pk)
    if request.method == "GET":
        form = PostForm(instance=post)
    else:
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        form.save()
        return redirect('post:post_detail', post_pk=post.pk)
    context = {
        'form': form,
        }
    return render(request, 'post/post_modify.html', context)


@post_owner
@login_required
def post_delete(request, post_pk):
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료후에는 post_list페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post:post_list')
    else:
        context = {
            'post': post,
            }
        return render(request, 'post/post_delete.html', context)


# POST 요청만 받음
@require_POST
@login_required
def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment.objects.create(
            content=form.data['comment_field'],
            author=request.user,
            post_id=post_pk,
            )
        form.save()
    return redirect('post:post_detail', post_pk=post.pk)



@comment_owner
@login_required
def comment_modify(request, comment_pk):
    origin_html = request.environ['HTTP_REFERER']
    # post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(data=request.POST, instance=comment)
        form.save()
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
        }
    return render(request, origin_html, context)


@comment_owner
@login_required
def comment_delete(request, comment_pk):
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect(request.environ['HTTP_REFERER'])


def post_anyway(request):
    return redirect('post:post_list')
