"""

Developed By : sumit kumar
facebook : fb.com/sumit.luv
Youtube :youtube.com/lazycoders


"""




from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from django.conf.urls.static import static


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.home_view,name=''),


    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('', LoginView.as_view(template_name='hospital/doctorlogin.html'),name='doctorlogin'),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('compounderlogin', LoginView.as_view(template_name='hospital/compounderlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    # path('logout', LogoutView.as_view(template_name='hospital/doctorlogin.html'),name='logout'),
    path('logout', views.doctor_logout,name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),


    path('admin-compunder', views.admin_compunder_view,name='admin-compunder'),
    path('admin-add-compunder', views.admin_add_compounder_view,name='admin-add-compunder'),
    path('admin-view-compounder', views.admin_view_compounder_view,name='admin-view-compounder'),

    path('admin-medicine', views.admin_medicine_view,name='admin-medicine'),
    path('admin-add-medicine', views.admin_add_medicine_view,name='admin-add-medicine'),
    path('admin-view-medicine', views.admin_view_medicine_view,name='admin-view-medicine'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-add-patient', views.doctor_add_patient_view,name='doctor-add-patient'),
    path('doctor-view-patient', views.doctor_view_patient,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-update-patient/<int:pk>', views.update_patient_view_doctor,name='doctor-update-patient'),
    path('delete-patient-from-doctor/<int:pk>', views.delete_patient_from_doctor_view,name='delete-patient-from-doctor'),
    
    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-add-appointment', views.doctor_add_appointment_view,name='doctor-add-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_from_doctor_view,name='delete-appointment'),
    path('update-appointment/<int:pk>', views.update_appointment_view,name='update-appointment'),


    path('doctor-medicine', views.doctor_medicine_view,name='doctor-medicine'),
    path('doctor-add-medicine', views.doctor_add_medicine_view,name='doctor-add-medicine'),
    path('doctor-view-medicine', views.doctor_view_medicine_view,name='doctor-view-medicine'),
    path('delete-medicine-from-doctor/<int:pk>', views.delete_medicine_from_doctor_view,name='delete-medicine-from-doctor'),
    path('update-medicine/<int:pk>', views.update_medicine_view,name='update-medicine'),
    
    
    
    path('doctor-compounder', views.doctor_compounder_view,name='doctor-compounder'),
    path('doctor-add-compounder', views.doctor_add_compounder,name='doctor-add-compounder'),
    path('doctor-view-compounder', views.doctor_view_compounder_view,name='doctor-view-compounder'),
    path('doctor-update-compounder/<int:pk>', views.update_compounder_view_doctor,name='doctor-update-compounder'),
    path('delete-compounder-from-doctor/<int:pk>', views.delete_compounder_from_doctor_view,name='delete-compounder-from-doctor'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]



# ---------FOR Compunder RELATED URLS-------------------------------------
urlpatterns +=[
    path('com-dashboard', views.compounder_dashboard_view,name='com-dashboard'),
    # path('search', views.search_view,name='search'),

    path('com-patient', views.com_patient_view,name='com-patient'),
    path('com-add-patient', views.com_add_patient_view,name='com-add-patient'),
    path('com-view-patient', views.com_view_patient_view,name='com-view-patient'),
    path('com-update-patient/<int:patient_id>', views.update_patient_view_com,name='com-update-patient'),
    path('delete-patient-from-com/<int:pk>', views.delete_patient_from_com_view,name='delete-patient-from-com'),

    # path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('com-prescription', views.com_prescription_view,name='com-prescription'),
    path('com-add-prescription', views.com_add_prescription_view,name='com-add-prescription'),
    path('delete-prescription-from-com/<int:pk>', views.delete_prescription_from_com_view,name='delete-prescription-from-com'),
    path('com-update-prescription/<int:prescription_id>', views.update_prescription_view_com,name='com-update-prescription'),
    # path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    # path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    # path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),

    path('com-medicine', views.com_medicine_view,name='com-medicine'),
    path('com-add-medicine', views.com_add_medicine_view,name='com-add-medicine'),
    path('delete-medicine-from-com/<int:pk>', views.delete_medicine_from_com_view,name='delete-medicine-from-com'),
]




###########################



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
