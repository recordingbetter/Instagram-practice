from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from member.models import User
from django.views.decorators.http import require_POST

from ..decorators import comment_owner
from ..forms import CommentForm
from ..models import Post, Comment

# 자동으로 Django에서 인증에 사용하는 User 모델클래스를 불러온다.
#   https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.get_user_model
User = get_user_model()

__all__ = (
    'comment_create',
    'comment_modify',
    'comment_delete',
    )


# POST 요청만 받음
@require_POST
@login_required
def comment_create(request, post_pk):
    # POST요청을 받아 Comment객체를 생성 후 post_detail페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        # Comment.objects.create(
        #     content=form.data['comment_field'],
        #     author=request.user,
        #     post_id=post_pk,
        #     )
        form.save()
    return redirect('post:post_detail', post_pk=post.pk)


@comment_owner
@login_required
def comment_modify(request, comment_pk):
    origin_html = request.environ['HTTP_REFERER']
    # post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(data=request.POST, instance=comment)
        form.save()
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
        }
    return render(request, origin_html, context)


@comment_owner
@login_required
def comment_delete(request, comment_pk):
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect(request.environ['HTTP_REFERER'])
