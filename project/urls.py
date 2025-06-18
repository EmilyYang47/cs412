

from django.urls import path
from . import views

urlpatterns = [
    path('', views.timer_view, name='timer'), 
    path('/todo_list/', views.ShowAllTaskDescriptionView.as_view(), name='todo_list'), 
]
