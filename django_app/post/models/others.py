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
    ]


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Tag({})'.format(self.name)

