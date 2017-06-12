from django.db import models
from django.contrib.auth.models import User

'''
member app
    User model
        username, nickname
이후 해당 User 모델을 Post나 Comment 에서 author나 user 항목으로 참조할 수 있게
'''


class Post(models.Model):
    author = models.ForeignKey(User)
    photo = models.ImageField(blank = True,
                              upload_to = 'photos/%Y/%m/%d',
                              height_field = 100,
                              width_field = 100,
                              max_length = 100)
    like_users = models.ManyToManyField(User, related_name = 'like_posts')
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    tags = models.ManyToManyField('Tag')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)


class Tag(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return 'Tag({})'.format(self.name)
