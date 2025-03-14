# Climetrics

A clinical metrics dashboard built with Django.

## Repository Structure

This repository is organized into two main directories:

- `frontend/`: Contains frontend templates, static files (CSS, JS, images)
- `backend/`: Contains all backend code (Django)

## Quick Start

The easiest way to run the application is to use the provided script:

```bash
# Run in development mode
./app.sh dev

# Run in production mode (not implemented yet)
./app.sh prod
```

This script will:
1. Set up the necessary environment
2. Install dependencies
3. Start the Django server

The application will be available at http://localhost:8000

## Manual Setup Instructions

If you prefer to set up the application manually, follow these instructions:

### Backend Setup

#### Environment Setup

Navigate to the backend directory:
```bash
cd backend
```

Using `uv` (recommended):
```bash
uv sync
```

This will install the following required packages:
- django
- pandas
- numpy
- scikit-learn
- statsmodels
- patsy
- and other dependencies

#### Database Configuration

Create a `.env` file in the `backend` directory with the following contents:

```bash
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>?sslmode=require
PGDATABASE=<database>
PGHOST=<host>
PGPORT=<port>
PGUSER=<username>
PGPASSWORD=<password>
```

Replace the placeholders (`<...>`) with your actual database credentials.

#### Django Setup

Initialize the database:
```bash
python manage.py migrate
```

Create a superuser (admin):
```bash
python manage.py createsuperuser
```

#### Running the Application

Start the Django development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Data Generation

### Simulation Data Generation

The repository includes a melanoma surgery simulation data generator for development and testing purposes.

#### Running the Generator

To generate simulation data:

```bash
cd backend
uv run simdata/generate_melanoma_data.py
```

This will create a `df_main.csv` file in the `backend/simdata` directory containing synthetic melanoma patient data.

You can customize the data generation by modifying the parameters at the top of the script:

```python
# Configuration parameters - Change these values as needed
N_PATIENTS = 2000                # Number of patients to generate
START_DATE = "2003-01-01"        # Start date for surgeries
END_DATE = "2018-12-31"          # End date for surgeries
OUTPUT_DIR = "."                  # Output directory (relative to script location)
OUTPUT_FILE = "df_main"          # Base filename for output
```

### Surgeon Rates Generation

The repository includes functionality to generate surgeon performance rates based on the simulation data, with a specific focus on melanoma procedures.

#### Input Data Format

The input data file (typically generated by the simulation data generator) should be a CSV file with the following columns:

Required columns:
- `eventId`: Unique identifier for each procedure
- `userId`: Surgeon identifier
- `surgDate`: Date of surgery (YYYY-MM-DD format)
- `yos`: Years of service
- `age`: Patient age
- `female`: Patient gender (0 = male, 1 = female)
- `bmi`: Patient BMI
- `thickness`: Melanoma thickness
- `ulceration`: Presence of ulceration (0 = no, 1 = yes)
- `slnd`: Sentinel Lymph Node Dissection performed (0 = no, 1 = yes)
- `posSlnd`: Positive SLND result (0 = negative, 1 = positive)
- `posSlndClnd`: Complete Lymph Node Dissection after positive SLND
- Complication columns (all 0 = no, 1 = yes):
  - `anyComp2`, `anyComp3`: Any complication (grade 2 or 3)
  - `woundInf2`, `woundInf3`: Wound infection
  - `cellulitis2`, `cellulitis3`: Cellulitis
  - `seroma2`, `seroma3`: Seroma
  - `graftComp2`, `graftComp3`: Graft complications

#### Running the Surgeon Rates Generator

To generate surgeon rates:

```bash
cd backend
python manage.py generate_rates
```

This will analyze the simulation data and generate surgeon performance metrics, saving the results to `backend/surgeon_rates/data/surgeon_rates.csv`.

#### Command Options

The generate_rates command supports several options:

```bash
python manage.py generate_rates --data-file=path/to/data.csv --output-dir=path/to/output --last-date=2022-12-31
```

- `--data-file`: Path to the input data file (default: df_main.csv)
- `--output-dir`: Directory to save the generated rates (default: surgeon_rates/data)
- `--last-date`: Last surgery date to include in the analysis (format: YYYY-MM-DD)

#### Output Files

The script generates two output files in the specified output directory:

1. `SurgeonRates_full.csv`: Complete results including all metrics and analysis details
2. `SurgeonRates.csv`: Trimmed version of the results with essential metrics

The results include:
- Complication rates by type and grade
- SLND (Sentinel Lymph Node Dissection) rates
- Positive SLND rates
- Complete node dissection rates
- Raw and adjusted rates
- Case counts and statistical metrics

#### Features

The surgeon rates analysis includes:
- Multiple imputation for handling missing data
- Risk-adjusted rates using logistic regression
- Support for different types of complications
- Analysis by time windows
- Automated data validation and error handling

#### Troubleshooting

If you encounter any issues with the surgeon rates generation:

1. Verify your input data format matches the required structure
2. Check that all required columns are present in your data file
3. Ensure all numeric columns contain valid numbers
4. Verify you have installed all required dependencies
5. Check the console output for specific error messages

The generated data can be used for development and testing without requiring access to real patient data.



