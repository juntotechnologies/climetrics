
## Database Configuration

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
uv run manage.py migrate
```

Create a superuser (admin):
```bash
uv run manage.py createsuperuser
```

#### Running the Application

Start the Django development server:
```bash
uv run manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`