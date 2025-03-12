# Melanoma Surgery Simulation Data Generator

This Python script generates simulated data for melanoma surgeries to support development and testing of the analysis pipeline.

## Dependencies Installation

This script requires pandas and numpy. You can install them using `uv` from Astral:

```bash
# Install uv if you haven't already
curl -sSf https://astral.sh/uv/install.sh | bash

# Install dependencies
uv pip install pandas numpy

# Optional: for R integration
uv pip install pyreadr
```

## Usage

Simply run the script directly with Python:

```
python generate_melanoma_data.py
```

This will generate melanoma surgery data based on the parameters set at the top of the script and save it as CSV in the `data` directory.

## Customizing Data Generation

To customize the data generation, simply edit the parameters at the top of the script:

```python
# Configuration parameters - Change these values as needed
N_PATIENTS = 2000                # Number of patients to generate
START_DATE = "2003-01-01"        # Start date for surgeries
END_DATE = "2018-12-31"          # End date for surgeries
OUTPUT_DIR = "data"              # Directory for output files
OUTPUT_FILE = "df_main"          # Base filename for output
RANDOM_SEED = 20230728           # Random seed for reproducibility
GENERATE_RDS = False             # Set to True to generate RDS file for R
```

## Generated Data Fields

The simulated dataset includes the following fields:

- **eventId**: Unique patient identifier
- **userId**: Surgeon identifier
- **surgDate**: Date of surgery
- **yos**: Year of surgery
- **age**: Patient age
- **female**: Patient gender (1=female, 0=male)
- **bmi**: Body mass index
- **thickness**: Tumor thickness in millimeters
- **ulceration**: Presence of ulceration (1=yes, 0=no)
- **mitoticIndex**: Mitotic index (0-10+)
- **site**: Location of melanoma (e.g., TRUNK, ARM, LEG, etc.)
- **slnd**: Sentinel lymph node dissection performed (1=yes, 0=no)
- **posSlnd**: Positive sentinel lymph node (1=yes, 0=no)
- **posSlndClnd**: Complete lymph node dissection after positive SLND (1=yes, 0=no)
- **Complications**: Various complication fields with grade (2 or 3)
  - **anyComp2**, **anyComp3**: Any complication
  - **woundInf2**, **woundInf3**: Wound infection
  - **cellulitis2**, **cellulitis3**: Cellulitis
  - **seroma2**, **seroma3**: Seroma
  - **graftComp2**, **graftComp3**: Graft complications 