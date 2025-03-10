# Climetrics - Surgeon Rates Analysis

This package provides tools for analyzing surgeon performance rates, with a specific focus on melanoma procedures.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/climetrics.git
cd climetrics
```

2. Install the package and its dependencies:
```bash
pip install -e .
```

This will install the following required packages:
- pandas
- numpy
- scikit-learn
- statsmodels
- patsy

## Input Data Format

The input data file should be a CSV file with the following columns:

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

## Running the Analysis

You can run the surgeon rates analysis using the following command:

```bash
python -m climetrics.surgeon_rates.generate_melanoma_rates \
    --data-path /path/to/your/data.csv \
    --output-path /path/to/output/directory \
    --last-surgery-date YYYY-MM-DD
```

Arguments:
- `--data-path`: Path to your input CSV file
- `--output-path`: Directory where results will be saved
- `--last-surgery-date`: (Optional) Last surgery date to include in the analysis

Example:
```bash
python -m climetrics.surgeon_rates.generate_melanoma_rates \
    --data-path "C:\GitHub\climetrics\data\df_main.csv" \
    --output-path "C:\GitHub\climetrics\results" \
    --last-surgery-date "2023-12-31"
```

## Output Files

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

## Features

- Multiple imputation for handling missing data
- Risk-adjusted rates using logistic regression
- Support for different types of complications
- Analysis by time windows
- Automated data validation and error handling

## Troubleshooting

If you encounter any issues:

1. Verify your input data format matches the required structure
2. Check that all required columns are present in your data file
3. Ensure all numeric columns contain valid numbers
4. Verify you have installed all required dependencies
5. Check the console output for specific error messages

## Contributing

Feel free to submit issues and enhancement requests!



