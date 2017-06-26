import requests
from django.shortcuts import render

from config import settings

__all__ = [
    'youtube_search',
    ]


def youtube_search(request):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')
    if q:
        search_params = {
            'q': q,
            'type': 'video',
            'part': 'snippet',
            'maxResult': '10',
            # 'type': request.GET.get('type', ''),
            # 'part': request.GET.get('part', ''),
            # 'maxResult': request.GET.get('maxResult', ''),
            'key': settings.YOUTUBE_KEY,
            }
        response = requests.get(url_api_search, params=search_params)
        print(response)
        context = {
            'response': response.json(),
            }
    else:
        context = {}
    return render(request, 'post/youtube_search.html', context)
