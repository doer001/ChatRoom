from django.urls import path
from . import views

app_name = 'msgs'
urlpatterns = [
    path('', views.index, name='index'),
    path('msgboard/', views.my_message_board, name='msgboard'),
    path('<int:user_id>/', views.message_sended, name='message_sended'),
]
