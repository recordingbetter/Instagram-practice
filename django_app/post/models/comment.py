import re

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse

from .post import Post
from .others import Tag

__all__ = [
    'Comment',
    'CommentLike',
    ]


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
        # 편집이 완료된 문자열을 html_content에 저장
        self.html_content = ori_content
        super().save(update_fields=['html_content'])


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} liked {} at {}.'
