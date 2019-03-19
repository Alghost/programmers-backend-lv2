from django.db import models
from fbuser.models import Fbuser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


# Create your models here.


class Comment(models.Model):
    """
    Comment
    """
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent = fields.GenericForeignKey('content_type', 'object_id')

    contents = models.CharField(max_length=32,
                                verbose_name='내용')
    writer = models.ForeignKey(Fbuser,
                               on_delete=models.CASCADE,
                               verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    def __repr__(self):
        return 'Comment()'

    def __str__(self):
        return self.contents[:10]

    class Meta:
        db_table = 'programmers_comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
