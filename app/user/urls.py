"""
URL Mapping
"""
from django.urls import path
from user import views
from rest_framework import generics
# reverse(user:create)
app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
