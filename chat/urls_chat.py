from django.urls import path
from . import views


app_name = 'chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:friend_id>/', views.chat_whit, name='chat_with'),
    path('add', views.add_friend, name='add'),
    path('send/', views.send_message, name='send'),
]
