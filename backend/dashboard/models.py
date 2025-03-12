from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Surgeon(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Procedure(models.Model):
    SERVICE_CHOICES = [
        ('Melanoma', 'Melanoma'),
        ('Gastrectomy', 'Gastrectomy'),
        ('Whipple', 'Whipple'),
    ]
    
    T_STAGE_CHOICES = [
        ('T1', 'T1'),
        ('T2', 'T2'),
        ('T3', 'T3'),
        ('T4', 'T4'),
    ]
    
    P_STAGE_CHOICES = [
        ('I', 'I'),
        ('II', 'II'),
        ('III', 'III'),
        ('IV', 'IV'),
    ]
    
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    surgeon = models.ForeignKey(Surgeon, on_delete=models.CASCADE)
    date = models.DateTimeField()
    length_of_stay = models.IntegerField()
    complications = models.BooleanField(default=False)
    t_stage = models.CharField(max_length=2, choices=T_STAGE_CHOICES)
    p_stage = models.CharField(max_length=3, choices=P_STAGE_CHOICES)
    procedure_time = models.FloatField()
    
    @classmethod
    def get_average_los(cls):
        return cls.objects.aggregate(Avg('length_of_stay'))['length_of_stay__avg']
    
    @classmethod
    def get_average_procedure_time(cls):
        return cls.objects.aggregate(Avg('procedure_time'))['procedure_time__avg']
    
    @classmethod
    def get_average_by_service(cls, service_type):
        return {
            'los': cls.objects.filter(service=service_type).aggregate(Avg('length_of_stay'))['length_of_stay__avg'],
            'procedure_time': cls.objects.filter(service=service_type).aggregate(Avg('procedure_time'))['procedure_time__avg']
        }

    def __str__(self):
        return f"{self.service} by {self.surgeon.name} on {self.date}" 