from django.db import models
from django.contrib.auth.models import User
import barcode
from barcode.writer import ImageWriter
import os
import barcode
from io import BytesIO
from django.core.files import File
import random
import string




ROLES = [
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
    ('compounder', 'Compounder'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES)

    # Add other fields as needed

    def __str__(self):
        return f'{self.user.username} Profile'
    



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=100,default=1)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name #
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    SYMPTOM_CHOICES = [
        ('', '-------- Select symptom --------'),
        ('Fever', 'Fever'),
        ('Cough', 'Cough'),
        ('Headache', 'Headache'),
        ('Fatigue', 'Fatigue'),
        ('Shortness of breath', 'Shortness of breath'),
        ('Other', 'Other'),
    ]
    symptoms = models.CharField(max_length=100, choices=SYMPTOM_CHOICES)
    # assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate = models.DateField(auto_now=True,blank=True,null=True)
    status = models.BooleanField(default=False)
    
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
    
    def __str__(self):
        return f" {self.first_name} {self.last_name}"
    



class Appointment(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,blank=True,null=True)
    # patientName=models.CharField(max_length=40,null=True)
    # doctorName=models.CharField(max_length=40,null=True)
    appointmentDate = models.DateField(auto_now_add=True,blank=True,null=True)  # Automatically set to current date when the object is created
    appointmentTime = models.TimeField(auto_now_add=True,blank=True,null=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)






class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    barcode = models.ImageField(upload_to='barcodes/', blank=True)
    created_at = models.DateField(auto_now_add=True,blank=True,null=True)

    # Modify the generate_barcode method to generate a 12-digit numeric string for EAN-13
    def generate_barcode(self):
        # Generate a random UUID as the barcode
        barcode_value = ''.join(random.choices(string.digits, k=12))

        # Generate barcode using python-barcode library
        ean = barcode.get_barcode_class('ean13')
        code = ean(barcode_value, writer=ImageWriter())

        # Save barcode to BytesIO buffer
        buffer = BytesIO()
        code.write(buffer)

        # Create filename
        filename = f'{barcode_value}.png'
        filepath = os.path.join('barcodes', filename)

        # Ensure the directory exists before saving the file
        if not os.path.exists('barcodes'):
            os.makedirs('barcodes')

        # Save barcode image to ImageField
        self.barcode.save(filename, File(buffer), save=False)


    def save(self, *args, **kwargs):
        if not self.barcode:
            self.generate_barcode()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Compounder(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=40, null=True)
    last_name = models.CharField(max_length=40, null=True)
    email = models.CharField(max_length=40, null=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True, blank=True)  # Assuming max_length for username
    password = models.CharField(max_length=128, blank=True)  # Storing password securely is crucial; consider using hashing algorithms
    created_at = models.DateField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medicine, related_name='prescriptions')
    notes = models.TextField(blank=True)
    

    def __str__(self):
        return f"Prescription for {self.patient}"

#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
