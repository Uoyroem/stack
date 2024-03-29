from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from django.views.generic import View, FormView
from .forms import SignupForm, LoginForm
from django.contrib import auth
from django.contrib.auth.views import LoginView


class ProfileView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'profile.html')
    

class UserLoginView(LoginView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

   
class SignupView(FormView):
    form_class = SignupForm
    template_name = 'signup.html'


def register(request: HttpRequest) -> HttpResponse:
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save()
        auth.login(request, user)
        return redirect('index')
    return redirect('signup')


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('signup')
        
