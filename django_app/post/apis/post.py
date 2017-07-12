
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import PostSerializer
from ..models import Post, Comment

__all__ = (
    'PostLikeCreateView',
    'PostLikeToggleView',
    )


class PostLikeCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        # comment_content에 request.data의 'comment'에 해당하는값을 할당
        comment_content = self.request.data.get('comment')
        # 'comment'에 값이 왔을 경우, my_comment항목을 채워줌
        if comment_content:
            instance.my_comment = Comment.objects.create(
                    post=instance,
                    author=instance.author,
                    content=comment_content,
            )
            instance.save()


class PostLikeToggleView(APIView):
    def post(self, request, post_pk):
        post_instance = get_object_or_404(Post, pk=post_pk)
        post_like, post_like_created = post_instance.postlike_set.get_or_create(
                user=request.user,
        )
        if not post_like_created:
            post_like.delete()
        return Response({'created': post_like_created})



    # def get(self, request, *args, **kwargs):
    #     # get요청이 왔을 때, Post.objects.all()을
    #     # PostSerailizer 를 통해 Response 로 반환
    #     # DRF API Guide
    #     # - API View
    #     # - Serializers
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request, *args, **kwargs):
    #     # serializer 를 이용해 Post 인스턴스생성
    #     # 'comment'라는값이 request.data에 올경우, 해당 내용으로 Post 인스턴스의 my_comment 항목을 만들어줌
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         # serializer.save()로 생성된 Post instance를 instance변수에 할당
    #         instance = serializer.save(author=request.user)
    #         # comment_content에 request.data의 'comment'에 해당하는값을 할당
    #         comment_content = request.data.get('comment')
    #         # 'comment'에 값이 왔을 경우, my_comment항목을 채워줌
    #         if comment_content:
    #             instance.my_comment = Comment.objects.create(
    #                     post=instance,
    #                     author=instance.author,
    #                     content=comment_content,
    #                     )
    #             instance.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
