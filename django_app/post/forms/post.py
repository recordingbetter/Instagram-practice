from django import forms


from ..models import Post


class PostForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.TextInput,
        )

    class Meta:
        model = Post
        fields = (
            'photo',
        )
