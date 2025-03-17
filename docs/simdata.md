
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