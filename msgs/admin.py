from django.contrib import admin
from . import models


@admin.register(models.Msgs)
class MsgAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'send_time', 'msg']
