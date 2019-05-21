from django.shortcuts import render
from . import models
from users.models import User
from . import forms


def index(request):
    if not request.session.get('is_login', None):
        return render(request, 'msgs/tologin.html')
    user_id = request.session.get('user_id')
    sender = User.objects.get(id=user_id)
    sender_name = sender.username
    context = {
        'sender_name': sender_name,
        'user_id': user_id
    }
    if request.method == 'GET':
        msg_form = forms.MsgForm()
        context['msg_form'] = msg_form
        return render(request, 'msgs/index.html', context)
    if request.method == 'POST':
        msg_form = forms.MsgForm(request.POST)
        if msg_form.is_valid():
            receiver_name = msg_form.cleaned_data.get('receiver')
            msg = msg_form.cleaned_data.get('msg')
            context['msg_form'] = msg_form
            try:
                receiver = User.objects.get(username=receiver_name)
            except User.DoesNotExist:
                context['message'] = '接收者不存在'
                return render(request, 'msgs/index.html', context)

            models.Msgs.objects.create(sender=sender, receiver=receiver, msg=msg)

            msgs_send = models.Msgs.objects.filter(sender=sender)
            context['msgs_send'] = msgs_send
            return render(request, 'msgs/message.html', context)


def my_message_board(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    msgs_receive = models.Msgs.objects.filter(receiver=user)
    context = {'msgs_receive': msgs_receive}
    return render(request, 'msgs/message_board.html', context)


def message_sended(request, user_id):
    sender = User.objects.get(id=user_id)
    msgs_send = models.Msgs.objects.filter(sender=sender)
    context = {'msgs_send': msgs_send}
    return render(request, 'msgs/message.html', context)
