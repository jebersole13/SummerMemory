from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns= [
    path('', include('django.contrib.auth.urls')),   
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),
    path('register/', views.register, name='register'),

    ]