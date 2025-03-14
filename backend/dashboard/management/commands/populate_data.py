from django.core.management.base import BaseCommand
from dashboard.models import Surgeon, Procedure
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Create surgeons
        surgeons = []
        for i in range(5):
            surgeon, created = Surgeon.objects.get_or_create(name=f'Surgeon {i+1}')
            surgeons.append(surgeon)
            if created:
                self.stdout.write(f'Created surgeon: {surgeon.name}')

        # Create procedures
        services = ['Melanoma', 'Gastrectomy', 'Whipple']
        t_stages = ['T1', 'T2', 'T3', 'T4']
        p_stages = ['I', 'II', 'III', 'IV']

        for _ in range(100):
            service = random.choice(services)
            surgeon = random.choice(surgeons)
            
            Procedure.objects.create(
                service=service,
                surgeon=surgeon,
                date=datetime.now() - timedelta(days=random.randint(0, 365)),
                length_of_stay=random.randint(1, 14),
                complications=random.choice([True, False]),
                t_stage=random.choice(t_stages),
                p_stage=random.choice(p_stages),
                procedure_time=random.uniform(60, 300)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated database')) 