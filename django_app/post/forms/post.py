from django import forms


from ..models import Post


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
        comment_string = self.cleaned_data['comment']
        if commit and comment_string:
            # RelateManager를 이용해 Comment 객체 생성 및 저장
            instance.comment_set.create(
                author=instance.author,
                content=comment_string,
                )
        return instance