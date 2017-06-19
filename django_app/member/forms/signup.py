from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    username = forms.CharField(
        help_text='Username을 입력하세요.',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type Username.',
                }
            )
        )
    nickname = forms.CharField(
        help_text='Nickname을 입력하세요.',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Type Nickname.',
                }
            )
        )
    password1 = forms.CharField(
        help_text='Password를 입력하세요.',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type Password.',
                }
            )
        )
    password2 = forms.CharField(
        help_text='Password를 다시 입력하세요.',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Type Password again.',
                }
            )
        )

    # clean_<fieldname>매서드를 사용해서 username 필드에 대한 유효성 검증을 실행
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists!')
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('Username already exists!')
        return nickname

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords are not match!')
        return password2

    def create_user(self):
        # 자신의 cleaned_data를 이용하여 유저 생성
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        return User.objects.Create(
            username=username,
            nickname=nickname,
            password=password,
            )