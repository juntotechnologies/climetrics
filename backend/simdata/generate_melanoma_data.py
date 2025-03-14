import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import os

# Configuration parameters - Change these values as needed
N_PATIENTS = 2000
START_DATE = "2003-01-01"
END_DATE = "2018-12-31"
OUTPUT_DIR = "."  # Save in current directory (simdata)
OUTPUT_FILE = "df_main"
RANDOM_SEED = 20230728
GENERATE_RDS = False  # Set to True if you want to generate RDS file for R

def generate_melanoma_data(n_patients=2000, start_date="2003-01-01", end_date="2018-12-31", seed=20230728):
    """
    Generate simulated data for melanoma surgeries.
    
    Parameters:
    -----------
    n_patients : int
        Number of patients to generate
    start_date : str
        Start date for surgeries (YYYY-MM-DD)
    end_date : str
        End date for surgeries (YYYY-MM-DD)
    seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    DataFrame with simulated melanoma surgery data
    """
    # Set random seed for reproducibility
    np.random.seed(seed)
    random.seed(seed)
    
    # Convert dates to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Generate random surgery dates
    days_range = (end_date - start_date).days
    random_days = np.random.randint(0, days_range, n_patients)
    # Convert numpy.int64 to regular Python int to avoid TypeError with timedelta
    surgery_dates = [start_date + timedelta(days=int(days)) for days in random_days]
    
    # Generate patient IDs
    event_ids = [str(uuid.uuid4())[:8] for _ in range(n_patients)]
    
    # Generate surgeon IDs (using a small set of surgeons)
    surgeon_names = ["ARIYAN", "BRADY", "COIT", "SMITH", "JONES", "PATEL", "WONG"]
    user_ids = np.random.choice(surgeon_names, n_patients)
    
    # Year of surgery
    yos = [date.year for date in surgery_dates]
    
    # Patient demographics and tumor characteristics
    ages = np.random.normal(60, 15, n_patients)  # Age centered around 60 with SD of 15
    ages = np.clip(ages, 18, 100).astype(int)  # Constrain to reasonable age range
    
    female = np.random.binomial(1, 0.45, n_patients)  # 45% female
    
    # BMI with some missing values (about 5%)
    bmi = np.random.normal(27, 5, n_patients)  # BMI centered around 27 with SD of 5
    bmi = np.clip(bmi, 16, 50, out=bmi)  # Constrain to reasonable BMI range
    bmi_missing_idx = np.random.choice(n_patients, int(n_patients * 0.05), replace=False)
    bmi[bmi_missing_idx] = np.nan
    
    # Tumor thickness in mm (log-normal distribution to skew toward thinner tumors)
    thickness = np.exp(np.random.normal(0, 1, n_patients))
    thickness = np.clip(thickness, 0.1, 15, out=thickness)  # Constrain to reasonable range
    thickness_missing_idx = np.random.choice(n_patients, int(n_patients * 0.1), replace=False)
    thickness[thickness_missing_idx] = np.nan
    
    # Ulceration (more likely in thicker tumors)
    ulceration_prob = 1 / (1 + np.exp(-(thickness - 2)))  # Logistic function centered at 2mm
    ulceration = [np.random.binomial(1, prob) if not np.isnan(thick) else np.nan 
                 for prob, thick in zip(ulceration_prob, thickness)]
    
    # Mitotic index (0-10+, related to thickness)
    mitotic_index = np.round(thickness * 0.8 + np.random.normal(0, 1, n_patients))
    mitotic_index = np.clip(mitotic_index, 0, 10, out=mitotic_index)
    mitotic_missing_idx = np.random.choice(n_patients, int(n_patients * 0.15), replace=False)
    mitotic_index[mitotic_missing_idx] = np.nan
    
    # Generate sites for melanoma
    site_options = [
        "TRUNK", "ARM", "LEG", "SCALP", "NECK", "HAND", "FOOT", 
        "FACE", "EAR", "OCULAR", "EYELID", "LIP", "MUCOSAL"
    ]
    site_probs = [0.25, 0.15, 0.15, 0.08, 0.08, 0.05, 0.05, 0.08, 0.04, 0.02, 0.02, 0.02, 0.01]
    sites = np.random.choice(site_options, n_patients, p=site_probs)
    
    # Generate sentinel lymph node dissection information
    # SLND more likely for thicker tumors
    slnd_prob = 1 / (1 + np.exp(-(thickness - 0.8) * 2))  # Logistic function centered at 0.8mm
    slnd = [np.random.binomial(1, prob) if not np.isnan(thick) else np.nan 
           for prob, thick in zip(slnd_prob, thickness)]
    
    # About 30% of SLND are missing in the data (per the comments in the R code)
    slnd_missing_idx = np.random.choice(n_patients, int(n_patients * 0.3), replace=False)
    for idx in slnd_missing_idx:
        slnd[idx] = np.nan
    
    # Generate positive SLND results (only for those who got SLND)
    pos_slnd = [np.random.binomial(1, 0.2) if s == 1 else (np.nan if np.isnan(s) else 0) 
               for s in slnd]
    
    # Complete lymph node dissection after positive SLND
    pos_slnd_clnd = [np.random.binomial(1, 0.7) if p == 1 else (np.nan if np.isnan(p) else 0) 
                    for p in pos_slnd]
    
    # Generate complications (more likely with increased age, BMI, thickness)
    # Base complication probability factors
    age_factor = (ages - 50) / 50  # Centered at age 50
    
    # Handle NaN values for BMI
    bmi_factor = np.zeros(n_patients)
    mask_bmi_valid = ~np.isnan(bmi)
    bmi_factor[mask_bmi_valid] = (bmi[mask_bmi_valid] - 25) / 10   # Centered at BMI 25
    
    # Handle NaN values for thickness
    thickness_factor = np.zeros(n_patients)
    mask_thickness_valid = ~np.isnan(thickness)
    thickness_factor[mask_thickness_valid] = thickness[mask_thickness_valid] / 3  # Normalized by 3mm
    
    # Compute base probability for any complication - handling NaNs
    base_comp_prob = 0.08 + 0.02 * age_factor + 0.03 * bmi_factor + 0.03 * thickness_factor
    base_comp_prob = np.clip(base_comp_prob, 0.01, 0.5)
    
    # For patients with missing BMI or thickness, use a base probability based on age only
    mask_any_missing = np.isnan(bmi) | np.isnan(thickness)
    base_comp_prob[mask_any_missing] = 0.08 + 0.02 * age_factor[mask_any_missing]
    base_comp_prob = np.clip(base_comp_prob, 0.01, 0.5)
    
    # Initialize complication arrays
    anyComp2 = np.zeros(n_patients, dtype=int)
    anyComp3 = np.zeros(n_patients, dtype=int)
    woundInf2 = np.zeros(n_patients, dtype=int)
    woundInf3 = np.zeros(n_patients, dtype=int)
    cellulitis2 = np.zeros(n_patients, dtype=int)
    cellulitis3 = np.zeros(n_patients, dtype=int)
    seroma2 = np.zeros(n_patients, dtype=int)
    seroma3 = np.zeros(n_patients, dtype=int)
    graftComp2 = np.zeros(n_patients, dtype=int)
    graftComp3 = np.zeros(n_patients, dtype=int)
    
    # Generate complications for each patient
    for i in range(n_patients):
        # Any complication
        if np.random.random() < base_comp_prob[i]:
            # Determine grade (2 or 3)
            if np.random.random() < 0.2:  # 20% chance of grade 3
                anyComp3[i] = 1
                grade = 3
            else:
                anyComp2[i] = 1
                grade = 2
            
            # Assign specific complication types (a patient can have multiple)
            comp_types = ["woundInf", "cellulitis", "seroma", "graftComp"]
            comp_probs = [0.4, 0.3, 0.2, 0.1]  # Probabilities for each complication type
            
            for comp_type, prob in zip(comp_types, comp_probs):
                if np.random.random() < prob:
                    if comp_type == "woundInf":
                        if grade == 2:
                            woundInf2[i] = 1
                        else:
                            woundInf3[i] = 1
                    elif comp_type == "cellulitis":
                        if grade == 2:
                            cellulitis2[i] = 1
                        else:
                            cellulitis3[i] = 1
                    elif comp_type == "seroma":
                        if grade == 2:
                            seroma2[i] = 1
                        else:
                            seroma3[i] = 1
                    elif comp_type == "graftComp":
                        if grade == 2:
                            graftComp2[i] = 1
                        else:
                            graftComp3[i] = 1
    
    # Create DataFrame
    data = {
        "eventId": event_ids,
        "userId": user_ids,
        "surgDate": surgery_dates,
        "yos": yos,
        "age": ages,
        "female": female,
        "bmi": bmi,
        "thickness": thickness,
        "ulceration": ulceration,
        "mitoticIndex": mitotic_index,
        "site": sites,
        "slnd": slnd,
        "posSlnd": pos_slnd,
        "posSlndClnd": pos_slnd_clnd,
        "anyComp2": anyComp2,
        "anyComp3": anyComp3,
        "woundInf2": woundInf2,
        "woundInf3": woundInf3,
        "cellulitis2": cellulitis2,
        "cellulitis3": cellulitis3,
        "seroma2": seroma2,
        "seroma3": seroma3,
        "graftComp2": graftComp2,
        "graftComp3": graftComp3
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Generating melanoma surgery data for {N_PATIENTS} patients...")
    print(f"Date range: {START_DATE} to {END_DATE}")
    
    # Generate the data
    df = generate_melanoma_data(
        n_patients=N_PATIENTS,
        start_date=START_DATE,
        end_date=END_DATE,
        seed=RANDOM_SEED
    )
    
    # Save as CSV
    csv_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_FILE}.csv")
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")
    
    # Save as RDS if configured
    if GENERATE_RDS:
        try:
            import pyreadr
            rds_path = os.path.join(OUTPUT_DIR, f"{OUTPUT_FILE}.Rds")
            
            # Convert datetime to string for easier R compatibility
            df_for_r = df.copy()
            df_for_r['surgDate'] = df_for_r['surgDate'].astype(str)
            
            # Save as RDS
            pyreadr.write_rds(rds_path, df_for_r)
            print(f"RDS file saved to {rds_path}")
        except ImportError:
            print("WARNING: pyreadr not installed. RDS file not created.")
            print("To create an RDS file, install pyreadr: pip install pyreadr")
    
    print(f"Successfully generated data for {len(df)} patients") 