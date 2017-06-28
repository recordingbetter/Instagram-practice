from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..forms import UserEditForm

User = get_user_model()

__all__ = (
    'profile',
    'profile_edit',
    )


def profile(request, user_pk=None):
    if not request.user.is_authenticated and not user_pk:
        login_url = reverse('member:login')
        return redirect(login_url + "?next=" + request.get_full_path())
    num_posts_per_page = 3
    # 0. urls.py 연결
    # 1. user_pk에 해당하는 User를 cur_user키로 render
    # 2. member/profile.html 작성, 해당 user 정보 보여주기
    #   2-1. 해당 user의 followers, following 목록 보여주기
    # 3. 현재 로그인한 유저가 해당 유저(cur_user)를 팔로우하고있는지 여부 보여주기
    #   3-1. 팔로우하고 있다면 '팔로우해제' 버튼, 아니라면 '팔로우' 버튼 보여주기
    # 4. -> def follow_toggle(request)뷰 생성
    # user = User.objects.get(pk=user_pk)
    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1
    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user
        # posts는 page 번호에 따라 9개씩 전달
        # filter나 order_by에는 안써도 됨
    posts = user.post_set.order_by('-created_date')[: num_posts_per_page * page]
    post_count = user.post_set.count()
    # next
    next_page = page + 1 if post_count > page * num_posts_per_page else page + 1
    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
        }
    return render(request, 'member/profile.html', context)


@login_required
# @require_POST
def profile_edit(request):
    '''
    request.method = 'POST" 일때
    nickname과 img_profile(모델에 필드 추가)을 수정할수있는
    UserEditForm을 구성 (ModelForm 상속) 및 사용
    '''
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=user
            )
        if form.is_valid():
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=user)
    context = {
        'form': form
        }
    return render(request, 'member/profile_edit.html', context=context)
