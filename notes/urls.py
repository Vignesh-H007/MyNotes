from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('dashboard/', views.dashboard, name = "dashboard"),
    path('create/', views.create_note, name = "createNotes"),
    path('edit/<int:noteid>/', views.edit_note, name = "editnotes"),
    path('view/<int:noteid>/', views.view_note, name = "viewnote"),
    path('delete/<int:noteid>/', views.delete_note, name = "delete"),
    path('logout/', views.logout, name="logout")
]