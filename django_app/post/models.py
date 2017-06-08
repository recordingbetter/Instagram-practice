from django.db import models

'''
member app
    User model
        username, nickname
이후 해당 User 모델을 Post나 Comment 에서 author나 user 항목으로 참조할 수 있게
'''


class Post(models.Model):
    # author, user 필드는 제외하고 생성
    pass


class Comment(models.Model):
    pass


class PostLike(models.Model):
    pass


class Tag(models.Model):
    pass
