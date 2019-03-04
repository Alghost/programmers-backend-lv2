from django.db import models
from fbuser.models import Fbuser


# Create your models here.


class Post(models.Model):
    """
    Post
    """

    contents = models.CharField(max_length=32,
                                verbose_name='내용')
    writer = models.ForeignKey(Fbuser,
                               on_delete=models.CASCADE,
                               verbose_name='작성자')
    tstamp = models.DateTimeField(auto_now_add=True,
                                  verbose_name='등록시간')

    def __repr__(self):
        return 'Post()'

    def __str__(self):
        return self.contents[:10]

    class Meta:
        db_table = 'programmers_post'
        verbose_name = '게시글'
        verbose_name_plural = '게시글'
