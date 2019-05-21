from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path("", views.index, name='index'),                 # 个人信息页面
    path("login/", views.login, name="login"),           # 登录页面
    path("register/", views.register, name="register"),  # 注册页面
    path("logout/", views.logout, name="logout"),        # 退出登录
    path('edit/', views.edit_info, name='edit'),
]
