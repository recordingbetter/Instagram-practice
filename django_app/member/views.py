from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from member.forms import LoginForm

User = get_user_model()


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 html 생성
    # POST 요청이 올 경우 로그인 완료 후 post_list로 이동
    # 실패할 경우, HttpResponse로 'Login invalid!' 띄어주기
    # member/urls.py 생성
    if request.method == 'POST':
        # Form class 미사용시
        # username = request.POST['username']
        # password = request.POST['password']
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password,
        #     Form class 사용시,
        #     )
        # if user is not None:
        #     django_login(request, user)
        #     return redirect('post:post_list')
        # else:
        #     return HttpResponse('Login credentials invalid.')

        # Form class 사용시
        form = LoginForm(data=request.POST)
        # Bound form의 유효성 검사
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login credentials invalid.')
    else:
        # 이미 로그인된 상태일 경우
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()
        context = {
            'form': form,
            }
        return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    # member/signup.html을 사용하여 username, password1, password2를 받아 회원가입
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # 이미유저가 존재하는지 검사
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username is already exist!')
        # password1, password2가 일치하는지 검사
        elif password1 != password2:
            return HttpResponse('Passwords are not match!')
        # 가입 성공시 로그인시키고 post_list 로 리다이렉트
        user = User.objects.create_user(
            username=username,
            password=password1,
            )
        # login
        django_login(request, user)
        return redirect('post:post_list')
    else:
        return render(request, 'member/signup.html')
