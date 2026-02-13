from django.urls import path

from .views import AgentListView, ChatView

urlpatterns = [
    path("agents", AgentListView.as_view(), name="agent-list"),
    path("agents/", AgentListView.as_view(), name="agent-list-slash"),
    path("chat", ChatView.as_view(), name="chat"),
    path("chat/", ChatView.as_view(), name="chat-slash"),
]
