from rest_framework import serializers

from ..models import User

__all__ = (
    'UserSerializer',
    'UserCreationSerializer'
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'nickname',
            'img_profile',
            )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'password1',
            'password2',
            'ori_password',
            'nickname',
            'img_profile',
            )
        read_only_fields = (
            'username',
            )


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(max_length=100)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exist.')
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def save(self, *args, **kwargs):
        username = self.validated_data.get('username')
        password = self.validated_data.get('password1')
        nickname = self.validated_data.get('nickname')
        user = User.objects.create_user(
                username=username,
                password=password,
                nickname=nickname,
                )
        return user