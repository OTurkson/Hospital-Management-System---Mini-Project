from django.urls import path
from . import views

urlpatterns = [
    path('doctors', views.DoctorList.as_view(), name='doctors'),
    path('doctors/<int:doctor_id>', views.DoctorDetail.as_view(), name='doctor_detail'),
]