from django.urls import path, re_path

from .views import ToDoListCreateView, ToDoDeleteView, ToDoMarkCompleteView

urlpatterns = [
    path("/<int:id>", ToDoDeleteView.as_view()),
    path("/mark_complete/<int:id>", ToDoMarkCompleteView.as_view()),
    path("", ToDoListCreateView.as_view()),
]
