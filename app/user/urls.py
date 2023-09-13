"""
URL Mapping
"""
from django.urls import path, include
from user import views

# reverse(user:create)
app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
]
