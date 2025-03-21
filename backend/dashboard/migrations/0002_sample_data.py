from django.db import migrations
from datetime import datetime, timedelta
import random

def create_sample_data(apps, schema_editor):
    Surgeon = apps.get_model('dashboard', 'Surgeon')
    Procedure = apps.get_model('dashboard', 'Procedure')
    
    # Create surgeons
    surgeons = [
        Surgeon.objects.create(name='ARIYAN'),
        Surgeon.objects.create(name='BRADY'),
        Surgeon.objects.create(name='COIT'),
        Surgeon.objects.create(name='SMITH'),
        Surgeon.objects.create(name='JONES')
    ]
    
    # Create procedures
    start_date = datetime(2023, 1, 1)
    for _ in range(100):  # Create 100 sample procedures
        surgeon = random.choice(surgeons)
        days_offset = random.randint(0, 365)
        procedure_date = start_date + timedelta(days=days_offset)
        
        Procedure.objects.create(
            service='Melanoma',
            surgeon=surgeon,
            date=procedure_date,
            length_of_stay=random.randint(1, 10),
            complications=random.choice([True, False]),
            t_stage=random.choice(['T1', 'T2', 'T3', 'T4']),
            p_stage=random.choice(['I', 'II', 'III', 'IV']),
            procedure_time=random.uniform(30, 240)
        )

def remove_sample_data(apps, schema_editor):
    Surgeon = apps.get_model('dashboard', 'Surgeon')
    Procedure = apps.get_model('dashboard', 'Procedure')
    Procedure.objects.all().delete()
    Surgeon.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data, remove_sample_data),
    ] 