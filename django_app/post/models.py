import re

from django.conf import settings
from django.db import models

# from django.contrib.auth.models import User
from django.urls import reverse

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

    def __str__(self):
        return '{} uploaded {} at {} liked by {}'.format(self.author, self.photo.name, self.created_date,
                                                         self.like_users.all())

    @property
    def like_count(self):
        # 자신을 like하고있는 user수 리턴
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    # migrate 이후에는 필요없음...(이미 없는 테이블)
    # class Meta:
    #     db_table = 'post_post_like_users'

    def __str__(self):
        return '{} liked {} at {}.'.format(self.user, self.post, self.created_date)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    html_content = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    tags = models.ManyToManyField('Tag')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CommentLike',
        related_name='like_comments', )

    # class Meta:
    #     ordering =

    def __str__(self):
        return '{} by {}'.format(self.content, self.author)

    def save(self, *args, **kwargs):
        # if not self.pk:
        #     super().save(*args, **kwargs)
        super().save(*args, **kwargs)
        self.make_html_content_and_add_tags()

    def make_html_content_and_add_tags(self):
        # 해쉬태그를 찾아냄
        p = re.compile(r'(#\w+)')
        tag_name_list = re.findall(p, self.content)
        # 원래 content를 기억한뒤
        ori_content = self.content
        # tag 리스트를 순회하며
        for tag_name in tag_name_list:
            # Tag 객체를 가져오거나 생성. 생성여부는 쓰지않는 변수이므로 _ 처리
            tag, _ = Tag.objects.get_or_create(name=tag_name.replace('#', ''))
            # 기존 content 내용을 변경
            change_tag = '<a href="{url}" class="hash-tag">{tag_name}</a>'.format(
                # 위치 인자로 넘기는 방법
                # url=reverse('post:hashtag_post_list', args=[tag_name.replace('#', '')]),
                # 키워드 인자로 넘기는 방법
                url=reverse('post:hashtag_post_list', kwargs={'tag_name': tag_name.replace('#', '')}),
                tag_name=tag_name)

            ori_content = re.sub(r'{}(?![<\w])'.format(tag_name), change_tag, ori_content, count=1)
            # content에 포함된 tag 목록을 자신의 tags 필드에 추가
            if not self.tags.filter(pk=tag.pk).exists():
                self.tags.add(tag)
        self.html_content = ori_content


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} liked {} at {}.'


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return 'Tag({})'.format(self.name)
