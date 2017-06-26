import re

import requests
from django.contrib import messages
from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
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
    # facebook_login view가 처음 호출될 때
    #   유저가 Facebook login dialog에서 로그인 후, 페이스북에서 우리서비스 (Consumer)쪽으로
    #   GET parameter를 이용해 'code'값을 전달해줌 (전달받는 주소는 위의 uri_redirect)
    code = request.GET.get('code')
    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
        )

    class GetAccessTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['error']
            self.code = error_dict['code']
            self.message = error_dict['message']
            self.is_valid = error_dict['is_valid']
            self.scope = error_dict['scope']

    class DebugTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['error']
            self.code = error_dict['code']
            self.message = error_dict['message']

    # 페이스북 로그인 오류메세지를 request에 추가하고, 이전 페이지로 redirect
    def add_message_and_redirect_referer():
        # 유저용 에러 메세지
        error_message_for_user = 'Facebook login error'
        messages.error(request, error_message_for_user)
        # print(result['error']['type'])
        # print(result['error']['message'])
        return redirect(request.META['HTTP_REFERER'])

    # code를 받아 액세스토큰
    def get_access_token(code):
        # 액세스토큰의 코드를 교환할 UR
        url_access_token = 'https://graph.facebook.com/v2.9/oauth/access_token'

        # 이전에 요청했던 redirect_uri와 같은 값을 만들어 줌 (access_token을 요청할 때 필요함)
        redirect_uri = '{}://{}{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
            )
        # if code:
        # 액세스토큰의 코드 교환
        # uri생성을 위한 params
        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            # 요청했던 uri와 정확히 같아야 함
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
            }
        # 해당 URL에 get요청 후 결과 (json형식)를 파이썬 object로 변환 (result변수)
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()
        # pprint(result)

        if 'access_token' in result:
            return result['access_token']
        # 액세스토큰 코드교환 결과에 오류가 있을 경우
        # 해당 오류를 request에 message로 넘기고 이전페이지 (HTTP_REFERER)로 redirect
        elif 'error' in result:
            # 상세 오류 메세지(개발자용)
            # error_message = 'Facebook login error\n type: {}\n message: {}'.format(
            #     result['error']['type'],
            #     result['error']['message']
            #     )
            raise GetAccessTokenException(result)
            # # 유저용 에러 메세지
            # error_message_for_user = 'Facebook login error'
            # messages.error(request, error_message_for_user)
            # # print(result['error']['type'])
            # # print(result['error']['message'])
            # return redirect(request.META['HTTP_REFERER'])
        else:
            raise Exception('Unknown user')

    def debug_token(token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': app_access_token,
            }
        response = requests.get(url_debug_token, params=url_debug_token_params)
        result = response.json()
        if 'error' in result['data']:
            raise GetAccessTokenException(result)
        else:
            return result

    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/{user_id}'.format(user_id=user_id)
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'email',
                'first_name',
                'last_name',
                'picture.type(large)',
                'gender',
                ])
            }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result

    # code키값이 존재하지 않으면 로그인을 더이상 진행하지 않음
    if not code:
        return add_message_and_redirect_referer()
    try:
        # 이 view에 GET parameter로 전달된 code를 사용해서 access_token을 받아옴
        # 성공시 access_token값을 가져옴
        # 실패시 GetAccessTokenException이 발생
        access_token = get_access_token(code)

        # 위에서 받아온 access_token을 이용해 debug_token을 요청
        # 성공시 토큰을 디버그한 결과 (user_id, scopes 등..)이 리턴
        # 실패시 DebugTokenException이 발생
        debug_result = debug_token(access_token)

        # debug_result에 있는 user_id값을 이용해서 GraphAPI에 유저정보를 요청
        user_info = get_user_info(user_id=debug_result['data']['user_id'], token=access_token)
        # print(user_info)
        user = User.objects.get_or_create_facebook_user(user_info)

        django_login(request, user)
        return redirect(request.META['HTTP_REFERER'])

    except GetAccessTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()

