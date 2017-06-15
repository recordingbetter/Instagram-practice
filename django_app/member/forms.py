from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    # 클래스의 __init__를 재정의(오버라이드) 하기위해 정의(상속받은 클래스를 변경할거)
    def __init__(self, *args, **kwargs):
        # label_suffix 값만 재정의(오버라이드) 한다.
        kwargs.setdefault('label_suffix', '  ')
        # super는 상속받으면서 오버라이드할때 나머지 부모속성을 다시 호출(그대로 사용)
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': '사용자 아이디',
                }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호',
                }
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(
            username=username,
            password=password,
            )
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Login failed.'
                )
