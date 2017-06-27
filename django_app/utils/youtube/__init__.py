import requests
from googleapiclient.discovery import build

from config import settings


def search_original(request, q):
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


def search_post(q):
    DEVELOPER_KEY = settings.YOUTUBE_KEY
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY
        )
    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=q,
        part='id,snippet',
        type='video',
        maxResults='10',
        ).execute()
    return search_response

