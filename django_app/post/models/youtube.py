import re

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

__all__ = [
    'Video',
    ]


class VideoManager(models.Manager):
    def create_from_search_results(self, video_item):
        """
        :param result: YouTube Search API를 사용 후, 검색 결과에서 'items'리스트의 각 항목
        :return: Video object
        """
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
        return video


class Video(models.Model):
    youtube_id = models.CharField(max_length=30)
    youtube_thumbnail = models.ImageField(upload_to='youtube_thumbnail')
    youtube_thumbnail_url = models.CharField(max_length=50, null=True, blank=True)
    youtube_title = models.CharField(max_length=100)
    youtube_description = models.TextField(null=True, blank=True)

    # def get_or_create_video(self, video_item):
    #     video, video_create = self.get_or_create(
    #         youtube_id=video_item['id']['videoId'],
    #         defaults={
    #             'youtube_title': video_item['snippet']['title'],
    #             'youtube_thumbnails': video_item['snippet']['thumbnails']['high']['url'],
    #             'youtube_description': video_item['snippet']['description']
    #             }
    #         )
    #     if video_create:
    #         url_thumbnail = video_item['snippet']['thumbnails']['high']['url']
    #         p = re.compile(r'.*\.([^?]+)')
    #         file_ext = re.search(p, url_thumbnail).group(1)
    #         file_name = '{}.{}'.format(
    #             video_item['id']['videoId'],
    #             file_ext
    #             )
    #         temp_file = NamedTemporaryFile()
    #         response = requests.get(url_thumbnail)
    #         temp_file.write(response.content)
    #         video.youtube_thumbnail.save(file_name, File(temp_file))
    #     return video
    #
