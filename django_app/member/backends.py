from django.contrib.auth import get_user_model

from config import settings

User = get_user_model()


# 이전 버전에서는 인증이 필요했으나 현재 버전은 필요없음
class FacebookBackend:
    def authenticate(self, request, facebook_id):
        username = '{}_{}_{}'.format(
            User.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            facebook_id,
            )
        try:
            user = User.objects.get(
                user_type=User.USER_TYPE_FACEBOOK,
                username=username,
                )
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
