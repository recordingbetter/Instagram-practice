from django import forms


from ..models import Post


class PostForm(forms.ModelForm):
    # 생성자를 조작해서 실제 Post의 photo 필드는 null=True이지만 Form을 사용할때에는 반드시 photo를 입력하게함.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True
    comment = forms.CharField(
        widget=forms.TextInput,
        )

    class Meta:
        model = Post
        fields = (
            'photo',
        )
