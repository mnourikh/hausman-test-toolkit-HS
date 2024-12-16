
# Hausman Test Toolkit

This toolkit provides methods for performing Hausman tests on panel data to compare fixed effects and random effects models.

## Features
1. **Data Preprocessing**: Formats and cleans panel data with multi-level indices.
2. **Hausman Test**: Compares fixed effects and random effects models.
3. **Result Export**: Saves test results to CSV files.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Prepare your panel data in Parquet format.
2. Update file paths and independent variables in `hausman_test_toolkit.py`.
3. Run the script:
   ```bash
   python hausman_test_toolkit.py
   ```

## Requirements
- Python 3.7 or later
- Libraries: pandas, numpy, linearmodels

## License
This project is licensed under the MIT License.
