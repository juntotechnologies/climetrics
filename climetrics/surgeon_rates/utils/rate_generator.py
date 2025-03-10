import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any

class RateGenerator:
    def __init__(self):
        self.covariates = ['age', 'female', 'bmi', 'thickness', 'ulceration']
        
    def generate_rate(
        self,
        df: pd.DataFrame,
        outcome: str,
        model_id: str,
        model_type: str = "LOGISTIC",
        date_var: str = "surgDate",
        user_id_var: str = "userId",
        patient_id_var: str = "eventId",
        weight_var: str = "yos",
        avg_covariates: Optional[Dict] = None,
        imputed_values: Optional[List[pd.DataFrame]] = None,
        pt_risk_groups: Optional[Dict] = None,
        date: datetime = None,
        survival: bool = True
    ) -> pd.DataFrame:
        """
        Generate adjusted and unadjusted rates for surgeons based on the provided data
        
        Args:
            df: Input DataFrame containing the procedure data
            outcome: Name of the outcome column
            model_id: Identifier for the model
            model_type: Type of model (LOGISTIC, LINEAR, SURVIVAL)
            date_var: Name of the date column
            user_id_var: Name of the surgeon ID column
            patient_id_var: Name of the patient ID column
            weight_var: Name of the weight column
            avg_covariates: Pre-calculated average covariates
            imputed_values: List of DataFrames with imputed values
            pt_risk_groups: Dictionary of patient risk groups
            date: Reference date for the analysis
            survival: Whether higher values are better (True) or worse (False)
            
        Returns:
            DataFrame containing the calculated rates
        """
        # Convert data types for required columns
        df = df.copy()
        for col in self.covariates + [outcome]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Input validation
        if not all(col in df.columns for col in [outcome] + self.covariates):
            missing_cols = [col for col in [outcome] + self.covariates if col not in df.columns]
            raise ValueError(f"Missing required columns in the dataset: {missing_cols}")
            
        model_type = model_type.upper()
        if model_type not in ["LINEAR", "LOGISTIC", "SURVIVAL"]:
            raise ValueError("Invalid model type")
            
        # Prepare the data
        df = self._prepare_data(df, outcome, weight_var)
        
        # Handle imputed values if provided
        if imputed_values is not None:
            results = self._process_imputed_data(
                df, imputed_values, outcome, model_type, avg_covariates
            )
        else:
            results = self._process_single_dataset(
                df, outcome, model_type, avg_covariates
            )
            
        # Add metadata to results
        results['model_id'] = model_id
        results['date'] = date or datetime.now()
        
        return results
        
    def _prepare_data(
        self,
        df: pd.DataFrame,
        outcome: str,
        weight_var: str
    ) -> pd.DataFrame:
        """Prepare the dataset for analysis"""
        # Remove rows with missing weights
        df = df[df[weight_var].notna()].copy()
        
        # Convert weight to numeric if needed
        df[weight_var] = pd.to_numeric(df[weight_var], errors='coerce')
        
        # Calculate model weights
        max_weight = df[weight_var].max()
        df['model_weight'] = 1 / np.sqrt(max_weight - df[weight_var] + 1)
        
        return df
        
    def _process_single_dataset(
        self,
        df: pd.DataFrame,
        outcome: str,
        model_type: str,
        avg_covariates: Optional[Dict]
    ) -> pd.DataFrame:
        """Process a single dataset without imputation"""
        # Get complete cases
        analysis_df = df.dropna(subset=[outcome] + self.covariates)
        
        if len(analysis_df) == 0:
            raise ValueError("No complete cases available for analysis")
            
        # Calculate rates
        if model_type == "LOGISTIC":
            return self._calculate_logistic_rates(
                analysis_df,
                outcome,
                avg_covariates
            )
        elif model_type == "LINEAR":
            return self._calculate_linear_rates(
                analysis_df,
                outcome,
                avg_covariates
            )
        else:  # SURVIVAL
            return self._calculate_survival_rates(
                analysis_df,
                outcome,
                avg_covariates
            )
            
    def _calculate_logistic_rates(
        self,
        df: pd.DataFrame,
        outcome: str,
        avg_covariates: Optional[Dict]
    ) -> pd.DataFrame:
        """Calculate rates using logistic regression"""
        # Prepare X and y
        X = df[self.covariates].astype(float)
        y = df[outcome].astype(float)
        weights = df['model_weight'].astype(float)
        
        # Fit the model
        model = LogisticRegression(class_weight='balanced')
        model.fit(X, y, sample_weight=weights)
        
        # Calculate rates for each surgeon
        results = []
        for surgeon_id in df['userId'].unique():
            surgeon_data = df[df['userId'] == surgeon_id]
            
            # Calculate raw rate
            raw_rate = surgeon_data[outcome].astype(float).mean()
            
            # Calculate adjusted rate using average covariates
            if avg_covariates is not None:
                adj_X = pd.DataFrame([avg_covariates])
                adj_rate = model.predict_proba(adj_X)[0][1]
            else:
                adj_rate = raw_rate
                
            results.append({
                'surgeon_id': surgeon_id,
                'rate': adj_rate,
                'raw_rate': raw_rate,
                'cases': len(surgeon_data),
                'method': 'logistic_regression'
            })
            
        return pd.DataFrame(results)
        
    def _process_imputed_data(
        self,
        df: pd.DataFrame,
        imputed_values: List[pd.DataFrame],
        outcome: str,
        model_type: str,
        avg_covariates: Optional[Dict]
    ) -> pd.DataFrame:
        """Process multiple imputed datasets and combine results"""
        # Calculate rates for each imputed dataset
        all_results = []
        for imp_df in imputed_values:
            # Create a copy of the original dataframe
            analysis_df = df.copy()
            
            # Update the covariates with imputed values
            for col in self.covariates:
                if col in imp_df.columns:
                    analysis_df[col] = imp_df[col]
            
            # Process the dataset
            try:
                results = self._process_single_dataset(
                    analysis_df,
                    outcome,
                    model_type,
                    avg_covariates
                )
                all_results.append(results)
            except Exception as e:
                print(f"Error processing imputed dataset: {str(e)}")
                continue
            
        if not all_results:
            raise ValueError("No valid results from any imputed dataset")
            
        # Combine results using Rubin's rules
        combined_results = self._combine_imputed_results(all_results)
        return combined_results
        
    def _combine_imputed_results(
        self,
        results_list: List[pd.DataFrame]
    ) -> pd.DataFrame:
        """Combine results from multiple imputations using Rubin's rules"""
        # Calculate mean estimates across imputations
        combined = pd.concat(results_list).groupby('surgeon_id').agg({
            'rate': 'mean',
            'raw_rate': 'mean',
            'cases': 'first',
            'method': 'first'
        }).reset_index()
        
        return combined 