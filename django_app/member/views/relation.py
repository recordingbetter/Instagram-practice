from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

User = get_user_model()

__all__ = (
    'follow_toggle_view',
    'block_toggle_view',
    )


@login_required
@require_POST
def follow_toggle_view(request, user_pk):
    next = request.GET.get('next')
    cur_user = User.objects.get(pk=request.user.pk)
    profile_user = get_object_or_404(User, pk=user_pk)
    cur_user.follow_toggle(profile_user)
    if next:
        return redirect(next)
    return redirect('member:profile', user_pk=user_pk)


@login_required
@require_POST
def block_toggle_view(request, user_pk):
    cur_user = User.objects.get(pk=request.user.pk)
    profile_user = User.objects.get(pk=user_pk)
    cur_user.block_toggle(profile_user)
    return redirect('member:profile', user_pk=profile_user.pk)
