from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.index, name="index"),
    path('direct/<username>', views.Directs, name="directs"),
    path('send/', views.SendDirect, name="send-directs"),
    path('delete-message/<int:pk>.', views.deleteMessage, name='delete-message'),
    path("task/", views.task, name="task"),
    path("shead_task/", views.shead_task, name="shead_task"),
    path("emoji_send/", views.emoji_send, name="emoji_send"),
    path("shared_task/", views.shared_task, name="shared_task"),
    path("chat/", views.chat, name="chat"),
    path("calendar/", views.calendar, name="calendar"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('completed/', views.completed, name='completed'),
    path('remaining', views.remaining, name='remaining'),
    # path('add_task', views.add_task, name='add_task'),
    path('detail/<str:task_id>', views.task_detail, name='task_detail'),
    path('toggle_complete/<str:task_id>', views.toggle_complete, name='toggle_complete'),
    path('remove_task/<str:task_id>', views.remove_task, name='remove_task'),
    # path("cha")
]