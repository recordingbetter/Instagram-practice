import requests
from config import settings


def search(request, q):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'q': q,
        'part': 'snippet',
        'type': request.GET.get('type', ''),
        'maxResults': request.GET.get('maxResults', ''),
        'key': settings.YOUTUBE_KEY,
        }
    # Youtube search api에 요청, 응답받음
    response = requests.get(url_api_search, params=search_params)
    data = response.json()
    return data


# def search()