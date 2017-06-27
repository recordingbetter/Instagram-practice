from django.db import models

# from django.contrib.auth.models import User

'''
member app
    User model
        username, nickname
이후 해당 User 모델을 Post 나 Comment 에서 author 나 user 항목으로 참조할 수 있게
'''

__all__ = [
    'Tag',
    'Video',
    ]


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Tag({})'.format(self.name)


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
