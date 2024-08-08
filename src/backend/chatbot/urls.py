
from django.urls import path, include

from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("save_chat", views.save_chat_to_history, name="save_chat"),
    path("modify", views.modify_user_configuration, name="modify"),
    path("search_chat/<str:openid>/<int:year>/<int:month>/<int:day>", views.search_chat_history_date, name="search_chat_Date"),
    path("chat_history", views.get_chat_history, name="chat_history"),
    path("clear_chat", views.clear_chat_history, name="clear_chat"),
    path("get_response", views.generate_response, name="get_response"),
    path("database", views.generate_database_response, name="generate_database_response"),
    path("audio2text",views.generate_text_from_audio,name='generate_text_from_audio_text'),
]
