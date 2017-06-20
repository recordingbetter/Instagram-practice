from django import forms

from ..models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'content',
            ]
        # 튜플로 만들면 수정할 수 없다.
        # ModelForm을 사용하면 속성은 Meta에 따로 지정
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': 'input-comment',
                    'placeholder': '댓글 입력',
                    }
                )
            }


