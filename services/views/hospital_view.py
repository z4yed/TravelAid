import datetime

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from address.models import District
from services.models.hospital_models import Hospital, Appointment
from users_auth.models import User
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
        doctors = hospital_object.doctors.all()
        context = {
            'hospital': hospital_object,
            'doctors': doctors,
        }
        return render(request, 'services/hospital/details.html', context)


class DoctorDetailsView(View):
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
        appointment_date = datetime.datetime.strptime(appointment_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2021-01-09

        problem_desc = data.get('problem_desc')

        appointment = Appointment(doctor=doctor_obj, patient=request.user, date=appointment_date,
                                  description=problem_desc)
        appointment.save()
        messages.success(request, 'Appointment Request Submitted Successfully to Dr. {a}'.format(a=doctor_obj.get_full_name()))
        return redirect('services:user_appointments_url', user_id=request.user.id)


class UserAppointmentView(View):
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
        appointment_date = datetime.datetime.strptime(appointment_date, '%b %d, %Y').strftime('%Y-%m-%d')  # 2021-01-09
        problem_desc = data.get('problem_desc')

        appointment.date = appointment_date
        appointment.description = problem_desc
        appointment.save()

        messages.success(request, "Appointment Updated Successfully. ")
        return redirect('services:user_appointments_url', user_id=request.user.id)


class DeleteAppointmentView(View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        appointment.delete()
        messages.success(request, 'Appointment Deleted Successfully. ')
        return redirect('services:user_appointments_url', user_id=request.user.id)
