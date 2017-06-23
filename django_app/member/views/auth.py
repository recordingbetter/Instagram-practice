from pprint import pprint

import requests
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.shortcuts import render, redirect

from config import settings
from ..forms import LoginForm, SignupForm

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login',
    )


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
        # LoginForm인스턴스 를 생성해서 context 에 넘김
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
            next_ = request.GET.get('next')
            if next_:
                return redirect(next_)

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


def facebook_login(request):
    redirect_uri = '{}://{}{}'.format(
        request.scheme,
        request.META['HTTP_HOST'],
        request.path,
        )
    url_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'
    # facebook_login view 가 처음 호출될때 'code' request GET parameter 를 받음
    code = request.GET.get('code')
    if code:
        # 액세스토큰의 코드 교환
        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            # 요청했던 uri와 정확히 같아야 함
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
            }
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()
        pprint(result)
