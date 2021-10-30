from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout', ),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset.html',
                                              email_template_name='usuarios/password_reset_email.html'),
         name='password_reset', ),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'),
         name='password_reset_done', ),
    path('password_reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'),
         name='password_reset_confirm', ),
    path('password_reset/complete/',
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_complete.html'),
         name='password_reset_complete', ),
]
