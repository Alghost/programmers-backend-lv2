from django.contrib import admin
from .models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    """
    [어드민] 게시글
    """
    list_display = ('contents',)


admin.site.register(Post, PostAdmin)
