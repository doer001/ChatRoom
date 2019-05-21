from django.shortcuts import render, redirect, reverse
from users.models import User
from . import models
from users import user_decorator


my_id = -1
friends = None
friend = None
context = None
MSG_NUM = 15


@user_decorator.login
def index(request):
    global my_id
    global friends
    global context
    if request.session.get('is_login', None):
        context = {}  # 刚进聊天室，应该什么都不传
        my_id = request.session.get('user_id')  # 当前用户的ID，并保存为公用
        friends = User.objects.filter(friends__id=my_id)  # 当前用户的所有好友，并保存为公用
        friends = friends.order_by('id')
        context['friends'] = friends  # 传好友列表，并保存为公用
        return render(request, 'chat/index.html', context)
    return render(request, 'chat/tologin.html')


@user_decorator.login
def chat_whit(request, friend_id):
    global friend
    global my_id
    global context
    if my_id == -1:
        my_id = request.session.get('user_id')
    current_user = User.objects.get(id=my_id)  # 当前用户
    if request.method == 'GET':  # 选择好友
        friend = User.objects.get(id=friend_id)  # 当前好友
        chat_records = models.ChatRecord.objects.filter(sender__id__in=[my_id, friend_id],
                                                        receiver__id__in=[my_id, friend_id]).order_by('send_time')
        end = chat_records.count()
        start = 0
        if end > MSG_NUM:
            start = end - MSG_NUM
        chat_records = chat_records[start:end]
        context['friend'] = friend  # 传入当前好友
        context['chat_records'] = chat_records  # 传入与当前好友的聊天记录
        return render(request, 'chat/index.html', context)
    if request.method == 'POST':  # 发送消息
        message = request.POST.get('message')  # 获得的消息
        models.ChatRecord.objects.create(sender=current_user, receiver=friend, msg=message)  # 保存记录到数据库
        chat_records = models.ChatRecord.objects.filter(sender__id__in=[my_id, friend_id],
                                                        receiver__id__in=[friend_id, my_id]).order_by('send_time')
        end = chat_records.count()
        start = 0
        if end > MSG_NUM:
            start = end - MSG_NUM
        chat_records = chat_records[start:end]
        context['chat_records'] = chat_records  # 传入聊天记录
        return render(request, 'chat/index.html', context)


@user_decorator.login
def add_friend(request):
    if request.method == 'POST':
        pal_name = request.POST.get('pal_name')
        try:
            pal = User.objects.get(username=pal_name)
            myself = User.objects.get(id=my_id)
            myself.friends.add(pal)
            return redirect(reverse('chat:index'))
        except User.DoesNotExist:
            message = '该用户不存在'
            context['message'] = message
            return render(request, 'chat/index.html', context)


def send_message(request):
    global friend
    current_user = User.objects.get(id=request.session['my_id'])
    msg = request.POST.get('message')
    models.ChatRecord.objects.create(sender=current_user, receiver=friend, msg=msg)
