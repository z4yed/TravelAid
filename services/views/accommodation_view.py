from django.shortcuts import render
from django.views import View
from address.models import District, Address
from services.models.accommodation_models import Accommodation


class AccommodationList(View):
    def get(self, request):
        districts = District.objects.all()
        accommodations = Accommodation.objects.all()
        context = {
            'districts': districts,
            'accommodations': accommodations,
        }
        return render(request, 'services/accommodation/list.html', context)

