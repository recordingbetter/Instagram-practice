import time
from django.conf import settings
from django.db import models
from post.tasks import task_update_post_like_count
# from .comment import Comment
# from .others import Video

# from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

__all__ = [
    'Post',
    'PostLike',
    ]

'''
member app
    User model
        username, nickname
이후 해당 User 모델을 Post 나 Comment 에서 author 나 user 항목으로 참조할 수 있게
'''


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(blank=True, upload_to='post', )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
        )
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    my_comment = models.OneToOneField(
        'Comment',
        blank=True,
        null=True,
        related_name='+',
        )
    video = models.ForeignKey('Video', null=True, blank=True)
    # 1. 이 Post를 좋아요 한 개수를 저장할 수 있는 필드(like_count)를 생성 -> migration
    # 2. 이 Post에 연결된 PostLike의 개수를 가져와서 해당 필드에 저장하는 메서드 구현
    # post_like_toggle 갯수를 저장하는 필드
    like_counts = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-pk', ]

    def add_comment(self, user, content):
        """
        자신을 post 로 갖고, 전달받은 user 를 author 로 가지며 content 를 content 필드내용으로넣는 Comment 객체 생성
        :param user: Author
        :param content:
        :return:
        """
        return self.comment_set.create(author=user, content=content)
        # return Comment.objects.create(post = self.post, author = user, content = content)

    # def add_tag(self, tag_name):
    #     """
    #     # tags 에 tag 매개변수로 전달된 str 을 name 으로 갖는 Tag 객체를 (이미 존대하면) 가져오고없으면 생성하여 자신의 tags 에 추가
    #     :param tag_name:
    #     :return:
    #     """
    #     # tag가 있으면 True, 없으면 False + 객체 생성
    #     tag, tag_created = Tag.objects.get_or_create(name=tag_name)
    #     if not self.tags.filter(name=tag_name).exists():
    #         self.tags.add(tag)

    # post_like_toggle 갯수를 저장하는 method
    def calc_like_count(self):
        time.sleep(6)
        self.like_counts = self.like_users.count()
        self.save()

    def __str__(self):
        return '{} uploaded {} at {} liked by {}'.format(self.author, self.photo.name, self.created_date,
                                                         self.like_users.all())

    @property
    def like_count(self):
        # 자신을 like하고있는 user수 리턴
        return self.like_users.count()

    @property
    def comments(self):
        if self.my_comment:
            return self.comment_set.exclude(pk=self.my_comment.pk)
        return self.comment_set.all()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    # post와 user가 같은 값이 생기지 않게 함
    class Meta:
        unique_together = (
            ('post', 'user'),
        )
    # migrate 이후에는 필요없음...(이미 없는 테이블)
    # class Meta:
    #     db_table = 'post_post_like_users'

    def __str__(self):
        return '{} liked {} at {}.'.format(self.user, self.post, self.created_date)


@receiver(post_save, sender=PostLike, dispatch_uid='postlike_save_update_like_count')
@receiver(post_delete, sender=PostLike, dispatch_uid='postlike_delete_update_like_count')
def update_post_like_count(sender, instance, **kwargs):
    if kwargs['signal'].receivers[0][0][0] == 'postlike_save_update_like_count':
        instance.post.like_counts += 1
    else:
        instance.post.like_counts -= 1
    instance.post.save()
    print('Signal update_post_like_count, instance: {}'.format(
        instance
    ))
    # instance.post.calc_like_count()
    task_update_post_like_count.delay(post_pk=instance.post.pk)