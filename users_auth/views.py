from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.


class LoginView(View):
    def get(self, request):
        return HttpResponse("Login GET")

    def post(self, request):
        pass