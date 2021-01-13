from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import auth, messages

from services.models import Hospital, Appointment, Accommodation, Room, ROOM_TYPE_CHOICES
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
    def get(self, request, doctor_id):
        doctor_obj = get_object_or_404(User, pk=doctor_id)
        pending_appointments = Appointment.objects.filter(doctor=doctor_obj, status=1)
        confirmed_appointments = Appointment.objects.filter(doctor=doctor_obj, status=2)
        rejected_appointments = Appointment.objects.filter(doctor=doctor_obj, status=3)
        total_appointments = Appointment.objects.filter(doctor=doctor_obj)
        context = {
            'pending_appointments': pending_appointments,
            'confirmed_appointments': len(confirmed_appointments),
            'rejected_appointments': len(rejected_appointments),
            'total_appointments': len(total_appointments),
        }
        return render(request, 'dashboard/doctor_dashboard.html', context)


class PoliceDashboardView(View):
    def get(self, request):
        context = {

        }
        return render(request, 'dashboard/police_dashboard.html', context)


class ManagerDashboardView(View):
    def get(self, request, manager_id):
        manager_obj = get_object_or_404(User, pk=manager_id)
        districts = District.objects.all()
        accommodations = Accommodation.objects.filter(owner=manager_obj)
        rooms = Accommodation.objects.none()
        for accommodation in accommodations:
            rooms |= Room.objects.filter(accommodation=accommodation.id)

        context = {
            'districts': districts,
            'accommodations': accommodations,
            'rooms': rooms,
            'room_type': list(ROOM_TYPE_CHOICES),
        }
        return render(request, 'dashboard/manager_dashboard.html', context)


class AccommodationManageView(View):
    def get(self, request, **kwargs):
        if 'deletable_id' in kwargs:
            deletable_obj = get_object_or_404(Accommodation, pk=kwargs.get('deletable_id'))
            deletable_obj.delete()
            messages.success(request, 'Accommodation Deleted Successfully. ')
            return redirect('authenticate:manager_dashboard_url', manager_id=request.user.id)

    def post(self, request, **kwargs):
        data = request.POST

        if 'editable_id' in kwargs:
            accommodation_obj = get_object_or_404(Accommodation, pk=kwargs.get('editable_id'))
            name = data.get('new_name')
            image = request.FILES.get('new_image')
            location = data.get('new_location')
            district = data.get('new_district')
            zip_code = data.get('new_zip_code')
            description = data.get('new_description')

            accommodation_obj.name = name
            if image:
                accommodation_obj.image = image

            # updating address object
            accommodation_obj.address.address = location
            accommodation_obj.address.district = District.objects.get(pk=district)
            accommodation_obj.address.zip_code = zip_code
            accommodation_obj.address.save()

            accommodation_obj.description = description
            accommodation_obj.save()

            messages.success(request, 'Accommodation Updated Successfully,')
            return redirect('authenticate:manager_dashboard_url', manager_id=request.user.id)

        # adding Accommodation, This won't be executed if edit url called
        name = data.get('name')
        image = request.FILES.get('image')
        location = data.get('location')
        district = data.get('district')
        zip_code = data.get('zip_code')
        description = data.get('description')

        # creating address object
        district = get_object_or_404(District, pk=district)
        address_obj = Address(address=location, district=district, zip_code=zip_code)
        address_obj.save()

        accommodation_obj = Accommodation(name=name, owner=request.user, image=image, address=address_obj, description=description)
        accommodation_obj.save()

        messages.success(request, 'Accommodation Added Successfully,')
        return redirect('authenticate:manager_dashboard_url', manager_id=request.user.id)


class RoomManageView(View):
    def get(self, request, **kwargs):
        if 'deletable_id' in kwargs:
            room_obj = get_object_or_404(Room, pk=kwargs.get('deletable_id'))
            room_obj.delete()
            messages.success(request, 'Room Deleted Successfully. ')
            return redirect('authenticate:manager_dashboard_url', manager_id=request.user.id)

    def post(self, request, **kwargs):
        data = request.POST
        room_number = data.get('room_number')
        image = request.FILES.get("room_image")
        accommodation = data.get('accommodation')
        description = data.get('room_description')
        room_type = data.get('room_type')
        cost_per_day = data.get('cost_per_day')

        # In case of updating room
        if 'editable_id' in kwargs:
            room_obj = get_object_or_404(Room, pk=kwargs.get('editable_id'))
            room_obj.room_number = room_number
            if image:
                room_obj.image = image
            room_obj.accommodation = Accommodation.objects.get(pk=accommodation)
            room_obj.description = description
            room_obj.room_type = room_type
            room_obj.cost_per_day = cost_per_day
            room_obj.save()
            messages.success(request, 'Room Updated Successfully. ')
            return redirect('authenticate:manager_dashboard_url', manager_id=request.user.id)

        room_obj = Room(accommodation=Accommodation.objects.get(pk=accommodation), room_type=room_type,
                        room_number=room_number, image=image, description=description, cost_per_day=cost_per_day)
        room_obj.save()
        messages.success(request, 'Room Added Successfully. ')
        return redirect('authenticate:manager_dashboard_url', manager_id=request.user.id)


class LoginView(View):
    def get(self, request):

        context = {

        }
        return render(request, 'users_auth/login.html', context)

    def post(self, request):
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_status != 1:
                auth.login(request, user)
                if user.is_staff:
                    return redirect('authenticate:admin_dashboard_url')
                elif user.is_doctor:
                    return redirect('authenticate:doctor_dashboard_url', doctor_id=user.id)
                elif user.is_police:
                    return redirect('authenticate:police_dashboard_url')
                elif user.is_manager:
                    return redirect('authenticate:manager_dashboard_url', manager_id=user.id)
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


class ProfileView(View):
    def get(self, request, pk):
        profile_obj = get_object_or_404(UserProfile, pk=pk)
        districts = District.objects.all()
        context = {
            'profile': profile_obj,
            'full_name': profile_obj.user.get_full_name(),
            'districts': districts,
            'expertises': Expertise.objects.all(),
            'profile_exp': profile_obj.expertise.all(),
        }
        return render(request, 'users_auth/profile.html', context)

    def post(self, request, pk):
        data = request.POST
        profile_picture = request.FILES.get('profile_picture')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        cell = data.get('cell')
        address = data.get('address')
        district = data.get('district')
        zip_code = data.get('zip_code')
        description = data.get('description')



        profile_obj = get_object_or_404(UserProfile, pk=pk)
        profile_obj.user.first_name = first_name
        profile_obj.user.last_name = last_name
        profile_obj.user.save()

        profile_obj.address.address = address
        profile_obj.address.district = District.objects.get(pk=district)
        profile_obj.address.zip_code = zip_code
        profile_obj.address.save()

        profile_obj.cell = cell
        if profile_picture:
            profile_obj.profile_picture = profile_picture
        profile_obj.description = description
        profile_obj.save()

        if request.user.is_doctor:
            profile_obj.expertise.clear()
            expertises = data.getlist('expertises')
            for exp in expertises:
                obj = Expertise.objects.get(pk=int(exp))
                profile_obj.expertise.add(obj)

        messages.success(request, 'Profile Updated Successfully. ')
        if profile_obj.user.is_doctor:
            return redirect('authenticate:doctor_dashboard_url', doctor_id=profile_obj.user.id)
        if profile_obj.user.is_manager:
            return redirect('authenticate:manager_dashboard_url', manager_id=profile_obj.user.id)

        return redirect('authenticate:profile_url', pk=profile_obj.id)
