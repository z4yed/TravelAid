from django.shortcuts import render, get_object_or_404
from django.views import View

from address.models import District
from services.models.hospital_models import Hospital
from utils.filter import filter_by_address


class HospitalList(View):
    def get(self, request):
        districts = District.objects.all()
        hospitals = Hospital.objects.all()
        context = {
            'districts': districts,
            'hospitals': hospitals,
        }
        return render(request, 'services/hospital/list.html', context)

    def post(self, request):
        data = request.POST
        location = data.get('location')
        district = data.get('district')
        zip_code = data.get('zip_code')

        districts = District.objects.all()
        hospitals = filter_by_address(Hospital, location, district, zip_code)

        context = {
            'districts': districts,
            'hospitals': hospitals,
        }
        return render(request, 'services/hospital/list.html', context)


class HospitalDetailsView(View):
    def get(self, request, id):
        hospital_object = get_object_or_404(Hospital, pk=id)
        context = {
            'hospital': hospital_object,
        }
        return render(request, 'services/hospital/details.html', context)
