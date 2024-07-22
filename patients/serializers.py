from rest_framework import serializers
from .models import *


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = '__all__'
        read_only_fields = ('patient',)

class VitalsSerializer(serializers.ModelSerializer):
    bmi = serializers.SerializerMethodField()

    class Meta:
        model = Vitals
        fields = '__all__'

    def get_bmi(self, obj):
        return obj.bmi

class MedicalRecordSerializer(serializers.ModelSerializer):
    vitals = VitalsSerializer(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['record_id', 'patient', 'doctor', 'time', 'reason', 'diagnosis', 'vitals']

class PatientSerializer(serializers.ModelSerializer):
    emergency_contact = EmergencyContactSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ['patient_id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'marital_status', 'occupation', 'emergency_contact']



###CHECKIN AND APPOINTMENT SERIALIZERS###
class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckIn
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'