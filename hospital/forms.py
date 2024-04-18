from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Medicine,Compounder
from django import forms
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment, Prescription


#for admin signup
class AdminSigupForm(forms.ModelForm):
    role = forms.ChoiceField(choices=models.ROLES)
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','role']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']



class PatientUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ['first_name','last_name','address', 'mobile', 'symptoms']

    

        



class AppointmentForm(forms.ModelForm):
    # patientId = forms.ModelChoiceField(queryset=Patient.objects.filter(status=True), empty_label="Select Patient", to_field_name="id")
    # doctorId = forms.ModelChoiceField(queryset=Doctor.objects.filter(status=True), empty_label="Select Doctor", to_field_name="id")

    class Meta:
        model = Appointment
        # fields = ['patientId', 'doctorId',  'description', 'status']
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].empty_label = "-------- Select patient --------"
        self.fields['doctor'].empty_label = "-------- Select doctor --------"


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'barcode']  # Add other fields as needed



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders


class CompounderUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
class CompounderForm(forms.ModelForm):
    class Meta:
        model = Compounder
        exclude = ['doctor']


class PrescriptionForm(forms.ModelForm):
    medications = forms.ModelChoiceField(queryset=Medicine.objects.all(), widget=forms.Select)

    class Meta:
        model = Prescription
        fields = ['patient', 'medications', 'notes']