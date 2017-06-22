"""

1. pyenv virtualenv 3.6.1 instagram
2. pyenv local instagram
3. pip install django ipython django_extensions
4. django-admin startproject instagram
5. mv instagram django_app
6. pip freeze > requirements.txt
7. git init
8. cp <이전 gitignore위치> .
9. git add -A & git commit -m 'First commit'
10. Pycharm Interpreter설정


기능들
	회원관리 모듈 (member/)
		로그인
		회원관리
		팔로우
		친구찾기
		친구추천
		마이페이지
			내가 올린글
			내 정보 관리

	글 관련 모듈 (post/)
		뉴스피드
		사진업로드
		댓글달기
		좋아요누르기
		태그달기

	알림 관련 모듈 (noti/)
		팔로워의 글 등록 알림
		댓글 알림


Django settings for instagram project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

1. TEMPLATE_DIR에 instagram/django_app/templates 폴더를 생성후, 해당 경로를 지정
2. TEMPLATES 의 DIRS 리스트 설정에 위 변수 삽입
3. post_list.html에서 for loop 사용해 전달된 posts 변수 순환및출력
4. post_list view가 /post/접근시 출력되도록 post/urls.py에 설정
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR,
    ]
MEDIA_URL = '/media/'
# django_app/media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Custom user 모델
AUTH_USER_MODEL = 'member.User'
LOGIN_URL = 'member:login'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(-kvu&sn0)yzn(i@64@uvp#3f8#mis9!q2vl5su2_$o)@vcw!o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'post',
    'member',
    'utils',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # context_processors 추가
                'member.context_processors.forms',
                ],
            },
        },
    ]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True
