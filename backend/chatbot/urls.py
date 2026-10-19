from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_page, name='page'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/history/', views.chat_history_api, name='history_api'),
    path('api/clear/', views.clear_chat_api, name='clear_api'),
]
