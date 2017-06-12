from django.db import models
from django.contrib.auth.models import User

'''
member app
    User model
        username, nickname
이후 해당 User 모델을 Post 나 Comment 에서 author 나 user 항목으로 참조할 수 있게
'''


class Post(models.Model):
    author = models.ForeignKey(User)
    photo = models.ImageField(blank = True,
                              upload_to = 'photos/%Y/%m/%d',
                              height_field = 100,
                              width_field = 100,
                              max_length = 100)
    like_users = models.ManyToManyField(User,
                                        through = 'PostLike',
                                        related_name = 'like_posts',
                                        )
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    tags = models.ManyToManyField('Tag')

    def add_comment(self, user, content):
        """
        자신을 post 로 갖고, 전달받은 user 를 author 로 가지며 content 를 content 필드내용으로넣는 Comment 객체 생성
        :param user: Author
        :param content:
        :return:
        """
        return self.comment_set.create(author = user, content = content)
        # return Comment.objects.create(post = self.post, author = user, content = content)

    def add_tag(self, tag_name):
        """
        # tags 에 tag 매개변수로 전달된 str 을 name 으로 갖는 Tag 객체를 (이미 존대하면) 가져오고없으면 생성하여 자신의 tags 에 추가
        :param tag_name:
        :return:
        """
        # tag가 있으면 True, 없으면 False + 객체 생성
        tag, tag_created = Tag.objects.get_or_create(name = tag_name)
        if not self.tags.filter(name = tag_name).exists():
            self.tags.add(tag)

    @property
    def like_count(self):
        # 자신을 like하고있는 user수 리턴
        return self.like_users.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)
    like_users = models.ManyToManyField(
        User,
        through = 'CommentLike',
        related_name = 'like_comments',
    )

    def __str__(self):
        return '{} by {}'.format(self.content, self.author)


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add = True)


class Tag(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return 'Tag({})'.format(self.name)


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add = True)
    # migrate 이후에는 필요없음...(이미 없는 테이블)
    # class Meta:
    #     db_table = 'post_post_like_users'
