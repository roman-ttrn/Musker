from django.urls import path
from . import views
from chat.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('update_user', views.update_user, name='update_user'),
    path('meep_likes/<int:pk>', views.meep_likes, name='meep-likes'),
    path('meep/<int:pk>', views.meep, name='meep'), 
    path('delete-meep/<int:pk>', views.delete_meep, name='delete-meep'), 
    path('search/', views.search, name='search'),
    path('chats/', chat_list, name='chat_list'),
    path('chats/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('chats/start/<int:user_id>/', start_chat, name='start_chat'),
]
