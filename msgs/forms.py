from django import forms


class MsgForm(forms.Form):
    receiver = forms.CharField(label='接收者', max_length=8,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入接收者'}))
    msg = forms.CharField(label='留言内容', max_length=200, min_length=1,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入消息内容'}))
