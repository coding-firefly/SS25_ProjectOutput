from django.db import models
from django.contrib.auth.models import User

default_name = "Annonymous_Doctor"
default_email = "incoming@codices-divinum.com"
default_branch = "The_Great_Gaa_Hospital"
default_speciality = "General Practitioner"

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete= models.CASCADE,
        related_name= "doctor_profile"
    )
    name = models.CharField(max_length= 250, blank= True, null= True, default= default_name)
    work_email = models.EmailField(max_length= 100, blank= True, null= True, default= default_email)
    branch = models.CharField(max_length= 100, blank= True, null= True, default= default_branch)
    speciality = models.CharField(max_length= 100, blank= True, null= True, default= default_speciality)

    def __str__(self):
        return f"Dr {self.name} is established as doctor in: {self.speciality}"
    
    def details(self):
        return [self.name, self.branch, self.speciality, self.work_email]
    
class PatientProfile(models.Model):
    name = models.CharField(max_length= 250)
    doctors = models.ManyToManyField(
        DoctorProfile,
        related_name= "patient",
        blank= True
    )
    patient_details = models.TextField(blank= True, null= True, default="No Details from Patient is Given")

    def __str__(self):
        doctor_names = ", ".join([d.name for d in self.doctors.all()])
        return f"Patient {self.name} in charge by Doctors: {doctor_names if doctor_names else 'None Assign Yet'}"
    
    def details(self):
        return [self.name, self.doctors.all]