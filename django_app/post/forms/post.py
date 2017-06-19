from django import forms


from ..models import Post, Comment


class PostForm(forms.ModelForm):
    # 생성자를 조작해서 실제 Post의 photo 필드는 null=True이지만 Form을 사용할때에는 반드시 photo를 입력하게함.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True
    comment = forms.CharField(
        required=False,
        widget=forms.TextInput,
        )

    class Meta:
        model = Post
        fields = (
            'photo',
            'comment',
        )

    def save(self, **kwargs):
        commit = kwargs.get('commit', True)
        # author 키워드인자는 삭제하여 부모 save()에 전달
        author = kwargs.pop('author', None)
        self.instance.author = author
        # 부모 save() 호출
        instance = super().save(**kwargs)
        # # commit(DB에 저장)이며, author가 None인 경우
        # if commit and not (author and author.is_authenticated):
        #     raise ValueError(
        #         'author is required field'
        #         )
        # if commit:

        # commit인수가 True이며 comment필드가 채워져 있을 경우 Comment생성 로직을 진행
        # 해당 comment는 instance의 my_comment 필드를 채워준다.
        #   (이 위에서 super().save()를 실행하기 때문에
        #       현재위치에서는 author나 pk에 대한 검증이 끝난 상태)
        comment_string = self.cleaned_data['comment']
        if commit and comment_string:
            if instance.my_comment:
                instance.my_comment.content = comment_string
                instance.my_comment.save()
            else:
                instance.my_comment = Comment.objects.get_or_create(
            # comment, comment_created = Comment.objects.get_or_create(
                    post=instance,
                    author=author,
                    defaults={'content': comment_string}
                    )
                instance.save()
            # if not comment_string:
            #     comment.content = comment_string
            # # RelateManager를 이용해 Comment 객체 생성 및 저장
            # instance.comment_set.create(
            #     author=instance.author,
            #     content=comment_string,
            #     )

        return instance