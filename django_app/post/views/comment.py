from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# from member.models import User
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMessage
from django.utils.datetime_safe import strftime

from config.settings import DEFAULT_FROM_EMAIL
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
    next_ = request.GET.get('next')
    form = CommentForm(request.POST)
    if form.is_valid():
        # commit=False하면 comment 인스턴스가 튀어나옴
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

        # email 발송
        mail_subject = '{}에 작성한 글에 {}님이 댓글을 작성했습니다.'.format(
                post.created_date.strftime('%Y.%m.%d %H:%M'),
                request.user
        )
        mail_content = '{}님의 댓글\n{}'.format(
                request.user,
                comment.content
        )
        send_mail(
                mail_subject,
                mail_content,
                DEFAULT_FROM_EMAIL,
                [post.author.email],
        )
    else:
        result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
        messages.error(request, result)
    if next_:
        return redirect(next_)
    return redirect('post:post_detail', post_pk=post.pk)


@comment_owner
@login_required
def comment_modify(request, comment_pk):
    next_ = request.GET.get('next')
    # origin_html = request.environ['HTTP_REFERER']
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            form.save()
            if next_:
                return redirect(next_)
            return redirect('post:post_detail', post_pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
        }
    return render(request, 'post/comment_modify.html', context)


@comment_owner
@require_POST
@login_required
def comment_delete(request, comment_pk):
    next_ = request.GET.get('next')
    # POST요청을 받아 Comment객체를 delete, 이후 post_detail페이지로 redirect
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    comment.delete()
    if next_:
        return redirect(next_)
    return redirect('post:post_detail', post_pk=post.pk)
