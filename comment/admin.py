from django.contrib import admin
from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    """
    [어드민] 댓글
    """
    list_display = ('contents',)


admin.site.register(Comment, CommentAdmin)
