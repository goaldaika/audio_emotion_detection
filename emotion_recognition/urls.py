from django.urls import path
from . import views

urlpatterns = [
    path('', views.emotion_recognition, name='emotion_recognition'),
]
