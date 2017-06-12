from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # Hello, world!를 출력해주는 index 함수
    return HttpResponse('Hello, world!')
