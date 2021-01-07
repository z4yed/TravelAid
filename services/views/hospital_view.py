from django.shortcuts import render
from django.views import View


class HospitalList(View):
    def get(self, request):
        context = {

        }
        return render(request, 'services/hospital/list.html', context)

