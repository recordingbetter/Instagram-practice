from django.http import HttpResponse
from django.shortcuts import render, redirect


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 html 생성
    # POST 요청이 올 경우 좌측코드를 기반으로 로그인 완료 후 post_list로 이동
    # 실패할 경우, HttpResponse로 'Login invalid!' 띄어주기

    # member/urls.py 생성

    if request.method == 'POST':
        pass
    else:
        return render(request, 'member/login.html')

