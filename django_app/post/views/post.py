from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views.decorators.http import require_POST

from ..decorators import post_owner
from ..forms import PostForm, CommentForm
from ..models import Post, Tag

# from member.models import User

# 자동으로 Django에서 인증에 사용하는 User 모델클래스를 불러온다.
#   https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.get_user_model
User = get_user_model()

# __all__ 설정하면 __init__ 에서 전체를 import해도 됨
__all__ = (
    'post_list',
    'post_detail',
    'post_create',
    'post_modify',
    'post_delete',
    'hashtag_post_list',
    'post_like_toggle',
    )


def post_list_original(request):
    # 모든 Post 목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용한다.
    context = {
        'posts': Post.objects.all(),
        # comment를 위해 CommentForm을 전달. post에서 CommentFormㅇ
        'comment_form': CommentForm(),
        }
    return render(request, 'post/post_list.html', context)


def post_list(request):
    all_posts = Post.objects.all()
    p = Paginator(all_posts, 2)
    page = request.GET.get('page')
    try:
        posts = p.page(page)
    except PageNotAnInteger:
        posts = p.page(1)
    except EmptyPage:
        posts = p.page(p.num_pages)

    context = {
        'posts': posts,
        'comment_form': CommentForm(),
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


# @post_owner
# @login_required
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


def hashtag_post_list(request, tag_name):
    # 1. template생성
    #   post/hashtag_post_list.html
    #   tag_name과 post_list, post_count변수를 전달받아 출력
    #   tag_name과 post_count는 최상단 제목에 사용
    #   post_list는 순회하며 post_thumbnail에 해당하는 html을 구성해서 보여줌
    #
    # 2. 쿼리셋 작성
    #   특정 tag_name이 해당 Post에 포함된 Comment의 tags에 포함되어있는 Post목록 쿼리 생성
    #        posts = Post.objects.filter()
    #
    # 3. urls.py와 이 view를 연결
    # 4. 해당 쿼리셋을 적절히 리턴
    # 5. Comment의 make_html_and_add_tags()메서드의
    #    a태그를 생성하는 부분에 이 view에 연결되는 URL을 삽입
    tag = get_object_or_404(Tag, name=tag_name)
    # Post에 달린 댓글의 Tag까지 검색할때
    # post = Post.objects.filter(comment__tags=tag).distinct()
    # Post의 mt_comment에 있는 Tag만 검색할때
    posts = Post.objects.filter(my_comment__tags=tag)
    posts_count = posts.count()

    context = {
        'tag': tag,
        'posts': posts,
        'posts_count': posts_count,
        }
    return render(request, 'post/hashtag_post_list.html', context)


@require_POST
@login_required
def post_like_toggle(request, post_pk):
    # 1. post_pk 에 해당하는 Post instance를 변수(post)에 할당
    post = get_object_or_404(Post, pk=post_pk)
    # 2. post에서 PostLike로의 RelatedManager를 사용해서
    #       post속성이 post, user속성이 request.user인 PostLike가 있는지 get_or_create

    # M2M 필드가 중간자모델을 거치지않을 경우
    # if request.user not in post.like_users:
    #     post.like_users.add(request.user)

    # 중간자 모델을 사용할 경우
    # get_or_create를 사용해서 현재 Post와 request.user에 해당하는 PostLike인스턴스를 가져옴
    post_like, post_like_created = post.postlike_set.get_or_create(
        user=request.user,
        )
    # 3. 이후 created여부에 따라 해당 PostLike인스턴스를 삭제 또는 그냥 넘어가기
    # post_like_created가 get_or_create를 통해 새로 PostLike가 만들어졌는지, 아니면 기존에 있었는지 여부를 나타냄
    if not post_like_created:
        # 기존에 PostLike가 있었다면 삭제해준다
        post_like.delete()
    # 4. 리턴주소는 next가 주어질 경우 next, 아닐 경우 post_detail로
    # next = request.GET.get('next')
    # if next:
    #     return redirect(next)
    return redirect('post:post_detail', post_pk=post.pk)


