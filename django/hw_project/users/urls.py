from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView
from .forms import LoginForm
from .views import RegisterView, ResetPasswordView, CustomLogoutView

app_name = "users"

urlpatterns = [
    path("signup/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm,
                                      redirect_authenticated_user=True), name='login'),
    path("logout/", CustomLogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url='/users/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]