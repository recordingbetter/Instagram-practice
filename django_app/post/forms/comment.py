from django import forms

from ..models import Comment


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content.required = True

    class Meta:
        model = Comment
        fields = ('content',)

