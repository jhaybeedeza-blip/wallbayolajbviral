from django.urls import path
from .views import home, search_messages, message_detail, messages_by_song

urlpatterns = [
    path('', home, name='home'),
    path('search/', search_messages, name='search'),
    path('message/<int:pk>/', message_detail, name='message_detail'),
    path('by-song/', messages_by_song, name='messages_by_song'),
]
