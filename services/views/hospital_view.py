import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from address.models import District
from services.models.hospital_models import Hospital, Appointment, AppointmentBill
from users_auth.models import User
from utils.filter import filter_by_address
from utils.print_invoice import render_to_pdf
from django.contrib.auth.mixins import LoginRequiredMixin


class HospitalList(LoginRequiredMixin, View):
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


class HospitalDetailsView(LoginRequiredMixin, View):
    def get(self, request, id):
        hospital_object = get_object_or_404(Hospital, pk=id)
        doctors = hospital_object.doctors.all()
        context = {
            'hospital': hospital_object,
            'doctors': doctors,
        }
        return render(request, 'services/hospital/details.html', context)


class DoctorDetailsView(LoginRequiredMixin, View):
    def get(self, request, doctor_id):
        doctor_obj = get_object_or_404(User, pk=doctor_id)
        expertises = doctor_obj.user_info.expertise.all()
        context = {
            'doctor': doctor_obj,
            'expertises': expertises,
        }
        return render(request, 'services/hospital/doctor_details.html', context)

    def post(self, request, doctor_id):
        doctor_obj = get_object_or_404(User, pk=doctor_id)

        data = request.POST
        appointment_date = data.get('appointment_date')
        appointment_date = datetime.datetime.strptime(appointment_date, '%b %d, %Y %H:%M').strftime('%Y-%m-%d %H:%M')  # 2021-01-09
        problem_desc = data.get('problem_desc')

        appointment = Appointment(doctor=doctor_obj, patient=request.user, date=appointment_date,
                                  description=problem_desc)
        appointment.save()
        messages.success(request, 'Appointment Request Submitted Successfully to Dr. {a}'.format(a=doctor_obj.get_full_name()))
        return redirect('services:user_appointments_url', user_id=request.user.id)


class UserAppointmentView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user_obj = get_object_or_404(User, pk=user_id)

        context = {
            'appointments': Appointment.objects.filter(patient=user_obj)
        }
        return render(request, 'services/hospital/my_appointments.html', context)

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        data = request.POST

        appointment_date = data.get('appointment_date')
        appointment_date = datetime.datetime.strptime(appointment_date, '%b %d, %Y %H:%M').strftime('%Y-%m-%d %H:%M')  # 2021-01-09
        problem_desc = data.get('problem_desc')

        appointment.date = appointment_date
        appointment.description = problem_desc
        appointment.save()

        messages.success(request, "Appointment Updated Successfully. ")
        return redirect('services:user_appointments_url', user_id=request.user.id)


class DeleteAppointmentView(LoginRequiredMixin, View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        appointment.delete()
        messages.success(request, 'Appointment Deleted Successfully. ')
        return redirect('services:user_appointments_url', user_id=request.user.id)


class ManageAppointmentsView(LoginRequiredMixin, View):
    def get(self, request, doctor_id):
        doctor_obj = get_object_or_404(User, pk=doctor_id)
        pending_appointments = Appointment.objects.filter(doctor=doctor_obj, status=1)
        approved_appointments = Appointment.objects.filter(doctor=doctor_obj, status=2)
        on_hold_appointments = Appointment.objects.filter(doctor=doctor_obj, status=4)
        released_appointments = Appointment.objects.filter(doctor=doctor_obj, status=5)
        rejected_appointments = Appointment.objects.filter(doctor=doctor_obj, status=3)
        context = {
            'pending_appointments': pending_appointments,
            'approved_appointments': approved_appointments,
            'on_hold_appointments': on_hold_appointments,
            'released_appointments': released_appointments,
            'rejected_appointments': rejected_appointments,
        }
        return render(request, 'doctors/appointment_manage.html', context)

    def post(self, request, **kwargs):
        if 'approve_id' in kwargs:
            appointment_obj = get_object_or_404(Appointment, pk=kwargs.get('approve_id'))
            data = request.POST
            doctors_note = data.get('doctors_note')
            appointment_obj.status = 2
        if 'reject_id' in kwargs:
            appointment_obj = get_object_or_404(Appointment, pk=kwargs.get('reject_id'))
            doctors_note = request.POST.get('doctors_reject_note')
            appointment_obj.status = 3

        if 'release_id' in kwargs:
            appointment_obj = get_object_or_404(Appointment, pk=kwargs.get('release_id'))
            data = request.POST
            room_charge = data.get('room_charge')
            medicine_charge = data.get('medicine_charge')
            doctors_fee = data.get('doctors_fee')
            others_charge = data.get('others_charge')
            total_bills = data.get('total_bills')
            note = data.get('note')

            appointment_obj.status = 5
            appointment_obj.save()

            bill_obj = AppointmentBill(appointment=appointment_obj, room_charge=room_charge, medicine_charge=medicine_charge,
                                       doctors_charge=doctors_fee, others_charge=others_charge, total_bills=total_bills, notes=note)
            bill_obj.save()
            messages.success(request, 'Patient Released & Bill Generated Successfully. ')
            return redirect('services:manage_appointments_url', doctor_id=request.user.id)

        appointment_obj.doctors_note = doctors_note
        appointment_obj.save()
        return redirect('services:manage_appointments_url', doctor_id=request.user.id)


class DownloadAppointmentInvoice(LoginRequiredMixin, View):
    def get(self, request, appointment_bill_id, *args, **kwargs):
        appointment_obj = get_object_or_404(Appointment, pk=appointment_bill_id)
        invoice_obj = AppointmentBill.objects.get(appointment=appointment_obj)

        context = {
            'invoice_obj': invoice_obj,
        }

        pdf = render_to_pdf('services/hospital/invoice_template.html', context)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (invoice_obj.id)
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response