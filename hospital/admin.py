from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Compounder, Medicine,Prescription
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)


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




from import_export.admin import ImportExportModelAdmin

@admin.register(Medicine)
class MedicineAdmin(ImportExportModelAdmin):
    list_display = ("id" ,"barcode" ,"name" , "description", "barcode_value", "created_at", )

@admin.register(Compounder)
class CompounderAdmin(ImportExportModelAdmin):
    list_display = ("id" ,"first_name" , "last_name", "mobile", "created_at", )

@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    list_display = ("id" , "first_name", "last_name", "symptoms", "admitDate", 'serial_number',)   

@admin.register(Appointment)
class AppointmentAdmin(ImportExportModelAdmin):
    list_display = ("id" , "patient", "appointmentDate", "appointmentTime", "description", "a_note", "add_note",)   
