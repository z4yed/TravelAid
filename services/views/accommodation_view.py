from django.shortcuts import render, get_object_or_404
from django.views import View
from address.models import District, Address
from services.models.accommodation_models import Accommodation, Room
from utils.filter import filter_by_address, filter_room


class AccommodationList(View):
    def get(self, request):
        districts = District.objects.all()
        accommodations = Accommodation.objects.all()
        context = {
            'districts': districts,
            'accommodations': accommodations,
        }
        return render(request, 'services/accommodation/list.html', context)

    def post(self, request):
        data = request.POST
        location = data.get('location')
        district = data.get('district')
        zip_code = data.get('zip_code')

        districts = District.objects.all()
        accommodations = filter_by_address(Accommodation, location, district, zip_code)

        context = {
            'districts': districts,
            'accommodations': accommodations,
        }
        return render(request, 'services/accommodation/list.html', context)


class AccommodationDetailView(View):
    def get(self, request, pk):
        accommodation_obj = get_object_or_404(Accommodation, pk=pk)
        rooms = accommodation_obj.room_set.all()
        available_rooms_count = accommodation_obj.room_set.filter(current_status=1).count()
        booked_rooms_count = accommodation_obj.room_set.filter(current_status=3).count()
        context = {
            'object': accommodation_obj,
            'rooms': rooms,
            'available_rooms': available_rooms_count,
            'booked_rooms': booked_rooms_count,
        }
        return render(request, 'services/accommodation/details.html', context)

    def post(self, request, pk):
        accommodation_obj = get_object_or_404(Accommodation, pk=pk)
        available_rooms_count = accommodation_obj.room_set.filter(current_status=1).count()
        booked_rooms_count = accommodation_obj.room_set.filter(current_status=3).count()

        room_status = request.POST.get('room_status')
        room_type = request.POST.get('room_type')
        cost_per_day = request.POST.get('cost_per_day')

        rooms = filter_room(Room, room_status, room_type, cost_per_day)

        context = {
            'object': accommodation_obj,
            'rooms': rooms,
            'available_rooms': available_rooms_count,
            'booked_rooms': booked_rooms_count,
        }
        return render(request, 'services/accommodation/details.html', context)



class RoomDetailView(View):
    def get(self, request, pk):
        room_obj = get_object_or_404(Room, pk=pk)
        context = {
            'room': room_obj,
        }
        return render(request, 'services/accommodation/room_details.html', context)
