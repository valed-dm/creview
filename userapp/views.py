from django.contrib.auth.views import LoginView as LoginViewContrib
from django.contrib.auth.views import LogoutView as LogoutViewContrib
from django.views.generic import CreateView

from .forms import AuthForm, RegisterForm
from .models import MyUser


class RegisterView(CreateView):
    model = MyUser
    form_class = RegisterForm
    template_name = "userapp/register_view.html"
    success_url = "/login/"


class LoginView(LoginViewContrib):
    form_class = AuthForm
    template_name = "userapp/login_view.html"
    success_url = "/"


class LogoutView(LogoutViewContrib):
    pass
