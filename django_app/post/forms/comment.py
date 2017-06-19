from django import forms

from ..models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.data['comment_field'].required = True

