# Climetrics

A clinical metrics dashboard built with Django and React.

## Repository Structure

This repository is organized into two main directories:

- `frontend/`: Contains all frontend code (React)
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
1. Set up the necessary environments
2. Install dependencies
3. Start both the frontend and backend servers

The Django backend will be available at http://localhost:8000
The React frontend will be available at http://localhost:3000

## Manual Setup Instructions

If you prefer to set up the application manually, follow these instructions:

### 1. Backend Setup

#### Environment Setup

Navigate to the backend directory:
```bash
cd backend
```

Using `uv` (recommended):
```bash
uv sync
```

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

#### Running the Backend

Start the Django development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000/`

### 2. Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

Start the development server:
```bash
npm start
```

The frontend application will be available at `http://localhost:3000/`

## Simulation Data Generation

The repository includes a melanoma surgery simulation data generator for development and testing purposes.

### Running the Generator

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

The generated data can be used for development and testing without requiring access to real patient data.



