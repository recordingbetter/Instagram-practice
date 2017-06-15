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

    # is_valid를 실행했을 때, Form내부의 모든 field들에 대한
    # 유효성 검증을 실행하는 메서드
    def clean(self):
        # clean()메서드를 실행한 기본결과 dict를 가져옴
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        # username, password를 이용해 사용자 authenticate
        user = authenticate(
            username=username,
            password=password,
            )
        # 인증에 성공할 경우, Form의 cleaned_data의 'user'
        # 키에 인증된 User객체를 할당
        if user is not None:
            self.cleaned_data['user'] = user
        # 인증에 실패한 경우, is_valid()를 통과하지 못하도록
        # ValidationError를 발생시킴
        else:
            raise forms.ValidationError(
                'Login failed.'
                )
        return self.cleaned_data
