import re

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render, redirect

from config import settings
from post.models import Video, Post

__all__ = [
    # 'youtube_search',
    'youtube_search_save',
    'youtube_post',
    ]

# def youtube_search(request):
#     url_api_search = 'https://www.googleapis.com/youtube/v3/search'
#     q = request.GET.get('q')
#     if q:
#         search_params = {
#             'q': q,
#             'type': 'video',
#             'part': 'snippet',
#             'maxResult': '10',
#             # 'type': request.GET.get('type', ''),
#             # 'part': request.GET.get('part', ''),
#             # 'maxResult': request.GET.get('maxResult', ''),
#             'key': settings.YOUTUBE_KEY,
#             }
#         response = requests.get(url_api_search, params=search_params)
#         context = {
#             'response': response.json(),
#             }
#     else:
#         context = {}
#     return render(request, 'post/youtube_search.html', context)


def youtube_search_save(request):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')
    if q:
        search_params = {
            'q': q,
            'part': 'snippet',
            'type': request.GET.get('type', ''),
            'maxResults': request.GET.get('maxResults', ''),
            'key': settings.YOUTUBE_KEY,
            }
        response = requests.get(url_api_search, params=search_params)
        videos = response.json().get('items')
        # 찾아진 결과를 DB에 저장
        for video_item in videos:
            video, video_create = Video.objects.get_or_create(
                youtube_id=video_item['id']['videoId'],
                defaults={
                    'youtube_title': video_item['snippet']['title'],
                    'youtube_thumbnail_url': video_item['snippet']['thumbnails']['high']['url'],
                    'youtube_description': video_item['snippet']['description'],
                    }
                )
            # DB에 저장했으면 thumbnail도 DB에 저장
            if video_create:
                url_thumbnail = video_item['snippet']['thumbnails']['high']['url']
                p = re.compile(r'.*\.([^?]+)')
                file_ext = re.search(p, url_thumbnail).group(1)
                file_name = '{}.{}'.format(
                    video_item['id']['videoId'],
                    file_ext
                    )
                temp_file = NamedTemporaryFile()
                response = requests.get(url_thumbnail)
                temp_file.write(response.content)
                video.youtube_thumbnail.save(file_name, File(temp_file))
        # youtube_search.html에 보여주는건 DB에서 title 검색 결과
        search_result = Video.objects.filter(youtube_title__contains=q)
        context = {
            'search_result': search_result,
            # 'videos': videos,
            }
    else:
        context = {}
    return render(request, 'post/youtube_search.html', context)


def youtube_post(request, video_id):
    video = Video.objects.get(pk=video_id)
    # video pk를 FK로 가지는 Post 생성
    post = video.post_set.create(
        video_id=video_id,
        author=request.user,
        photo=video.youtube_thumbnail,
        )
    # 비디오타이틀을 comment로 저장
    post.comment_set.create(
        content=video.youtube_title,
        author=request.user,
        )
    return redirect('post:post_list')

