from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # root URL will render index.html
]
