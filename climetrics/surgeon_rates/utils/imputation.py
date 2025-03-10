import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from typing import List, Optional

class MultipleImputer:
    def __init__(self, n_imputations: int = 5, random_state: Optional[int] = None):
        """
        Initialize the multiple imputation handler
        
        Args:
            n_imputations: Number of imputations to generate
            random_state: Random seed for reproducibility
        """
        self.n_imputations = n_imputations
        self.random_state = random_state
        
    def generate_multiple_imputations(
        self,
        df: pd.DataFrame,
        vars_to_impute: List[str],
        patient_id: str = 'patient_id'
    ) -> List[pd.DataFrame]:
        """
        Generate multiple imputations for missing values
        
        Args:
            df: Input DataFrame
            vars_to_impute: List of variables to impute
            patient_id: Name of the patient ID column
            
        Returns:
            List of DataFrames with imputed values
        """
        # Validate inputs
        if not all(var in df.columns for var in vars_to_impute):
            raise ValueError("Not all variables to impute exist in the dataset")
            
        # Create subset with variables to impute
        imputation_df = df[vars_to_impute + [patient_id]].copy()
        
        # Initialize imputer
        imputer = IterativeImputer(
            max_iter=10,
            random_state=self.random_state,
            sample_posterior=True
        )
        
        # Generate multiple imputations
        imputed_dfs = []
        for i in range(self.n_imputations):
            # Perform imputation
            imputed_values = imputer.fit_transform(imputation_df[vars_to_impute])
            
            # Create DataFrame with imputed values
            imputed_df = pd.DataFrame(
                imputed_values,
                columns=vars_to_impute
            )
            imputed_df[patient_id] = imputation_df[patient_id].values
            
            imputed_dfs.append(imputed_df)
            
        return imputed_dfs
        
    @staticmethod
    def validate_imputations(
        original_df: pd.DataFrame,
        imputed_dfs: List[pd.DataFrame],
        vars_to_impute: List[str]
    ) -> bool:
        """
        Validate the imputed datasets
        
        Args:
            original_df: Original DataFrame
            imputed_dfs: List of imputed DataFrames
            vars_to_impute: Variables that were imputed
            
        Returns:
            True if validation passes, raises ValueError otherwise
        """
        # Check that we have the expected number of imputed datasets
        if len(imputed_dfs) == 0:
            raise ValueError("No imputed datasets provided")
            
        # Check that all imputed datasets have the same shape
        shapes = [df.shape for df in imputed_dfs]
        if len(set(shapes)) > 1:
            raise ValueError("Imputed datasets have different shapes")
            
        # Check that imputed values are within reasonable bounds
        for var in vars_to_impute:
            original_stats = original_df[var].describe()
            
            for imp_df in imputed_dfs:
                imp_stats = imp_df[var].describe()
                
                # Check if imputed means are within 2 standard deviations
                if abs(original_stats['mean'] - imp_stats['mean']) > 2 * original_stats['std']:
                    raise ValueError(f"Imputed values for {var} may be unreasonable")
                    
        return True 