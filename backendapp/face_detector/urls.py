from django.urls import path
from . import views

urlpatterns = [
    path('hellodjango/', views.hello_django, name = 'hellodjango'),
    path('face_detect/', views.detect, name = 'face_detect')
]
