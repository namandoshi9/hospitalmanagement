from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Compounder, Medicine,Prescription
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

# class PatientAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)




from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'get_medications', 'notes']

    def get_medications(self, obj):
        return ", ".join([medication.name for medication in obj.medications.all()])

    get_medications.short_description = 'Medications'

# class MedicineAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'barcode_img')

#     def barcode_img(self, obj):
#         return '<img src="{}" width="100" />'.format(obj.barcode.url)

#     barcode_img.allow_tags = True

# admin.site.register(Medicine, MedicineAdmin)


from import_export.admin import ImportExportModelAdmin

@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    list_display = ("id" ,"barcode" ,"name" , "description", "created_at", )

@admin.register(Compounder)
class CompounderAdmin(ImportExportModelAdmin):
    list_display = ("id" ,"first_name" , "last_name", "mobile", "created_at", )

@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    list_display = ("id" , "first_name", "last_name", "symptoms", "admitDate",)   
