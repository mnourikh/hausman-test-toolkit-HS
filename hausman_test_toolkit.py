
# Hausman Test Toolkit
# This script provides tools for performing Hausman tests on panel data.

import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS, RandomEffects, compare

def preprocess_panel_data(df):
    # Combines 'country' and 'code' levels into one to create a two-level MultiIndex
    df['entity'] = df['country'] + '_' + df['code'].astype(str)
    df.set_index(['entity', 'year'], inplace=True)  # Two-level MultiIndex
    df.drop(['country', 'code', 'const'], axis=1, inplace=True)  # Drop redundant columns

    # Data Cleaning
    df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinities with NaN
    df.dropna(inplace=True)  # Drop rows with NaN values

    return df

def perform_hausman_test(df, independent_vars, name, output_dir="results"):
    # Ensures the data is panel-structured and performs the Hausman test
    dependent_var = "log_dollar"

    # Construct the formula for fixed and random effects models
    formula = f"{dependent_var} ~ {' + '.join(independent_vars)}"

    # Fit the fixed effects model
    fixed_effects = PanelOLS.from_formula(formula + " + EntityEffects", df, check_rank=False)
    fixed_effects_result = fixed_effects.fit()

    # Fit the random effects model
    random_effects = RandomEffects.from_formula(formula, df)
    random_effects_result = random_effects.fit()

    # Perform the Hausman test
    comparison = compare({'Fixed Effects': fixed_effects_result, 'Random Effects': random_effects_result})

    # Save the results
    output_dir = f"./{output_dir}"
    os.makedirs(output_dir, exist_ok=True)
    summary_table = comparison.summary.as_html()
    results_df = pd.read_html(summary_table)[0]
    results_df.to_csv(f"{output_dir}/Hausman_Test_Results_{name}.csv", index=False)

    print(f"Hausman Test results for {name} saved in {output_dir}/")
    return comparison

if __name__ == "__main__":
    # Example Usage
    # Load datasets
    export_data = pd.read_parquet("Aggregated_Export.parquet")
    import_data = pd.read_parquet("Aggregated_Import.parquet")

    # Preprocess datasets
    export_data_preprocessed = preprocess_panel_data(export_data)
    import_data_preprocessed = preprocess_panel_data(import_data)

    # Independent variables for the analysis
    independent_vars = [
        "log_exchange", "log_exchange_official", "log_irgdp",
        "log_gdp_iran_lag1", "log_gdp_iran_lag2", "log_gdp_iran_lag3",
        "log_world_gdp", "log_world_gdp_lag1", "log_world_gdp_lag2",
        "log_world_gdp_lag3", "log_gdp_partner", "log_gdp_lag1",
        "log_gdp_lag2", "log_gdp_lag3", "log_cpi_ir", "log_cpi_us"
    ]

    # Perform Hausman tests for each dataset
    perform_hausman_test(export_data_preprocessed, independent_vars, "Export_Aggregated")
    perform_hausman_test(import_data_preprocessed, independent_vars, "Import_Aggregated")
