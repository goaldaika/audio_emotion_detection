from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('emotion_recognition/', include('emotion_recognition.urls')),
]
