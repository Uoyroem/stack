from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.generic import View


class ProfileView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('login')
        return render(request, 'profile.html')
