from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_process_image, name='upload'),
    path('result/', views.result, name='result'),
]