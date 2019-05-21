from django.shortcuts import render, reverse, redirect
from . import models
from . import forms
import hashlib
import random

HOME = 'chat:index'
item_num = -1


def hash_code(s, salt='SecretKey'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def digital_verification():
    num1 = random.randint(0, 33)
    num2 = random.randint(0, 33)
    num3 = random.randint(0, 33)
    # 由于输入是字符串，所以要把数字转换成字符串
    return '%d + %d + %d =' % (num1, num2, num3), '%s' % (num1 + num2 + num3)


def index(request):
    if request.session.get('is_login', None):
        user_id = request.session.get('user_id', None)
        user = models.User.objects.get(id=user_id)
        context = {'user': user}
        return render(request, 'users/index.html', context)
    return render(request, 'users/tologin.html')


def login(request):
    global item_num  # 验证码

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect(reverse('users:index'))

    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            post_num = request.POST.get('post_num')
            context = {'login_form': login_form}
            try:
                user = models.User.objects.get(username=username)
                if user.password == hash_code(password):
                    if post_num == item_num:
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.username
                        request.session.set_expiry(60 * 60 * 12)  # 设置session过期时间为12小时
                        return redirect(reverse(HOME, args=None))
                    else:
                        verification, item_num = digital_verification()
                        context['verification'] = verification
                        context['message'] = '验证码不正确'
                        return render(request, 'users/login.html', context)
                else:
                    verification, item_num = digital_verification()
                    context['verification'] = verification
                    context['message'] = '密码不正确'
                    return render(request, 'users/login.html', context)
            except models.User.DoesNotExist:
                verification, item_num = digital_verification()
                context['verification'] = verification
                context['message'] = '用户不存在'
                return render(request, 'users/login.html', context)
        else:
            login_form = forms.LoginForm()
            context = {
                'login_form': login_form,
                'message': '请检查填写内容'
            }
            return render(request, 'users/login.html', context)
    verification, item_num = digital_verification()
    login_form = forms.LoginForm()
    context = {
        'login_form': login_form,
        'verification': verification,
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            gender = register_form.cleaned_data.get('gender')
            context = {'register_form': register_form}  # 记录之前填过的信息，避免重复填写

            if password1 != password2:
                context['message'] = '两次输入的密码不同！'
                return render(request, 'users/register.html', context)

            if models.User.objects.filter(username=username):
                context['message'] = '用户名已存在！'
                return render(request, 'users/register.html', context)

            if models.User.objects.filter(email=email):
                context['message'] = '邮箱已存在！'
                return render(request, 'users/register.html', context)
            models.User.objects.create(username=username, password=hash_code(password1), email=email, gender=gender)
            return redirect(reverse('users:login'))
        else:
            register_form = forms.RegisterForm()
            context = {
                'register_form': register_form,
                'message': '输入不合法，请检查填写内容！'
            }
            return render(request, 'users/register.html', context)
    register_form = forms.RegisterForm()  # 如果请求方式不是post，则显示空表单
    context = {'register_form': register_form}
    return render(request, 'users/register.html', context)


def logout(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('users:login'))
    request.session.flush()  # 删除当前的会话数据和会话cookie
    return redirect(reverse('users:login'))


def edit_info(request):
    if not request.session.get('is_login', None):
        return redirect(reverse('users:login'))
    my_id = request.session.get('user_id', None)
    user = models.User.objects.get(id=my_id)
    context = {'user': user}
    if request.method == 'GET':
        return render(request, 'users/edit_info.html', context)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        if username != user.username:
            if models.User.objects.filter(username=username):
                context['message'] = '用户名已存在！'
                return render(request, 'users/edit_info.html', context)
            else:
                user.username = username
        if email != user.email:
            if models.User.objects.filter(email=email):
                context['message'] = '该邮箱已被绑定！'
                return render(request, 'users/edit_info.html', context)
            else:
                user.email = email
        if hash_code(password) != user.password:
            user.password = hash_code(password)
        if gender != user.gender:
            user.gender = gender
        user.save()
        return redirect(reverse('users:index'))
