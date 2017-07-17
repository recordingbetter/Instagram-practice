from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm1(forms.Form):
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
    email = forms.EmailField(
            widget=forms.EmailInput(
                    attrs={
                        'placeholder': 'Type Email address.',
                    }
            ),
            help_text='이메일은 유일해야 합니다',
            max_length=100,
            required=True,
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists!')
        return email

    # 자신의 cleaned_data를 이용하여 유저 생성
    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        email = self.cleaned_data['email']
        return User.objects.create(
                username=username,
                nickname=nickname,
                password=password,
                email=email,
        )


# UserCreationForm을 사용할 경우
class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'nickname',)

