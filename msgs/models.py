from django.db import models


class Msgs(models.Model):
    sender = models.ForeignKey('users.User', related_name='msgs_sender', on_delete=models.DO_NOTHING,
                               verbose_name='发送者')
    receiver = models.ForeignKey('users.User', related_name='msgs_receiver', on_delete=models.DO_NOTHING,
                                 verbose_name='接收者')
    send_time = models.DateTimeField(verbose_name='发送时间', auto_now_add=True)
    msg = models.CharField(verbose_name='消息', max_length=200)

