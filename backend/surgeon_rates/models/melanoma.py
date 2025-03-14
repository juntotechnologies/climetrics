from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Surgeon(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    years_of_service = models.FloatField()

    def __str__(self):
        return self.name

class Patient(models.Model):
    patient_id = models.CharField(max_length=100, unique=True)
    age = models.FloatField()
    female = models.BooleanField()
    bmi = models.FloatField()
    
    def __str__(self):
        return self.patient_id

class MelanomaProcedure(models.Model):
    event_id = models.CharField(max_length=100, unique=True)
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    surgery_date = models.DateField()
    thickness = models.FloatField()  # Melanoma thickness in mm
    ulceration = models.BooleanField()  # Presence of ulceration
    
    # SLND (Sentinel Lymph Node Dissection) related fields
    slnd_performed = models.BooleanField(default=False)
    slnd_positive = models.BooleanField(default=False)
    complete_node_dissection = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['surgery_date']),
            models.Index(fields=['surgeon']),
        ]

class Complication(models.Model):
    COMPLICATION_TYPES = [
        ('ANY', 'Any Complication'),
        ('WOUND', 'Wound Infection'),
        ('CELLULITIS', 'Cellulitis'),
        ('SEROMA', 'Seroma'),
        ('GRAFT', 'Graft Complication')
    ]
    
    GRADES = [
        (2, 'Grade 2'),
        (3, 'Grade 3')
    ]
    
    procedure = models.ForeignKey(MelanomaProcedure, on_delete=models.CASCADE)
    complication_type = models.CharField(max_length=20, choices=COMPLICATION_TYPES)
    grade = models.IntegerField(choices=GRADES)
    date_occurred = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['complication_type', 'grade']),
            models.Index(fields=['procedure']),
        ]

class SurgeonRate(models.Model):
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    model_id = models.CharField(max_length=100)
    rate = models.FloatField()
    cases = models.IntegerField()
    method = models.CharField(max_length=100)
    date = models.DateField()
    covariates = models.TextField(blank=True)
    heterotest = models.FloatField(null=True)
    routine_unadjusted = models.BooleanField(default=False)
    result_text = models.TextField()
    total_cases = models.IntegerField()
    num_users = models.IntegerField()
    min_events = models.IntegerField()
    avg_cov = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['model_id']),
            models.Index(fields=['surgeon']),
            models.Index(fields=['date']),
        ] 