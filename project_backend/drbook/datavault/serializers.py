from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.mail import send_mail 
from django.template.loader import render_to_string 
from django.utils.html import strip_tags 
from django.conf import settings

from .models import DoctorProfile, PatientProfile

class DoctorsSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only= True)
    username = serializers.CharField(required= True)
    password = serializers.CharField(required= True)
    name = serializers.CharField(
        source="doctor_profile.name",
        default= "Annonymous_Doctor",
        required= False,
        allow_null= False,
        allow_blank= True
    )
    branch = serializers.CharField(
        source="doctor_profile.branch",
        default= "The_Great_Gaa_Hospital",
        required= False,
        allow_null= False,
        allow_blank= True
    )
    speciality = serializers.CharField(
        source="doctor_profile.speciality",
        default= "General Practitioner",
        required= False,
        allow_null= False,
        allow_blank= True
    )
    work_email = serializers.EmailField(
        source="doctor_profile.work_email",
        default= "incoming@codices-divinum.com",
        required= False,
        allow_null= False,
        allow_blank= True
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "name", "branch", "speciality", "work_email"]

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        profile_data = validated_data.pop("doctor_profile", {})

        profile_name = profile_data.get('name') 
        profile_work_email = profile_data.get('work_email')
        profile_branch = profile_data.get('branch')
        profile_speciality = profile_data.get('speciality')

        print(f"New Doctor Created:{profile_name, profile_branch, profile_speciality}")
        validated_data.pop('name', None) 
        validated_data.pop('branch', None)
        validated_data.pop('speciality', None)
        validated_data.pop('username', None) 
        validated_data.pop('password', None)

        user = User.objects.create_user(
            username=username,
            password=password
        )

        DoctorProfile.objects.create(
            user=user,
            name=profile_name,
            work_email=profile_work_email,
            branch=profile_branch,
            speciality=profile_speciality
        )
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        instance.username = validated_data.get('username', instance.username)
        instance.save()

        profile_data = validated_data.pop('doctor_profile', {})
        profile, created = DoctorProfile.objects.get_or_create(user=instance)

        profile.name = profile_data.get('name', profile.name)
        profile.work_email = profile_data.get('work_email', profile.work_email)
        profile.branch = profile_data.get('branch', profile.branch)
        profile.speciality = profile_data.get('speciality', profile.speciality)
        profile.save()

        return instance
    
class PatientProfileSerializer(serializers.ModelSerializer):
    doctors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DoctorProfile.objects.all(), 
        required=False, 
        allow_empty=True 
    )

    patient_details = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = PatientProfile
        fields = ['id', 'name', 'doctors', 'patient_details']
        read_only_fields = ['id']

    def create(self, validated_data):
        doctors_data = validated_data.pop("doctors", [])
        patient = PatientProfile.objects.create(**validated_data)
        if doctors_data:
            patient.doctors.set(doctors_data)
        
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                requesting_doctor_profile = request.user.doctor_profile
                recipient_emails = requesting_doctor_profile.work_email
                subject = f'New Patient Created: {patient.name} (ID: {patient.id})'
                
                plain_message = (
                    f"Dear {requesting_doctor_profile.name},\n\n"
                    f"A new patient has been created in the system by your account:\n\n"
                    f"Patient ID: {patient.id}\n"
                    f"Patient Name: {patient.name}\n"
                    f"Patient Details: {patient.patient_details if patient.patient_details else 'No details provided.'}\n"
                    f"Assigned Doctors: {', '.join([d.name for d in patient.doctors.all()])}\n\n"
                    f"Please log in to the system to view full details and manage this patient.\n\n"
                    f"This is an automated notification. Please do not reply."
                )

                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL, 
                    [recipient_emails], 
                    fail_silently=False, 
                )
            except DoctorProfile.DoesNotExist:
                print(f"Warning: Authenticated user {request.user.username} (ID: {request.user.id}) does not have a DoctorProfile. Cannot send email.")
            except Exception as e:
                print(f"Error sending email for new patient: {e}")


        return patient