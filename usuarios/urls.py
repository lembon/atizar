from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout', ),
    path('password_reset/', auth_views.LoginView.as_view(template_name='usuarios/password_reset.html'),
         name='password_reset', ),
]
