from django.contrib import admin
from .models import Fbuser

# Register your models here.


class FbuserAdmin(admin.ModelAdmin):
    """
    [어드민] 사용자
    """
    list_display = ('username', 'email')


admin.site.register(Fbuser, FbuserAdmin)
