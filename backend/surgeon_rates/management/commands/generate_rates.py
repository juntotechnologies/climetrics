import os
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from pathlib import Path

from surgeon_rates.generate_melanoma_rates import generate_melanoma_rates


class Command(BaseCommand):
    help = 'Generate surgeon rates for melanoma procedures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-file',
            type=str,
            default='df_main.csv',
            help='Input data file (default: df_main.csv)'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='surgeon_rates/data',
            help='Output directory for generated rates (default: surgeon_rates/data)'
        )
        parser.add_argument(
            '--last-date',
            type=str,
            help='Last surgery date to include (format: YYYY-MM-DD)'
        )

    def handle(self, *args, **options):
        # Get the base directory
        base_dir = Path(settings.BASE_DIR)
        
        # Determine the data file path
        data_file = options['data_file']
        if not os.path.isabs(data_file):
            if os.path.exists(base_dir / 'simdata' / data_file):
                data_path = str(base_dir / 'simdata' / data_file)
            elif os.path.exists(base_dir / data_file):
                data_path = str(base_dir / data_file)
            else:
                self.stderr.write(self.style.ERROR(f'Data file not found: {data_file}'))
                return
        else:
            data_path = data_file
            
        # Ensure output directory exists
        output_dir = options['output_dir']
        if not os.path.isabs(output_dir):
            output_dir = str(base_dir / output_dir)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Parse last date if provided
        last_date = None
        if options['last_date']:
            try:
                last_date = datetime.strptime(options['last_date'], '%Y-%m-%d')
            except ValueError:
                self.stderr.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD'))
                return
        
        # Generate the rates
        output_path = os.path.join(output_dir, 'surgeon_rates.csv')
        
        self.stdout.write(self.style.SUCCESS(f'Generating surgeon rates...'))
        self.stdout.write(f'Input data: {data_path}')
        self.stdout.write(f'Output file: {output_path}')
        
        try:
            generate_melanoma_rates(
                data_path=data_path,
                output_path=output_path,
                last_surgery_date=last_date
            )
            self.stdout.write(self.style.SUCCESS('Successfully generated surgeon rates'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error generating rates: {str(e)}')) 