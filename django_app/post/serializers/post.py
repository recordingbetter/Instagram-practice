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

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'my_comment',
        )
        read_only_fields = (
            'author',
            'my_comment',
        )


