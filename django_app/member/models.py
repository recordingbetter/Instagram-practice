# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
# from utils.fields import CustomImageField


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
    img_profile = models.CustomImageField(upload_to='member/', null=True, blank=True)
    relations = models.ManyToManyField(
        'self',
        through='Relation',
        through_fields=('from_user', 'to_user', 'blocked_user'),
        symmetrical=False,
        )

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

