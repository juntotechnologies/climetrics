
# To set up the `uv` environment, run

`uv sync`

# To set up the database and relevant credentials

`touch .env` and add these contents with the filled out info:

```bash
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>?sslmode=require
PGDATABASE=<database>
PGHOST=<host>
PGPORT=<port>
PGUSER=<username>
PGPASSWORD=<password>
```

# To run the app, do

`uv run streamlit run main.py`
