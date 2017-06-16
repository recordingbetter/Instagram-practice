from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm
from .forms.signup import SignupForm

User = get_user_model()


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 html 생성
    # POST 요청이 올 경우 로그인 완료 후 post_list로 이동
    # 실패할 경우, HttpResponse로 'Login invalid!' 띄어주기
    # member/urls.py 생성
    if request.method == 'POST':
        origin_html = request.environ['HTTP_REFERER']
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
            return redirect(origin_html)
        else:
            return HttpResponse('Login credentials invalid.')
    # method가 GET 일때
    else:
        # 만약 이미 로그인 된 상태일 경우에는
        # post_list로 redirect
        if request.user.is_authenticated:
            return redirect('post:post_list')
        # LoginForm인스턴스를 생성해서 context에 넘김
        form = LoginForm()
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
