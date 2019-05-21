from django.db import models


class ChatRecord(models.Model):
    msg = models.TextField(verbose_name='信息')
    sender = models.ForeignKey('users.User', on_delete=models.SET_DEFAULT, default=True, related_name='sender',
                               verbose_name='发送方')
    receiver = models.ForeignKey('users.User', on_delete=models.SET_DEFAULT, default=True, related_name='receiver',
                                 verbose_name='接收方')
    send_time = models.DateTimeField(verbose_name='发送时间', auto_now_add=True)
