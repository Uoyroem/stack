from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import View, FormView
from .forms import SignupForm
from django.contrib import auth


class ProfileView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'profile.html')
    
    
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
        
