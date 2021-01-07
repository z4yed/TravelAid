from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth, messages

from services.models import Hospital
from system.models import Expertise
from .models import User, UserProfile
from address.models import District, Address

# Create your views here.


class HomeView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'home.html', context)


class AdminDashboardView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/admin_dashboard.html', context)


class DoctorDashboardView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/doctor_dashboard.html', context)


class PoliceDashboardView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/police_dashboard.html', context)


class ManagerDashboardView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/manager_dashboard.html', context)


class LoginView(View):
    def get(self, request):

        context = {

        }
        return render(request, 'users_auth/login.html', context)

    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        print(">>>>>>>>>>>>>>>>..", username, password)

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_status != 1:
                auth.login(request, user)
                if user.is_staff:
                    return redirect('authenticate:admin_dashboard_url')
                elif user.is_doctor:
                    return redirect('authenticate:doctor_dashboard_url')
                elif user.is_police:
                    return redirect('authenticate:police_dashboard_url')
                elif user.is_manager:
                    return redirect('authenticate:manager_dashboard_url')
                else:
                    return redirect('home_url')

            else:
                messages.warning(request, 'Your account is not Approved By Admin Yet. Please Wait. ')
                return redirect('authenticate:login_url')
        else:
            messages.warning(request, "Incorrect Username or Password")
            return redirect('authenticate:login_url')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('home_url')


class RegistrationView(View):
    def get(self, request):
        district = District.objects.all()
        expertises = Expertise.objects.all()
        hospitals = Hospital.objects.all()
        context = {
            'district': district,
            'expertises': expertises,
            'hospitals': hospitals,
        }
        return render(request, 'users_auth/user_register.html', context)

    def post(self, request):
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        contact_number = data.get('contact_number')
        address = data.get('address')
        district = data.get('district')
        zip_code = data.get('zip_code')
        designation = data.get('designation')
        expertises = data.getlist('expertises')
        hospital = data.get('hospital')

        email_taken = User.objects.filter(username=email).exists()
        if email_taken:
            messages.error(request, "This email is already taken. ")
            return redirect('authenticate:registration_url')
        else:
            if password == confirm_password:
                user = User.objects.create_user(username=email, first_name=first_name, last_name=last_name,
                                                password=password, email=email)
                user.save()
                if designation == "manager":
                    user.is_manager = True
                    user.save()
                if designation == "doctor":
                    user.is_doctor = True
                    user.save()
                if designation == "police":
                    user.is_police = True
                    user.save()

                address_obj = Address()
                address_obj.address = address
                address_obj.district = District.objects.get(pk=int(district))
                address_obj.zip_code = zip_code
                address_obj.save()

                userprofile = UserProfile.objects.get(user=user)
                userprofile.full_name = user.get_full_name()
                userprofile.cell = contact_number
                userprofile.address = address_obj
                userprofile.save()

                # if user is doctor, assign expertises & Hospital to the doctor.
                if designation == 'doctor':
                    for value in expertises:
                        exp_obj = Expertise.objects.get(pk=int(value))
                        userprofile.expertise.add(exp_obj)

                    hospital_obj = Hospital.objects.get(pk=hospital)
                    hospital_obj.doctors.add(user)

                messages.success(request, 'Hello, {f_name}. Please Login. '.format(f_name=first_name))
                return redirect('authenticate:login_url')

            else:
                messages.error(request, "Password didn't matched. ")
                return redirect('authenticate:registration_url')
