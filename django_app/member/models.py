# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
import re

import requests
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

from config import settings
from utils.fields import CustomImageField


class UserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id'],
            )
        user, user_created = self.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'last_name': user_info.get('last_name', ''),
                'first_name': user_info.get('first_name', ''),
                'email': user_info.get('email', ''),
                }
            )
        # 유저가 새로 생성되었을 때만 프로필 이미지를 받아옴
        if user_created and user_info.get('picture'):
            # 프로필 이미지 url
            url_picture = user_info['picture']['data']['url']
            # print(url_picture)
            # https://scontent.xx.fbcdn.net/v/t1.0-1/p200x200/19059446_10209996745337245_5215440260872549542_n.jpg?oh=abd97958784c7774e52480592400bd3e&oe=59DE21C6

            # 파일 확장자
            p = re.compile(r'.*\.([^?]+)')
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                user.pk,
                file_ext,
                )
            print(file_name)
            # 이미지파일을 임시저장할 객체. delete=True(기본값) 로컬변수가 사라지는 순간 삭제됨
            temp_file = NamedTemporaryFile(delete=True)
            # 프로필 이미지 url에 대한 get 요청(이미지 다운로드)
            response = requests.get(url_picture)
            # 요청 결과를 temp_file에 기록
            temp_file.write(response.content)
            # ImageField의 save()메서드를 호출해서 해당 임시파일객체를 주어진 이름의 파일로 저장
            # 저장하는 파일명은 위에서 만든 <유저pk.주어진파일확장자> 를 사용
            user.img_profile.save(file_name, File(temp_file))

            # user_info에 있는 값으로 새 User를 만들어줌
            # User.objects.create(
            # )
        return user


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
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
        )
    # 유저타입. 기본은 Django이며, 페이스북 로그인시 USER_TYPE_FACEBOOK값을 갖도록함
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)
    nickname = models.CharField(max_length=24, null=True, unique=True)
    email = models.EmailField(null=True, unique=True)
    img_profile = CustomImageField(
        upload_to='member/',
        # null=True, # text field가 아닐때에는 blank=True와 동시에 사용하면 안됨
        blank=True,
        # img_profile 이미지가 없을 경우 profile.png 파일이 보이게 CustomImageField를 오버라이드
        # default_static_image='images/profile.png',
        )
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        through_fields=('from_user', 'to_user', 'blocked_user'),
        symmetrical=False,
        )
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username
        # return self.nickname if self.nickname else self.username

    def follow(self, user):
        if not isinstance(user, User):
            raise ValueError('"user argument must <User> class')
        # 해당 user를 follow하는 Relation을 생성한다.
        # 이미 follow 상태일 경우 아무일도 하지 않음

        # self로 주어진 User로 부터 Relation의 from_user에 해당하는 RelatedManager를 사용
        self.follow_relations.get_or_create(to_user=user)

        # Relation 모델의 매니저를 사용
        # Relation.objects.get_or_create(
        #     from_user=self,
        #     to_user=user,
        #     )

    def unfollow(self, user):
        # 위의 반대
        # is_follow = self.follow_relations.get(to_user=user)
        # if not is_follow:
        #     is_follow.delete()
        # return None
        Relation.objects.filter(
            from_user=self,
            to_user=user,
            ).delete()

    def follow_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError('"user argument must <User> class')
        r, t = self.follow_relations.get_or_create(to_user=user)
        if not t:
            r.delete()
        else:
            return r

    def block_toggle(self, user):
        if not isinstance(user, User):
            raise ValueError('"user argument must <User> class')
        if user in self.following:
            self.follow_relations.get(to_user=user).delete()
        r, t = self.follow_relations.get_or_create(blocked_user=user)
        if not t:
            r.delete()
        else:
            return r

    def is_follow(self, user):
        # 해당 user를 내가 follow하고 있는지 bool 반환
        if not isinstance(user, User):
            raise ValueError('"user argument must <User> class')
        return self.follow_relations.filter(to_user=user).exists()

    def is_follower(self, user):
        # 해당 user가 나를 follow하고 있는지 bool
        if not isinstance(user, User):
            raise ValueError('"user argument must <User> class')
        return self.follower_relations.filter(from_user=user).exists()

    @property
    def following(self):
        relations = self.follow_relations.all()
        return User.objects.filter(pk__in=relations.values('to_user'))

    @property
    def followers(self):
        relations = self.follower_relations.all()
        return User.objects.filter(pk__in=relations.values('from_user'))

    @property
    def blocking(self):
        relations = self.follow_relations.all()
        return User.objects.filter(pk__in=relations.values('blocked_user'))


# User._meta.get_field('email')._unique = True


class Relation(models.Model):
    # user who follows
    from_user = models.ForeignKey(User, related_name="follow_relations")
    # user who is followed
    to_user = models.ForeignKey(User, related_name="follower_relations", null=True, blank=True)
    blocked_user = models.ForeignKey(User, related_name="blocked_relations", null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Relation from {} to {}".format(
            self.from_user,
            self.to_user
            )

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
            ('from_user', 'blocked_user'),
            )
