from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms, models
from django.contrib.auth.forms import UserChangeForm
from .models import Doctor, UserProfile, Medicine, Patient,Compounder, Appointment, Prescription
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import MedicineForm, CompounderForm, PatientForm,PatientUserForm, AppointmentForm
from django.contrib.auth.models import Group
from django.http import Http404
from django.contrib import messages
from .forms import DoctorForm  # Assuming you have a DoctorForm defined
from django.contrib.auth import logout
from .forms import PrescriptionForm,CompounderUserForm
from datetime import date



def doctor_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request,'Logout success')
        return redirect('/')
    else:
        messages.info(request,'Please login first')
        return redirect('/')



# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')



def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_compounder(user):
    return user.groups.filter(name='COMPOUNDER').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin-dashboard')
        elif is_doctor(request.user):
            accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
            if accountapproval:
                return redirect('doctor-dashboard')
            else:
                return render(request,'hospital/doctor_wait_for_approval.html')
        elif is_patient(request.user):
            accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
            if accountapproval:
                return redirect('patient-dashboard')
            else:
                return render(request,'hospital/patient_wait_for_approval.html')
        elif is_compounder(request.user):
                return redirect('com-dashboard')
        else:
            messages = "User does not exist or invalid username/password"
        
        return render(request, 'hospital/doctorlogin.html', {'messages': messages})
    else:
        messages.info(request,'Please login first')
        return redirect('/')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True).order_by('-id')
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    patients=models.Patient.objects.all().filter(status=True).order_by('-id')
    patientscount=models.Patient.objects.all().filter(status=True).count()
    mydict={
    'doctors':doctors,
    'doctorcount':doctorcount,
    'patients':patients,
    'patientscount':patientscount
    }
    return render(request,'hospital/admin_doctor.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_compounder_view(request):
    compounder=models.Compounder.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_compounder.html',{'compounder':compounder})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_medicine_view(request):
    medicines = Medicine.objects.all()
    return render(request,'hospital/admin_view_medicine.html',{'medicines':medicines})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk,redirect_to=None):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    dtype = request.GET.get('delete_doctor')
    if dtype == 'from_dash':
        user.delete()
        doctor.delete()
        return redirect('admin-doctor')
    elif dtype=='from_view':
        user.delete()
        doctor.delete()
        return redirect('admin-view-doctor')
    else:
        return redirect('admin-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def update_medicine_view(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    print(medicine)
    if request.method == 'POST':
        medicine.name= request.POST.get('name')
        medicine.description = request.POST.get('description')
        medicine.save()
        return redirect('doctor-medicine')  
    return render(request, 'hospital/update_medicine.html', {'medicine': medicine})




@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def update_medicine_com_view(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    print(medicine)
    if request.method == 'POST':
        medicine.name= request.POST.get('name')
        medicine.description = request.POST.get('description')
        medicine.save()
        return redirect('com-medicine') 
    return render(request, 'hospital/com_update_medicine.html', {'medicine': medicine})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def update_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        
        appointment_date = datetime.strptime(request.POST.get('appointmentDate'), '%Y-%m-%d')
        appointment_time = request.POST.get('appointmentTime')
        appointment.appointmentDate = appointment_date
        appointment.appointmentTime = appointment_time
        appointment.description = request.POST.get('description')
        appointment.a_note = request.POST.get('note')
        appointment.save()
        return redirect('doctor-appointment')  # Redirect to doctor's dashboard after update
    
    return render(request, 'hospital/update_appointment.html', {'appointment': appointment})


@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_update_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        
        appointment_date = datetime.strptime(request.POST.get('appointmentDate'), '%Y-%m-%d')
        appointment_time = request.POST.get('appointmentTime')
        appointment.appointmentDate = appointment_date
        appointment.appointmentTime = appointment_time
        appointment.description = request.POST.get('description')
        appointment.a_note = request.POST.get('note')
        appointment.save()
        return redirect('com-appointment')  # Redirect to doctor's dashboard after update
    
    return render(request, 'hospital/com_update_appointment.html', {'appointment': appointment})







@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_medicine_from_doctor_view(request, pk):
    medicine = get_object_or_404(Medicine, id=pk)
    dtype = request.POST.get('delete_doctor')
    if dtype == 'from_dash':
        medicine.delete()
        return redirect('doctor-medicine')
    elif dtype=='from_view':
        medicine.delete()
        return redirect('doctor-view-medicine')
    elif dtype=='from_dash1':
        medicine.delete()
        return redirect('doctor-dashboard')
    else:
        return redirect('doctor-medicine')




@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def delete_medicine_from_com_view(request, pk):
    medicine = get_object_or_404(Medicine, id=pk)
    dtype = request.POST.get('delete_medicine')
    if dtype == 'from_dash':
        medicine.delete()
        return redirect('com-medicine')
    elif dtype=='from_view':
        medicine.delete()
        return redirect('com-view-medicine')
    elif dtype=='from_dash1':
        medicine.delete()
        return redirect('com-dashboard')
    else:
        return redirect('com-medicine')




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_compounder_from_doctor_view(request, pk):
    compounder = get_object_or_404(Compounder, id=pk)
    dtype = request.POST.get('delete_compounder')
    if dtype == 'from_dash':
        compounder.delete()
        return redirect('doctor-compounder')
    elif dtype=='from_view':
        compounder.delete()
        return redirect('doctor-view-compounder')
    else:
        return redirect('doctor-compounder')



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_patient_from_doctor_view(request, pk):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=pk)
        dtype = request.POST.get('delete_patient')
        if dtype == 'from_dash':
            patient.delete()
            return redirect('doctor-patient')
        elif dtype=='from_view':
            patient.delete()
            return redirect('doctor-view-patient')
        elif dtype=='from_dash1':
            patient.delete()
            return redirect('doctor-dashboard')
        else:
            return redirect('doctor-patient')




@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def delete_prescription_from_com_view(request, pk):
    if request.method == 'POST':
        prescription = get_object_or_404(Prescription, id=pk)
        dtype = request.POST.get('delete_prescription')
        if dtype == 'from_dash':
            prescription.delete()
            return redirect('com-prescription')
        elif dtype=='from_view':
            prescription.delete()
            return redirect('com-view-prescription')
        elif dtype=='from_dash1':
            prescription.delete()
            return redirect('com-dashboard')
        else:
            return redirect('com-prescription')




@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def delete_patient_from_com_view(request, pk):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=pk)
        delete_type = request.POST.get('delete_patient')
        if delete_type == 'from_dash':
            patient.delete()
            return redirect('com-patient')
        elif delete_type == 'from_view':
            patient.delete()
            return redirect('com-view-patient')
    # If the request method is not POST or delete type is invalid, redirect to an appropriate page
    return redirect('com-patient')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            UserProfile.objects.create(user=user, role='doctor')
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group, created = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group.user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            UserProfile.objects.create(user=user, role='doctor')
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group, created = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group.user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_compounder_view(request):
    userForm = CompounderUserForm()  
    compounderForm = CompounderForm()  
    mydict = {'userForm': userForm, 'compounderForm': compounderForm}
    
    if request.method == 'POST':
        userForm = CompounderUserForm(request.POST)
        compounderForm = CompounderForm(request.POST, request.FILES)
        
        if userForm.is_valid() and compounderForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            
            UserProfile.objects.create(user=user, role='compounder')
            
            compounder = compounderForm.save(commit=False)
            compounder.user = user
            compounder.status = True
            compounder.save()

            my_compounder_group, created = Group.objects.get_or_create(name='COMPOUNDER')
            my_compounder_group.user_set.add(user)

            return HttpResponseRedirect('admin-view-compounder')

    return render(request, 'hospital/admin_add_compounder.html', context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_medicine_view(request):
    medicineForm = MedicineForm()
    mydict = {'medicineForm': medicineForm}
    
    if request.method == 'POST':
        medicineForm = MedicineForm(request.POST)
        
        if medicineForm.is_valid():
            medicine = medicineForm.save()
            return HttpResponseRedirect('admin-view-medicine')

    return render(request, 'hospital/admin_add_medicine.html', context=mydict)




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_patient_view(request):
    if request.method == 'POST':
        patientForm = PatientForm(request.POST)
        if patientForm.is_valid():
            patient = patientForm.save(commit=False)
            patient.doctor = Doctor.objects.get(user=request.user)
            patient.save()

            return HttpResponseRedirect('doctor-patient')  # Redirect after successful submission
    else:
        patientForm = PatientForm()
        
    return render(request, 'hospital/doctor_add_patient.html', {'patientForm': patientForm})



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_add_patient_view(request):
    if request.method == 'POST':
        patientForm = PatientForm(request.POST)
        if patientForm.is_valid():
            patient = patientForm.save(commit=False)
            compounder_username = request.user.username
            compounder = Compounder.objects.get(username=compounder_username)
            patient.compounder = compounder
            patient.save()

            return HttpResponseRedirect('com-patient')  # Redirect after successful submission
    else:
        patientForm = PatientForm()
        
    return render(request, 'hospital/com_add_patient.html', {'patientForm': patientForm})




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_appointment_view(request):
    doctor = Doctor.objects.filter(user = request.user)
    patients = Patient.objects.all()
    if request.method == 'POST':
        appointmentForm = AppointmentForm(request.POST)
        if not doctor.exists():
            messages.error(request,'Doctor does not exist!')
        print(appointmentForm.is_valid())
        print(appointmentForm.errors)
        if appointmentForm.is_valid():
            obj = appointmentForm.save(commit=False)
            obj.doctor = doctor.first()
            obj.save()
            return HttpResponseRedirect('doctor-appointment')  # Redirect after successful submission
    else:
        appointmentForm = AppointmentForm()
        
    return render(request, 'hospital/doctor_add_appointment.html', {'appointmentForm': appointmentForm,'patients':patients})



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_add_appointment_view(request):
    patients = Patient.objects.all()
    if request.method == 'POST':
        appointmentForm = AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            compounder_username = request.user.username
            compounder = Compounder.objects.get(username=compounder_username)
            appointment.compounder = compounder
            appointment.save()

            return HttpResponseRedirect('com-appointment')  # Redirect after successful submission
    else:
        appointmentForm = AppointmentForm()
        
    return render(request, 'hospital/com_add_appointment.html', {'appointmentForm': appointmentForm, 'patients':patients})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def update_patient_view_doctor(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    ch = [i[0] for i in Patient.SYMPTOM_CHOICES]

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient information updated successfully.')
            return redirect('doctor-patient')  # Redirect to the desired URL after successful update
        else:
            messages.error(request, 'Failed to update patient information. Please correct the errors below.')
    else:
        form = PatientForm(instance=patient)

    mydict = {'form': form, 'ch': ch, 'patient': patient}
    return render(request, 'hospital/doctor_update_patient.html', context=mydict)




@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def update_patient_view_com(request, patient_id):
    # Retrieve the patient object
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        # Populate the form with the patient's current data
        patientForm = PatientForm(request.POST, instance=patient)
        if patientForm.is_valid():
            # Save the updated patient data
            patientForm.save()
            return HttpResponseRedirect(reverse('com-patient'))  # Redirect to compounder dashboard
    else:
        # Populate the form with the patient's current data
        patientForm = PatientForm(instance=patient)
        
    return render(request, 'hospital/com_update_patient.html', {'patientForm': patientForm, 'patient': patient})





@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def update_prescription_view_com(request, prescription_id):
    # Retrieve the prescription object
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    if request.method == 'POST':
        # Populate the form with the prescription's current data
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            # Save the updated prescription data
            form.save()
            return redirect('com-prescription')  # Redirect to compounder prescription page
    else:
        # Populate the form with the prescription's current data
        form = PrescriptionForm(instance=prescription)
        
    return render(request, 'hospital/com_update_prescription.html', {'form': form, 'prescription': prescription})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def update_compounder_view_doctor(request, pk):
    compounder = get_object_or_404(Compounder, id=pk)
    

    # userForm = UserChangeForm(request.POST or None, instance=request.user)  # Using Django's built-in UserChangeForm
    compounderForm = CompounderForm(request.POST or None, instance=compounder)
    if request.method == 'POST':
        compounder.first_name = request.POST.get('first_name')
        compounder.last_name = request.POST.get('last_name')
        compounder.address = request.POST.get('address')
        compounder.mobile = request.POST.get('mobile')
        compounder.save()
        return redirect('doctor-compounder')

    context = {'compounder': compounder,}
    return render(request, 'hospital/doctor_update_compounder.html', context)


from django.shortcuts import render

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_medicine_view(request):
    error_message = None  # Initialize error_message variable
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST)
        if medicine_form.is_valid():
            medicine_name = medicine_form.cleaned_data['name']
            
            # Check if the medicine name already exists
            if Medicine.objects.filter(name=medicine_name).exists():
                # If the medicine name already exists, set the error message
                error_message = "Medicine with this name already exists."
            else:
                # If the medicine name is unique, save it
                medicine_form.save()
                return HttpResponseRedirect('doctor-medicine')  # Redirect to the medicine view
    else:
        medicine_form = MedicineForm()

    mydict = {'medicine_form': medicine_form, 'error_message': error_message}  # Include error_message in the context
    return render(request, 'hospital/Doctor_Add_medicine.html', context=mydict)



####aa nakhvanuch###
@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_add_medicine_view(request):
    if request.method == 'POST':
        medicine_form = MedicineForm(request.POST)
        if medicine_form.is_valid():
            medicine_form.save()
            return HttpResponseRedirect('com-medicine')  # Redirect to the medicine view
    else:
        medicine_form = MedicineForm()

    mydict = {'medicine_form': medicine_form}
    return render(request, 'hospital/com_add_medicine.html', context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_medicine_view(request):
    medicine = Medicine.objects.all()  # Fetch all doctors from the database
    return render(request, 'hospital/doctor_view_medicine.html', {'medicine': medicine})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_medicine_view(request):
    medicine = Medicine.objects.all().order_by('-created_at')   
    medicine_count = medicine.count()
    mydict={
    'medicine':medicine,
    'medicine_count': medicine_count
    }
    return render(request,'hospital/doctor_medicine.html',context=mydict)



# views.py

from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404, redirect
from xhtml2pdf import pisa
from .models import Appointment, Medicine
from .forms import AppointmentForm

def download_invoice_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Fetch related data
    appointments = Appointment.objects.all()
    past_appointments = Appointment.objects.filter(patient=appointment.patient, id__lt=appointment_id)
    medicines = Medicine.objects.all()

    # Prepare context data for rendering the invoice template
    context = {
        'appointments' : appointments,
        'appointment': appointment,
        'past_appointments': past_appointments,
        'medicines': medicines,
    }

    # Get the HTML template for the invoice
    template_path = 'hospital/invoice.html'
    template = get_template(template_path)

    # Render the HTML template with the context data
    html = template.render(context)

    # Create a PDF from the HTML content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Failed to generate PDF: %s' % pisa_status.err)

    return response



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_medicine_view(request):
    medicine = Medicine.objects.all().order_by('-id')
    medicine_count = medicine.count()
    mydict={
    'medicine':medicine,
    'medicine_count': medicine_count
    }
    return render(request,'hospital/com_medicine.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True).order_by('-id')
    patientscount=models.Patient.objects.all().filter(status=True).count()
    mydict={
    'patients':patients,
    'patientscount':patientscount
    }
    return render(request,'hospital/admin_patient.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            UserProfile.objects.create(user=user, role='patient')

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group, created = Group.objects.get_or_create(name='PATIENT')
            my_patient_group.user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    # patientcount = models.Patient.objects.all().filter(status=True, user=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctor=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()
    patients = Patient.objects.all()
    patient_count = patients.count()
    medicine = Medicine.objects.all()
    medicine_count = medicine.count()
    doctor = request.user.doctor 
    appointments = Appointment.objects.filter(doctor=doctor)
    appointmentscount = appointments.count()
    compounder = Compounder.objects.all()
    compounder_count = compounder.count()
    mydict={
    'doctor': doctor,
    'appointments': appointments,
    'appointmentscount': appointmentscount,
    'patients':patients,
    'patient_count': patient_count,
    # 'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'medicine':medicine,
    'medicine_count': medicine_count,
    'compounder':compounder,
    'compounder_count': compounder_count,
    # 'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def compounder_dashboard_view(request):
    user = request.user
    patients = Patient.objects.all()
    patient_count = patients.count()
    medicine = Medicine.objects.all()
    medicine_count = medicine.count()
    appointments = Appointment.objects.all()
    appointmentscount = appointments.count()
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patients':patients,
        'patient_count':patient_count,
        'medicine':medicine,
        'medicine_count': medicine_count,
        'appointments': appointments,
        'appointmentscount':appointmentscount,
    }
    return render(request,'hospital/com_dashboard.html',context)




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_card_view(request):
    patients = Patient.objects.all()
    patient_count = patients.count()
    medicine = Medicine.objects.all()
    medicine_count = medicine.count()
    mydict={
    'patients':patients,
    'patient_count':patient_count,
    'medicine':medicine,
    'medicine_count': medicine_count,
    }
    return render(request,'hospital/doctor_dashboard_cards.html',context=mydict)


@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def compounder_dashboard_card_view(request):
    return render(request,'hospital/com_dashboard_cards.html')




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    patients = Patient.objects.all().order_by('-admitDate')
    patient_count = patients.count()
    mydict={
    'patients':patients,
    'patient_count': patient_count
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)


@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_patient_view(request):
    patients = Patient.objects.all().order_by('-admitDate')
    patient_count = patients.count()
    mydict={
    'patients':patients,
    'patient_count': patient_count
    }
    return render(request,'hospital/com_patient.html',context=mydict)



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_prescription_view(request):
    prescriptions = Prescription.objects.all() 
    return render(request,'hospital/com_prescription.html', {'prescriptions': prescriptions})


from .models import Medicine

@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_add_prescription_view(request):
    patients = Patient.objects.all()  # Fetch all patients
    medications = Medicine.objects.all()  # Fetch all medications

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('com-prescription')
    else:
        form = PrescriptionForm()
    return render(request, 'hospital/com_add_prescription.html', {'form': form, 'patients': patients, 'medications': medications})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_compounder_view(request):
    compounder = Compounder.objects.all().order_by('-created_at')
    compounder_count = compounder.count()
    mydict={
    'compounder':compounder,
    'compounder_count': compounder_count
    }
    return render(request,'hospital/doctor_compounder.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_compounder(request):
    userForm = CompounderUserForm()  
    compounderForm = CompounderForm()  
    mydict = {'userForm': userForm, 'compounderForm': compounderForm}
    
    if request.method == 'POST':
        userForm = CompounderUserForm(request.POST)
        compounderForm = CompounderForm(request.POST, request.FILES)
        
        if userForm.is_valid() and compounderForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            
            UserProfile.objects.create(user=user, role='compounder')
            
            compounder = compounderForm.save(commit=False)
            compounder.user = user
            compounder.status = True
            compounder.save()

            my_compounder_group, created = Group.objects.get_or_create(name='COMPOUNDER')
            my_compounder_group.user_set.add(user)

            return HttpResponseRedirect('doctor-compounder')

    return render(request, 'hospital/doctor_add_compounder.html', context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient(request):
    patients = Patient.objects.all()
    context = {'patients': patients}
    return render(request, 'hospital/doctor_view_patient.html', context)


@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_view_patient_view(request):
    return render(request, 'hospital/com_view_patient.html')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = request.user.doctor  # Retrieve the logged-in doctor
    appointments = Appointment.objects.all().order_by('-id')
    appointmentscount = appointments.count()
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'appointmentscount': appointmentscount,
    }
    
    return render(request, 'hospital/doctor_appointment.html', context)



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_appointment_view(request):
    appointments = Appointment.objects.all().order_by('-id')
    appointmentscount = appointments.count()
    context = {
        'appointments': appointments,
        'appointmentscount': appointmentscount,
    }
    return render(request, 'hospital/com_appointment.html', context)



@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_receipts_view(request):
    current_date = date.today()  # Get the current date
    appointments = Appointment.objects.filter(appointmentDate=current_date)
    appointmentscount = appointments.count()
    context = {
        'appointments': appointments,
        'appointmentscount': appointmentscount,
    }
    return render(request, 'hospital/receipts.html',context)


@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def com_get_receipts_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    past_appointments = Appointment.objects.filter(patient=appointment.patient, id__lt=appointment_id)
    medicines = Medicine.objects.all()

    if request.method == 'POST':
        print(request.POST.get('addnote'))
        appointment.add_note = request.POST.get('addnote')
        appointment.save()
        return redirect('com-get-receipts', appointment_id=appointment_id)
    else:
        form = AppointmentForm(instance=appointment)

    appointment_notes = appointment.a_note.split(',') if appointment.a_note else []

    context = {
        'appointment': appointment,
        'past_appointments': past_appointments,
        'medicines': medicines,
        'form': form,
        'appointment_notes': appointment_notes,  # e
    }
    return render(request, 'hospital/get_receipt.html', context)





@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def check_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.visited = True
    past_appointments = Appointment.objects.filter(patient=appointment.patient, id__lt=appointment_id)
    medicines = Medicine.objects.all()

    if request.method == 'POST':
        print(request.POST.get('note'))
        appointment.a_note = request.POST.get('note')
        appointment.visited = True
        appointment.save()
        return redirect('doctor-appointment')
    else:
        form = AppointmentForm(instance=appointment)

    context = {
        'appointment': appointment,
        'past_appointments': past_appointments,
        'medicines': medicines,
        'form': form,
    }
    return render(request, 'hospital/check_appointment.html', context)




@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_today_appointment_view(request):
    current_date = date.today()  # Get the current date
    appointments = Appointment.objects.filter(appointmentDate=current_date).order_by('-id')
    appointmentscount = appointments.count()
    context = {
        'appointments': appointments,
        'appointmentscount': appointmentscount,
    }
    return render(request, 'hospital/doctor_today_appointment.html', context)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    appointments = Appointment.objects.filter(doctor=request.user.doctor)
    return render(request, 'hospital/doctor_view_appointment.html', {'appointments': appointments})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_compounder_view(request):
    doctor = request.user
    compounders = Compounder.objects.filter(doctor=doctor)
    return render(request, 'hospital/doctor_view_compounder.html', {'compounders': compounders})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_patient_from_hospital(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        patient.delete()
        return redirect('doctor-view-patient')  # Redirect to the patient list page
    return render(request, 'hospital/doctor_view_patient.html', {'patient': patient})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_from_doctor_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    dtype = request.POST.get('delete_appointment')
    if dtype == 'from_dash':
        appointment.delete()
        return redirect('doctor-appointment')
    elif dtype=='from_view':
        appointment.delete()
        return redirect('doctor-view-appointment')
    else:
        return redirect('doctor-appointment')





@login_required(login_url='compounderlogin')
@user_passes_test(is_compounder)
def delete_appointment_from_com_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    dtype = request.POST.get('delete_appointment')
    if dtype == 'from_dash':
        appointment.delete()
        return redirect('com-appointment')
    elif dtype=='from_view':
        appointment.delete()
        return redirect('com-view-appointment')
    else:
        return redirect('com-appointment')





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    return render(request,'hospital/patient_dashboard.html')



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)



def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_compunder_view(request):
    compounder=models.Compounder.objects.all().filter(status=True).order_by('-id')
    compoundercount=models.Doctor.objects.all().filter(status=True).count()
    mydict={
    'compounder':compounder,
    'compoundercount':compoundercount,
    }
    return render(request,'hospital/admin_compunder.html',{'mydict':mydict})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_medicine_view(request):
    medicines=models.Medicine.objects.all()
    medicinecount=models.Medicine.objects.all().count()
    mydict={
    'medicines':medicines,
    'medicinecount':medicinecount,
    }
    return render(request,'hospital/admin_medicine.html',{'mydict':mydict})
