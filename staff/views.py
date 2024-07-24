from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from django.http import Http404
from django.db.models.deletion import ProtectedError
from patients.models import MedicalRecord

# Create your views here.
class DoctorList(APIView):
    permission_classes = [IsAuthenticated]
    #retrieve all doctors
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True) 
        response_data = {
            'doctors': serializer.data,
            'doctor_count': len(doctors)
        }       
        return Response(response_data, status=status.HTTP_200_OK)
        
    #add a new doctor
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        #check if doctor exists with same email address
        if Doctor.objects.filter(email=request.data['email']).exists():
            return Response({"message":"Doctor with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DoctorDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, doctor_id):
        try:
            return Doctor.objects.get(doctor_id= doctor_id)
        except Doctor.DoesNotExist:
            raise Http404("Doctor does not exist")
        
    #get doctor by id
    def get(self, request, doctor_id):
        doctor = self.get_object(doctor_id)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #update doctor by id
    def put(self, request, doctor_id):
        doctor = self.get_object(doctor_id)
        serializer = DoctorSerializer(doctor, data=request.data)
        #check if doctor exists with same email address
        if Doctor.objects.filter(email=request.data['email']).exclude(doctor_id=doctor_id).exists():
            return Response({"message":"Doctor with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
            # reassign related MedicalRecord instances here
            # MedicalRecord.objects.filter(doctor=doctor).update(doctor=None)
            # For example, reassign or delete them
            doctor.delete()
            return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Doctor.DoesNotExist:
            return Response({"message": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        except ProtectedError:
            return Response({"message": "Cannot delete Doctor because they are referenced in medical records"}, status=status.HTTP_400_BAD_REQUEST)