from django.contrib import admin
from .models import Like

# Register your models here.


class LikeAdmin(admin.ModelAdmin):
    """
    [어드민] 좋아요
    """
    list_display = ('writer',)


admin.site.register(Like, LikeAdmin)
