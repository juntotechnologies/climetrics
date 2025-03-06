# Climetrics

A clinical metrics dashboard built with Django.

## Setup Instructions

### 1. Environment Setup

Using `uv` (recommended):
```bash
uv sync
```

### 2. Database Configuration

Create a `.env` file in the root directory with the following contents:

```bash
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>?sslmode=require
PGDATABASE=<database>
PGHOST=<host>
PGPORT=<port>
PGUSER=<username>
PGPASSWORD=<password>
```

Replace the placeholders (`<...>`) with your actual database credentials.

### 3. Django Setup

Initialize the database:
```bash
python manage.py migrate
```

Create a superuser (admin):
```bash
python manage.py createsuperuser
```

### 4. Running the Application

Start the Django development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Simulation Data Generation

The repository includes a melanoma surgery simulation data generator for development and testing purposes.

### Running the Generator

To generate simulation data:

```bash
uv run simdata/generate_melanoma_data.py
```

This will create a `df_main.csv` file in the `simdata` directory containing synthetic melanoma patient data.

You can customize the data generation by modifying the parameters at the top of the script:

```python
# Configuration parameters - Change these values as needed
N_PATIENTS = 2000                # Number of patients to generate
START_DATE = "2003-01-01"        # Start date for surgeries
END_DATE = "2018-12-31"          # End date for surgeries
OUTPUT_DIR = "."                  # Output directory (relative to script location)
OUTPUT_FILE = "df_main"          # Base filename for output
```

The generated data can be used for development and testing without requiring access to real patient data.



