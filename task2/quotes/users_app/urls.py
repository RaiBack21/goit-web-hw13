from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from . import views

app_name = "users_app"

urlpatterns = [
    path("signup/", views.signupuser, name="signup"),
    path("login/", views.loginuser, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset-password/done/",
        PasswordResetDoneView.as_view(template_name="users_app/reset_password_done.html"),
        name="reset_password_done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users_app/reset_password_confirm.html",
            success_url="/users/reset-password/complete/",
        ),
        name="reset_password_confirm",
    ),
    path(
        "reset-password/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users_app/reset_password_complete.html"
        ),
        name="reset_password_complete",
    ),
]
