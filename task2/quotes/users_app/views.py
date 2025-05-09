from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes_app:main")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes_app:main")
        else:
            return render(request, "users_app/signup.html", context={"form": form})

    return render(request, "users_app/signup.html", context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to="quotes_app:main")

    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user is None:
            messages.error(request, "Username or password didn't match")
            return redirect(to="users_app:login")

        login(request, user)
        return redirect(to="quotes_app:main")

    return render(request, "users_app/login.html", context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to="quotes_app:main")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users_app/reset_password.html'
    email_template_name = 'users_app/reset_password_email.html'
    html_email_template_name = 'users_app/reset_password_email.html'
    success_url = reverse_lazy('users_app:reset_password_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users_app/reset_password_subject.txt'
