from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from post.models import Post
from .forms import LoginForm
from .forms.signup import SignupForm

User = get_user_model()


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 html 생성
    # POST 요청이 올 경우 로그인 완료 후 post_list로 이동
    # 실패할 경우, HttpResponse로 'Login invalid!' 띄어주기
    # member/urls.py 생성
    # method가 GET 일때
    if request.method == 'GET':
        # 만약 이미 로그인 된 상태일 경우에는
        # post_list로 redirect
        if request.user.is_authenticated:
            return redirect('post:post_list')
        # LoginForm인스턴스를 생성해서 context에 넘김
        form = LoginForm()

    # method가 POST 일때
    else:
        # origin_html = request.environ['HTTP_REFERER']
        # Form class 미사용시
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password,
        #     )
        # if user is not None:
        #     django_login(request, user)
        #     return redirect(origin_html)
        # else:
        #     return HttpResponse('Login credentials invalid.')

        # Form class 사용시
        form = LoginForm(data=request.POST)
        # Bound form의 유효성 검사
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            # 일반적인 경우에는 post_list로 이동하지만,
            # GET parameter의 next 속성값이 있을 경우 해당 url로 이동
            next = request.GET.get('next')
            if next:
                return redirect(next)

            return redirect('post:post_list')
        # else:
        #     return HttpResponse('Login credentials invalid.')
    context = {
        'form': form,
        }
    # render시 context에는 LoginForm클래스형 form객체가 포함됨
    return render(request, 'member/login.html', context)


def logout(request):
    origin_html = request.environ['HTTP_REFERER']
    django_logout(request)
    return redirect(origin_html)


def signup(request):
    # member/signup.html을 사용하여 username, password1, password2를 받아 회원가입
    if request.method == 'POST':
        #     # Form class 미사용시
        #     username = request.POST['username']
        #     password1 = request.POST['password1']
        #     password2 = request.POST['password2']
        #     # 이미유저가 존재하는지 검사
        #     if User.objects.filter(username=username).exists():
        #         return HttpResponse('Username is already exist!')
        #     # password1, password2가 일치하는지 검사
        #     elif password1 != password2:
        #         return HttpResponse('Passwords are not match!')
        #     # 가입 성공시 로그인시키고 post_list 로 리다이렉트
        #     user = User.objects.create_user(
        #         username=username,
        #         password=password1,
        #         )
        #     # login
        #     django_login(request, user)
        #     return redirect('post:post_list')
        # else:
        #     return render(request, 'member/signup.html')

        # Form class 사용시,
        form = SignupForm(data=request.POST)
        # valid check of bound form
        if form.is_valid():
            # username = form.cleaned_data['username']
            # password1 = form.cleaned_data['password1']
            # password2 = form.cleaned_data['password2']
            # 이후에 Form class 를 사용하지않는 경우를 적용해도 동작한다.
            user = form.create_user()
            django_login(request, user)
            return redirect('post:post_list')
        else:
            # form = SignupForm()
            # 에러메세지를 폼에 보여줄수있다.
            context = {
                'form': form,
                }
            return render(request, 'member/signup.html', context)

    form = SignupForm()
# 에러메세지를 폼에 보여줄수있다.
    context = {
        'form': form,
        }
    return render(request, 'member/signup.html', context)


def profile(request, user_pk=None):
    NUM_POSTS_PER_PAGE = 3
    # 0. urls.py 연결
    # 1. user_pk에 해당하는 User를 cur_user키로 render
    # 2. member/profile.html 작성, 해당 user 정보 보여주기
    #   2-1. 해당 user의 followers, following 목록 보여주기
    # 3. 현재 로그인한 유저가 해당 유저(cur_user)를 팔로우하고있는지 여부 보여주기
    #   3-1. 팔로우하고 있다면 '팔로우해제' 버튼, 아니라면 '팔로우' 버튼 보여주기
    # 4. -> def follow_toggle(request)뷰 생성
    # user = User.objects.get(pk=user_pk)
    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user
        # posts는 page 번호에 따라 9개씩 전달
        # filter나 order_by에는 안써도 됨
    posts = user.post_set.order_by('-created_date')[: NUM_POSTS_PER_PAGE * page]
    post_count = user.post_set.count()
    # next
    next_page = page + 1 if post_count > page * NUM_POSTS_PER_PAGE else page + 1
    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
        }
    return render(request, 'member/profile.html', context)


@login_required
@require_POST
def follow_toggle_view(request, user_pk):
    next = request.GET.get('next')
    cur_user = User.objects.get(pk=request.user.pk)
    profile_user = get_object_or_404(User, pk=user_pk)
    cur_user.follow_toggle(profile_user)
    if next:
        return redirect(next)
    return redirect('member:profile', user_pk=user_pk)


@login_required
@require_POST
def block_toggle_view(request, user_pk):
    cur_user = User.objects.get(pk=request.user.pk)
    profile_user = User.objects.get(pk=user_pk)
    cur_user.block_toggle(profile_user)
    return redirect('member:profile', user_pk=profile_user.pk)
