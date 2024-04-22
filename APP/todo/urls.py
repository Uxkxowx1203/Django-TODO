from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.todo_list, name='todo_list'),
    path('detail/<int:todo_id>/', views.todo_detail, name='todo_detail'),
    path('add/', views.add_todo, name='add_todo'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
   
]
