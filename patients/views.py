from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import Patient, Vitals, MedicalRecord, EmergencyContact, CheckIn, Appointment
from django.http import Http404
# from .forms import EmergencyContactForm
from django.shortcuts import redirect,get_object_or_404
from datetime import datetime
from .emails import *

#add permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PatientList(APIView):
    permission_classes = [IsAuthenticated]
    #list all patients
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        response_data = {
            'patients': serializer.data,
            'patient_count': len(patients)
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    #add a new patient
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            # #send email to patient
            # send_registration_email(patient.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):
    permission_classes = [IsAuthenticated]
    #find patient by id
    def get_object(self, patient_id):
        try:
            return Patient.objects.get(patient_id= patient_id)
        except Patient.DoesNotExist:
            raise Http404('Patient does not exist')
    
    #a single patient
    def get(self, request, patient_id):
        patient = self.get_object(patient_id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #edit patient
    def put(self, request, patient_id):
        patient = self.get_object(patient_id)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete patient
    def delete(self, request, patient_id):
        patient = self.get_object(patient_id)
        #add logic to delete undone appointments and check them out
        undone_appointments = Appointment.objects.filter(patient=patient, status=False)
        [appointment.delete() for appointment in undone_appointments]
        # checkins = CheckIn.objects.filter(patient=patient, checkout_time=None)
        # [checkin.delete() for checkin in checkins]
            
        patient.delete()
        return Response("Patient has been deleted successfully",status=status.HTTP_204_NO_CONTENT)


class PatientVitals(APIView):
    permission_classes = [IsAuthenticated]

    #find patient by id
    def get_object(self, patient_id):
        try:
            patient = Patient.objects.get(patient_id= patient_id)
        except Patient.DoesNotExist:
            raise Http404('Patient does not exist')
        try:
            vitals = Vitals.objects.filter(patient=patient_id)
        except Vitals.DoesNotExist:
            raise Http404("Vitals do not exist")
        return vitals
        
        
    #single patient's vitals
    def get(self, request, patient_id):
        vitals = self.get_object(patient_id=patient_id)
        vitals = vitals.latest('vitals_id')
        serializer = VitalsSerializer(vitals)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #add vitals for a patient
    def post(self, request, patient_id):
        vitals = self.get_object(patient_id=patient_id)
        patient = Patient.objects.get(patient_id=patient_id)
        serializer = VitalsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #edit vitals
    def put(self, request, patient_id):
        vitals = self.get_object(patient_id=patient_id)
        try:
            vitals = vitals.get(vitals_id=request.data["vitals_id"])
        except Vitals.DoesNotExist:
            raise Http404("Vitals record does not exist")
    
        serializer = VitalsSerializer(vitals, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete patient's vitals
    def delete(self, request, patient_id):
        vitals = self.get_object(patient_id = patient_id)
        try:
            vitals = vitals.get(vitals_id=request.data["vitals_id"])
        except Vitals.DoesNotExist:
            raise Http404("Vitals record does not exist")
        vitals.delete()
        return Response("Vitals record successfully deleted",status=status.HTTP_204_NO_CONTENT)


class MedicalRecordList(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, patient_id):
        try:
            patient = Patient.objects.get(patient_id= patient_id)
        except Patient.DoesNotExist:
            raise Http404('Patient does not exist')
        else:
            try:
                records = MedicalRecord.objects.filter(patient= patient_id)
            except MedicalRecord.DoesNotExist:
                raise Http404("Medical record does not exist")
        return records
 

    # all medical records for a patient
    def get(self, request, patient_id):
        records = self.get_object(patient_id=patient_id)
        if records is None:
            return Response({'error':'Non-existent medical record(s)'},status=status.HTTP_404_NOT_FOUND)
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #add medical record
    def post(self, request, patient_id):
        
        
        # # Retrieve the Patient instance
        # patient = get_object_or_404(Patient, pk=patient_id)

        # #use serialization
        # serializer = EmergencyContactSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(patient=patient)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        patient = get_object_or_404(Patient, pk=patient_id)
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientMedicalRecord(APIView):
    permission_classes = [IsAuthenticated]
    #find patient by id
    def get_object(self, patient_id, record_id):
        try:
            patient = Patient.objects.get(patient_id= patient_id)
        except Patient.DoesNotExist:
            raise Http404('Patient does not exist')
        else:
            try:
                medical_record = MedicalRecord.objects.get(patient= patient_id, record_id=record_id)
            except MedicalRecord.DoesNotExist:
                raise Http404("Medical record does not exist")
        return medical_record
        
        
    #get a single medical record
    def get(self, request, patient_id, record_id):
        medical_record = self.get_object(patient_id=patient_id, record_id=record_id)
        serializer = MedicalRecordSerializer(medical_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #change a single medical record
    def put(self, request, patient_id, record_id):
        medical_record = self.get_object(patient_id=patient_id, record_id=record_id)
        serializer = MedicalRecordSerializer(medical_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete a single medical record
    def delete(self, request, patient_id, record_id):
        medical_record = self.get_object(patient_id = patient_id, record_id=record_id)
        medical_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmergencyContactDetail(APIView):
    permission_classes = [IsAuthenticated]
    #find emergency contact by patient id
    def get_object(self, patient_id):
        try:
            patient = Patient.objects.get(patient_id=patient_id)
        except Patient.DoesNotExist:
            raise Http404("Patient does not exist")    
        else:
            try:
                emergency_contact = EmergencyContact.objects.get(patient= patient_id)
            except EmergencyContact.DoesNotExist:
                raise Http404("Emergency contact does not exist")
        return emergency_contact
        
    #retrieve a patient's emergency contact
    def get(self, request, patient_id):
        emergency_contact = self.get_object(patient_id)
        serializer = EmergencyContactSerializer(emergency_contact)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #add emergency contact for a patient
    def post(self, request, patient_id):
        # Each patient is allowed only one emergency contact
        if EmergencyContact.objects.filter(patient=patient_id).exists():
            return Response({"error": "Patient already has an emergency contact"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the Patient instance
        patient = get_object_or_404(Patient, pk=patient_id)

        #use serialization
        serializer = EmergencyContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=patient)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
    #change emergency contact for a patient
    def put(self, request, patient_id):
        emergency_contact = self.get_object(patient_id)
        serializer = EmergencyContactSerializer(emergency_contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete emergency contact for a patient
    def delete(self, request, patient_id):
        emergency_contact = self.get_object(patient_id)
        emergency_contact.delete()
        return Response("Contact has been deleted successfully",status=status.HTTP_204_NO_CONTENT)
   
# def add_emergency_contact(request, patient_id):
#     patient = Patient.objects.get(patient_id=patient_id)
#     if request.method == 'POST':
#         form = EmergencyContactForm(request.POST)
#         if form.is_valid():
#             form.save(patient=patient)
#             return redirect('patients')
        




    ###CHECKIN AND APPOINTMENT###
# from django.shortcuts import render, redirect
# from .forms import CheckInForm, AppointmentForm

class CheckInList(APIView):
    permission_classes = [IsAuthenticated]
    #list all checkins
    def get(self, request):
        checkins = CheckIn.objects.all()
        modified_data = []
        for checkin in checkins:
            serializer = CheckInSerializer(checkin)
            data = serializer.data
            patient = Patient.objects.get(patient_id=data["patient"])
            doctor = Doctor.objects.get(doctor_id=data["doctor"])
            data["patient_name"] = f'{patient.first_name} {patient.last_name}'
            data["doctor_name"] = f'{doctor.first_name} {doctor.last_name}'
            modified_data.append(data)

        response_data = {
            'checkins': modified_data,
            'checkin_count': len(checkins)
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    #add a new checkin
    def post(self, request):
        
        #check if last record of checkin for patient is checked out
        try:
            patient = Patient.objects.get(patient_id=request.data["patient"])
        except Patient.DoesNotExist:
            raise Http404("Patient does not exist. Please add patient first")
        try:
            last_checkin = CheckIn.objects.filter(patient=patient).first()
            if last_checkin:
                if last_checkin.checkout_time is None:
                    return Response("Patient has not checked out", status=status.HTTP_400_BAD_REQUEST)
        except CheckIn.DoesNotExist:
            pass

        checkin_datetime_str = request.data["checkin_time"] # Assuming request.data["checkin_time"] is a string representing a datetime
        checkin_datetime = datetime.strptime(checkin_datetime_str, "%Y-%m-%d %H:%M:%S")# Convert the string to a datetime object
        checkin_date = checkin_datetime.date()# Extract just the date part

        serializer = CheckInSerializer(data=request.data)
        
        #check if patient has an appointment
        if serializer.is_valid():
            try:
                appointment = Appointment.objects.get(patient=patient, date = checkin_date)
            except Appointment.DoesNotExist:
                pass
            else:
                if appointment.status:
                    return Response("Patient has already checked in for this appointment", status=status.HTTP_400_BAD_REQUEST)
                else:
                    appointment.status = True
                    appointment.save()
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckInDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, checkin_id):
        try:
            return CheckIn.objects.get(checkin_id= checkin_id)
        except CheckIn.DoesNotExist:
            raise Http404('Checkin record does not exist')
        
    #get checkin by id
    def get(self, request, checkin_id):
        checkin = self.get_object(checkin_id)
        serializer = CheckInSerializer(checkin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #update checkin by id
    def put(self, request, checkin_id):
        checkin = self.get_object(checkin_id)
        # Assuming 'status' is a boolean field on the checkin object
        if hasattr(checkin, 'status'):
            checkin.status = not checkin.status  # Toggle the status
            checkin.save()  # Save the changes to the database
            return Response({'status': f'Checkin status toggled successfully to {checkin.status}'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'CheckIn object does not have a status attribute'}, status=status.HTTP_400_BAD_REQUEST)
    
    #delete checkin by id
    def delete(self, request, checkin_id):
        checkin = self.get_object(checkin_id)
        checkin.delete()
        return Response({'message':'CheckIn record successfully deleted'},status=status.HTTP_204_NO_CONTENT)
    

class AppointmentList(APIView):
    permission_classes = [IsAuthenticated]

    #list all appointments
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        response_data = {
            'appointments': serializer.data,
            'appointment_count': len(appointments)
        }
        return Response(response_data, status=status.HTTP_200_OK)
        
    #add a new appointment
    def post(self, request):
        try:
            patient = Patient.objects.get(patient_id=request.data["patient"])
        except Patient.DoesNotExist:
            raise Http404("Patient does not exist. Please add patient first")
        
        serializer = AppointmentSerializer(data=request.data)
        
        if serializer.is_valid():
            #check if the current appointment time is not in the past
            appointment_date = request.data["date"]
            appointment_time = request.data["time"]
            
            # Convert string to datetime.date object
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()

            # Convert string to datetime.time object, assuming time is in 'HH:MM' format
            appointment_time = datetime.strptime(appointment_time, '%H:%M').time()

            if appointment_date < datetime.now().date():
                return Response({"error":"Appointment date cannot be in the past"}, status=status.HTTP_400_BAD_REQUEST)
            elif appointment_date == datetime.now().date():
                if appointment_time <= datetime.now().time():
                    return Response({"error":"Appointment time cannot be in the past"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    pass
            else:
                pass
           
            serializer.save()
            patient = Patient.objects.get(patient_id=serializer.data["patient"])
            doctor = Doctor.objects.get(doctor_id=serializer.data["doctor"])
            #send email to patient and doctor
            if patient.email:
                send_appointment_email(patient.email, doctor.email, serializer.data["date"], serializer.data["time"])
            else:
                send_appointment_email(patient.email, doctor.email, serializer.data["date"], serializer.data["time"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AppointmentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, appointment_id):
        try:
            return Appointment.objects.get(appointment_id= appointment_id)
        except Appointment.DoesNotExist:
            raise Http404('Appointment does not exist')
        
    #get appointment by id
    def get(self, request, appointment_id):
        appointment = self.get_object(appointment_id)
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #update appointment by id
    def put(self, request, appointment_id):
        appointment = self.get_object(appointment_id)
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete appointment by id
    def delete(self, request, appointment_id):
        appointment = self.get_object(appointment_id)
        appointment.delete()
        return Response({'message':'Successfully deleted appointment record'},status=status.HTTP_204_NO_CONTENT)




# def check_in_view(request):
#     if request.method == 'POST':
#         form = CheckInForm(request.POST)
#         if form.is_valid():
#             form.save()
#             #display bootstrap success alert if succesful
#             success = True
#             return redirect('/', {'success':success})  # Replace 
#     else:
#         form = CheckInForm()
#     return render(request, 'patients/check_in_template.html', {'form': form})


# def appointment_view(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_url')  # Replace 'success_url' with the name of your success URL
#     else:
#         form = AppointmentForm()
#     return render(request, 'patients/appointment_template.html', {'form': form})