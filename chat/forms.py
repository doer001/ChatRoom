from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(label='请输入消息', max_length=200,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入您要发送的消息'}))
