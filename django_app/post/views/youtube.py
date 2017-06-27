import requests
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from config import settings
from post.models import Video, Post, Comment
from utils import youtube

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
    """
    유튜브 검색을
    :param request:
    :return:
    """
    context = dict()
    q = request.GET.get('q')
    if q:
        data = youtube.search_post(q)
        # 찾아진 결과를 DB에 저장
        for video_item in data['items']:
            # model에 만든 ModelManager 사용
            Video.objects.create_from_search_results(video_item)
# 검색방법
        # youtube_search.html에 보여주는건 DB에서 title 검색 결과
        # title에 검색어가 포함되는지 여부
        # search_result = Video.objects.filter(youtube_title__contains=q)
        #
        # title과 description에 검색어가 포함되는지 여부
        # search_result = Video.objects.filter(Q(youtube_title__contains=q) | Q(description__contains=q))
        #
        # 검색어가 빈칸으로 구분되어있을때 (빈칸으로 split한 값들을 각각 포함하고 있는지 and 연산)
        # 원초적인 방법
        # Video.objects.all()
        # for cur_q in q.split(' '):
        #     videos.filter(title__contains=cur_q)
        # videos.filter(title__contains='aa').filter(title__contains='bb').filter(title__contains='cc')...

        # regex 사용법 대박!!
        # and 연산
        re_pattern = ''.join(['(?=.*{})'.format(item) for item in q.split()])
        # or 연산
        # re_pattern = '|'.join(['({})'.format(item) for item in q.split()])
        # title과 description중 하나만 조건을 만족하면 됨
        search_result = Video.objects.filter(
            Q(youtube_title__iregex=re_pattern) |
            Q(youtube_description__iregex=re_pattern)
        )
        context['search_result'] = search_result
    # else:
    #     context = {}
    return render(request, 'post/youtube_search.html', context)


# 숙제...
def youtube_post(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    # video pk를 FK로 가지는 Post 생성
    post = video.post_set.create(
        # video_id=video_id,
        author=request.user,
        photo=video.youtube_thumbnail,
        )
    # 비디오타이틀을 comment로 저장
    post.my_comment = Comment.objects.create(
        post=post,
        content=video.youtube_title,
        author=request.user,
        )
    return redirect('post:post_list')


# #  학원...
# def youtube_post(request, video_id):
#     # video_pk = request.POST['video_pk']
#     video = get_object_or_404(Video, pk=video_id)
#     post = Post.objects.create(
#         author=request.user,
#         video=video,
#         )
#     post.my_comment = Comment.objects.create(
#         author=request.user,
#         content=video.youtube_title,
#         )
#     return redirect('post:post_detail', post_pk=post.pk)
