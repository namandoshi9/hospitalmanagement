from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Compounder, Medicine,Prescription
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)


admin.site.register(Compounder)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient',  'notes']


# class MedicineAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'barcode_img')

#     def barcode_img(self, obj):
#         return '<img src="{}" width="100" />'.format(obj.barcode.url)

#     barcode_img.allow_tags = True

# admin.site.register(Medicine, MedicineAdmin)


from import_export.admin import ImportExportModelAdmin

@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    list_display = ("id" ,"barcode" ,"name" , "description",)