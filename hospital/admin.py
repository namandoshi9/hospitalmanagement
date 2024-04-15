from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails,Compounder, Medicine
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


class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'barcode_img')

    def barcode_img(self, obj):
        return '<img src="{}" width="100" />'.format(obj.barcode.url)

    barcode_img.allow_tags = True

admin.site.register(Medicine, MedicineAdmin)