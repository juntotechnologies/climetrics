import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import traceback
from tqdm import tqdm

from surgeon_rates.utils.rate_generator import RateGenerator
from surgeon_rates.utils.imputation import MultipleImputer

def generate_melanoma_rates(
    data_path: str,
    output_path: str,
    last_surgery_date: datetime = None
) -> None:
    """
    Generate surgeon rates for melanoma procedures

    Args:
        data_path: Path to the input data file
        output_path: Path to save the results
        last_surgery_date: Last date to include in the analysis
    """
    try:
        print(f"Loading data from {data_path}")
        all_data = pd.read_csv(data_path, dtype={
            'eventId': str,
            'userId': str,
            'surgDate': str,
            'yos': float,
            'age': float,
            'female': float,
            'bmi': float,
            'thickness': float,
            'ulceration': float,
            'mitoticIndex': float,
            'site': str,
            'slnd': float,
            'posSlnd': float,
            'posSlndClnd': float,
            'anyComp2': float,
            'anyComp3': float,
            'woundInf2': float,
            'woundInf3': float,
            'cellulitis2': float,
            'cellulitis3': float,
            'seroma2': float,
            'seroma3': float,
            'graftComp2': float,
            'graftComp3': float
        })

        print(f"Successfully loaded data with {len(all_data)} rows")
        print("Columns found:", all_data.columns.tolist())
        print("\nSample of data:")
        print(all_data.head())
        print("\nData types:")
        print(all_data.dtypes)

        # Convert surgDate to datetime
        all_data['surgDate'] = pd.to_datetime(all_data['surgDate'])

        # Initialize tools
        rate_generator = RateGenerator()
        imputer = MultipleImputer(n_imputations=5)

        # Variables to impute
        vars_to_impute = ['age', 'female', 'bmi', 'thickness', 'ulceration']

        print("\nGenerating imputations for variables:", vars_to_impute)
        imputed_values = imputer.generate_multiple_imputations(
            df=all_data,
            vars_to_impute=vars_to_impute,
            patient_id='eventId'
        )
        print(f"Successfully generated {len(imputed_values)} imputations")

        # Generate date IDs for analysis windows
        date_ids = _generate_date_ids(all_data, 'surgDate')
        print("\nGenerated date IDs:", date_ids[:5], "...")

        # Calculate total iterations for progress tracking
        comp_types = ['ANY', 'WOUND', 'CELLULITIS', 'SEROMA', 'GRAFT']
        comp_grades = ['COMPGRADE2', 'COMPGRADE3']

        total_iterations = (
            len(comp_types) * len(comp_grades) * len(date_ids) +  # Complications
            len(date_ids) +  # SLND
            len(date_ids) +  # Positive SLND
            len(date_ids)    # Complete node dissection
        )

        print(f"\nTotal models to process: {total_iterations}")

        # Initialize results DataFrame
        user_results = pd.DataFrame()

        # Use tqdm for the main loop
        pbar = tqdm(total=total_iterations, desc="Processing models")

        # Generate complication rates
        comp_types = ['ANY', 'WOUND', 'CELLULITIS', 'SEROMA', 'GRAFT']
        comp_grades = ['COMPGRADE2', 'COMPGRADE3']

        for comp_type in comp_types:
            for grade in comp_grades:
                for date_id in date_ids:
                    model_id = f"COMP.{comp_type}.{grade}.{date_id}"
                    outcome = _map_complication_outcome(comp_type, grade)

                    results = rate_generator.generate_rate(
                        df=all_data,
                        outcome=outcome,
                        model_id=model_id,
                        model_type='LOGISTIC',
                        date_var='surgDate',
                        user_id_var='userId',
                        patient_id_var='eventId',
                        weight_var='yos',
                        imputed_values=imputed_values,
                        date=last_surgery_date
                    )

                    user_results = pd.concat([user_results, results])
                    pbar.update(1)
                    pbar.set_postfix({'Current': f"{comp_type}-{grade}"})

        # Generate SLND rates
        slnd_model_ids = [f"SLND.{date_id}" for date_id in date_ids]
        for model_id in slnd_model_ids:
            results = rate_generator.generate_rate(
                df=all_data,
                outcome='slnd',
                model_id=model_id,
                model_type='LOGISTIC',
                date_var='surgDate',
                user_id_var='userId',
                patient_id_var='eventId',
                weight_var='yos',
                imputed_values=imputed_values,
                date=last_surgery_date
            )
            user_results = pd.concat([user_results, results])
            pbar.update(1)
            pbar.set_postfix({'Current': 'SLND'})

        # Generate positive SLND rates
        pos_slnd_model_ids = [f"POSSLND.{date_id}" for date_id in date_ids]
        for model_id in pos_slnd_model_ids:
            results = rate_generator.generate_rate(
                df=all_data[all_data['slnd'] == 1],
                outcome='posSlnd',
                model_id=model_id,
                model_type='LOGISTIC',
                date_var='surgDate',
                user_id_var='userId',
                patient_id_var='eventId',
                weight_var='yos',
                imputed_values=imputed_values,
                date=last_surgery_date
            )
            user_results = pd.concat([user_results, results])
            pbar.update(1)
            pbar.set_postfix({'Current': 'POS-SLND'})

        # Generate complete node dissection rates
        clnd_model_ids = [f"CLND.{date_id}" for date_id in date_ids]
        for model_id in clnd_model_ids:
            results = rate_generator.generate_rate(
                df=all_data[all_data['posSlnd'] == 1],
                outcome='complete_node_dissection',
                model_id=model_id,
                model_type='LOGISTIC',
                date_var='surgDate',
                user_id_var='userId',
                patient_id_var='eventId',
                weight_var='yos',
                imputed_values=imputed_values,
                date=last_surgery_date
            )
            user_results = pd.concat([user_results, results])
            pbar.update(1)
            pbar.set_postfix({'Current': 'CLND'})

        pbar.close()

        # Save results
        print("\nSaving results...")
        _save_results(user_results, output_path)
        print("Successfully saved results")

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        return

def _generate_date_ids(df: pd.DataFrame, date_col: str) -> List[str]:
    """Generate date IDs for different analysis windows"""
    thickness_categories = ['ALLLENGTH', 'LESSTHANPT8MM', 'PT8MMTO1MM', 'GRTHAN1MM']
    dates = df[date_col].dt.strftime('%Y%m%d')
    return [f"{cat}.DATE{date}" for cat in thickness_categories for date in dates.unique()]

def _map_complication_outcome(comp_type: str, grade: str) -> str:
    """Map complication type and grade to outcome variable name"""
    grade_num = grade[-1]
    outcomes = {
        'ANY': f'anyComp{grade_num}',
        'WOUND': f'woundInf{grade_num}',
        'CELLULITIS': f'cellulitis{grade_num}',
        'SEROMA': f'seroma{grade_num}',
        'GRAFT': f'graftComp{grade_num}'
    }
    return outcomes[comp_type]

def _save_results(results: pd.DataFrame, output_path: str) -> None:
    """Save full and trimmed results"""
    # Create output directory if it doesn't exist
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save full results
    results.to_csv(output_dir / 'SurgeonRates_full.csv', index=False)

    # Save trimmed results (excluding certain columns or filtering as needed)
    trimmed_results = results.copy()
    # Add any trimming logic here
    trimmed_results.to_csv(output_dir / 'SurgeonRates.csv', index=False)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate melanoma surgeon rates')
    parser.add_argument('--data-path', required=True, help='Path to input data file')
    parser.add_argument('--output-path', required=True, help='Path to save results')
    parser.add_argument('--last-surgery-date', help='Last surgery date to include (YYYY-MM-DD)')

    args = parser.parse_args()

    last_date = datetime.strptime(args.last_surgery_date, '%Y-%m-%d') if args.last_surgery_date else None

    generate_melanoma_rates(args.data_path, args.output_path, last_date)
