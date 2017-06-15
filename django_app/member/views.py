from django.contrib.auth import authenticate, login as django_login
from django.http import HttpResponse
from django.shortcuts import render, redirect


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 html 생성
    # POST 요청이 올 경우 좌측코드를 기반으로 로그인 완료 후 post_list로 이동
    # 실패할 경우, HttpResponse로 'Login invalid!' 띄어주기

    # member/urls.py 생성

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request.POST)
        user = authenticate(
            request,
            username=username,
            password=password,
            )
        if user is not None:
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login credentials invalid.')
    else:
        return render(request, 'member/login.html')

