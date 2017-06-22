from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    동작
        follow: 내가 다른 사람을 follow 함
        unfollow: 내가 다른 사람에게 한 follow 를 취소함

    속성
        follower: 나를 follow 하고있는 사람
        followers: 나를 follow 하고있는 사람들
        following: 내가 follow 하고있는 사람들

        friend: 나와 서로 follow하고 있는 관계의 사람
        friends: 나와 서로 follow하고 있는 모든 관계
        없음: 내가 follow 하고있는 사람 1명
    """
    nickname = models.CharField(max_length=24, null=True, unique=True)

    def __str__(self):
        return self.nickname or self.username
        # return self.nickname if self.nickname else self.username
