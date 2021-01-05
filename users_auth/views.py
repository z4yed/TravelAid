from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


class LoginView(View):
    def get(self, request):

        context = {

        }
        return render(request, 'users_auth/login.html', context)

    def post(self, request):
        pass


class Registration(View):
    def get(self, request):
        context = {

        }
        return render(request, 'users_auth/user_register.html', context)