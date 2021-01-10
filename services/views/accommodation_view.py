import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from address.models import District, Address
from services.models.accommodation_models import Accommodation, Room, BookAccommodation, AccommodationBillPayment
from utils.filter import filter_by_address, filter_room
from utils.print_invoice import render_to_pdf


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

    def post(self, request, pk):
        room_obj = get_object_or_404(Room, pk=pk)
        from_date = request.POST.get('from_date')  # Jan 9, 2021 [format specified in JS using datepicker ]
        from_date = datetime.datetime.strptime(from_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2021-01-09
        to_date = request.POST.get('to_date')
        to_date = datetime.datetime.strptime(to_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2021-01-09
        total_bills = request.POST.get('total_bills')
        note = request.POST.get('note')

        book_accommodation = BookAccommodation(user=request.user, room=room_obj, start_date=from_date, end_date=to_date,
                                               total_bills=total_bills, note=note)
        book_accommodation.save()
        messages.success(request, 'Booking Request Submitted Successfully. ')
        return redirect('services:bookings_url', user_id=request.user.id)


class BookingsView(View):
    def get(self, request, user_id):
        bookings = BookAccommodation.objects.filter(user=request.user)
        context = {
            'bookings': bookings,
        }
        return render(request, 'services/accommodation/bookings.html', context)


class DownloadInvoice(View):
    def get(self, request, booking_id, *args, **kwargs):
        invoice_obj = get_object_or_404(BookAccommodation, pk=booking_id)

        context = {
            'invoice_obj': invoice_obj,
        }

        pdf = render_to_pdf('services/accommodation/pdf_template.html', context)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (invoice_obj.id)
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


class AccommodationPaymentView(View):
    def post(self, request, booking_id):
        data = request.POST
        booking_id = data.get('booking_id')
        bill_obj = get_object_or_404(BookAccommodation, pk=int(booking_id))
        payment_method = data.get('payment_method')
        account_number = data.get('account_number')
        payment_bdt = data.get('payment_bdt')
        tx_id = data.get('tx_id')
        proof = request.FILES.get('proof')
        note = data.get('note')

        accommodation_bill = AccommodationBillPayment(bill=bill_obj, payment_bdt=payment_bdt, transaction_id=tx_id,
                                                      payment_provider=payment_method, account_number=account_number,
                                                      proof=proof, note=note)
        accommodation_bill.save()
        messages.success(request, 'BDT {a} Payment Successful. '.format(a=payment_bdt))

        bill_obj.paid_bills += float(payment_bdt)
        bill_obj.due_bills = bill_obj.total_bills - bill_obj.paid_bills

        if bill_obj.total_bills == bill_obj.paid_bills:
            bill_obj.payment_status = 'Paid'
        elif 0 < bill_obj.due_bills < bill_obj.total_bills:
            bill_obj.payment_status = 'Partially Paid'
        elif bill_obj.due_bills == bill_obj.total_bills:
            bill_obj.payment_status = 'Unpaid'
        else:
            bill_obj.payment_status = 'Over Paid'
        bill_obj.save()
        return redirect('services:bookings_url', user_id=bill_obj.user.id)



