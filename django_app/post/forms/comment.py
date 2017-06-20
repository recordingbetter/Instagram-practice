from django import forms
from django.core.exceptions import ValidationError

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

    # comment를 최소 3자 이상 적게하기위해 clean을 재정의
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 3:
            raise ValidationError(
                '댓글은 최소 3자 이상이어야 합니다.'
                )
        return content
