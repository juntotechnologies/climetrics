# Climetrics

A clinical metrics dashboard built with Django.

## Setup Instructions

### 1. Environment Setup

Using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
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
