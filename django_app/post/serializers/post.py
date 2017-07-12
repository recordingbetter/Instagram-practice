from rest_framework import serializers

from member.serializer import UserSerializer
from ..serializers.comment import CommentSerializer
from ..models import Post

__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    my_comment = CommentSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'my_comment',
            'comments',
        )
        read_only_fields = (
            'author',
            'my_comment',
        )

    # 마지막 결과에 뭔가 추가하고 싶을때
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['is_like'] = self.context['request'].user in instance.like_users.all()
        return ret
