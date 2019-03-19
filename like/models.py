from django.db import models
from fbuser.models import Fbuser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


# Create your models here.


class Like(models.Model):
    """
    Like
    """
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    parent = fields.GenericForeignKey('content_type', 'object_id')

    writer = models.ForeignKey(Fbuser,
                               on_delete=models.CASCADE,
                               verbose_name='작성자')
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    def __repr__(self):
        return 'Like()'

    def __str__(self):
        return '({}) => {} [{}]'.format(self.writer, self.content_type, self.object_id)

    class Meta:
        db_table = 'programmers_like'
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'
