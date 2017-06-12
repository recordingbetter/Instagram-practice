from django.contrib import admin

# Post에 대한 ModelAdmin을 만들고, register 이후/admin에 가서 Post 확인하고 사진첨부
from .models import Post


class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)

