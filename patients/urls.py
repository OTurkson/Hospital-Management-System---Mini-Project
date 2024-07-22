from django.urls import path
from .views import *

urlpatterns = [
    path('', PatientList.as_view(), name='patients'),
    path('<int:patient_id>', PatientDetail.as_view(), name='patient_detail'),
    path('<int:patient_id>/vitals', PatientVitals.as_view(), name='patient_vitals'),
    path('<int:patient_id>/records', MedicalRecordList.as_view(), name='medical_records'),
    path('<int:patient_id>/records/<int:record_id>', PatientMedicalRecord.as_view() , name='patient_record'),
    path('<int:patient_id>/emergency_contact', EmergencyContactDetail.as_view(), name='emergency_contact'),
    path('check-ins', CheckInList.as_view(), name='checkins'),
    path('check-ins/<int:checkin_id>', CheckInDetail.as_view(), name='checkin_detail'),
    path('appointments', AppointmentList.as_view(), name='appointments'),
    path('appointments/<int:appointment_id>', AppointmentDetail.as_view(), name='appointment_detail'),  
]