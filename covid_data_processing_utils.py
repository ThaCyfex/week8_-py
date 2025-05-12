# ==============================
# DATA UTILITIES (data_utils.py)
# ==============================
# Last Updated: 2023-11-15
# Compatible with:
# - analysis.ipynb
# - dashboard.py
# ==============================

# I am importing the necessary libraries for data processing and handling.
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import logging  # Added logging for better debugging
from typing import Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# I disabled chained assignment warnings to avoid unnecessary clutter in the output.
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)

# 1. PATH HANDLING ==================================
# This function determines the correct path to the data file.
def get_data_path() -> Path:
    try:
        # First, I check if the file exists relative to the script's location.
        path = Path(__file__).parent / "data" / "owid-covid-data.csv"
        if path.exists():
            return path
        
        # If not found, I check the current working directory.
        path = Path.cwd() / "data" / "owid-covid-data.csv"
        if path.exists():
            return path
        
        # If the file is still not found, I raise an error.
        raise FileNotFoundError(f"Data file not found in expected locations.")
    except Exception as e:
        logging.error(f"Error determining data path: {str(e)}")
        return Path("data") / "owid-covid-data.csv"  # Final fallback

# 2. DATA LOADING ===================================
# This function loads the raw data from the CSV file.
def load_raw_data() -> pd.DataFrame:
    path = get_data_path()
    
    try:
        # I specify the columns to load and parse the date column.
        df = pd.read_csv(
            path,
            usecols=[
                'iso_code', 'continent', 'location', 'date',
                'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
                'icu_patients', 'hosp_patients', 'weekly_icu_admissions',
                'population', 'people_vaccinated', 'people_fully_vaccinated'
            ],
            parse_dates=['date'],
            low_memory=False
        )
        
        # If the dataset is empty, I raise an error.
        if df.empty:
            raise ValueError("Loaded empty dataset")
            
        return df
    
    except Exception as e:
        # I provide a detailed error message if loading fails.
        logging.error(f"Error loading data from {path}: {str(e)}")
        raise

# 3. DATA CLEANING ==================================
# This function applies a standard cleaning pipeline to the data.
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # I remove rows where the 'continent' column is NaN (e.g., aggregates).
    df = df[df['continent'].notna()].copy()
    
    # I calculate additional metrics like death rate and vaccination percentages.
    df['death_rate'] = np.where(
        df['total_cases'] > 0,
        df['total_deaths'] / df['total_cases'],
        np.nan
    )
    df['pct_vaccinated'] = (df['people_vaccinated'] / df['population']) * 100
    df['pct_fully_vaccinated'] = (df['people_fully_vaccinated'] / df['population']) * 100
    
    # I fill missing values for ICU and hospital patients with 0.
    df[['hosp_patients', 'icu_patients']] = df[['hosp_patients', 'icu_patients']].fillna(0)
    
    return df

# 4. MAIN LOAD FUNCTION =============================
# This function loads and processes the data, returning both the full dataset and the latest records per country.
def load_processed_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = clean_data(load_raw_data())
    latest = df.groupby('location').last().sort_values('total_cases', ascending=False)
    return df, latest

# 5. CACHING DECORATORS =============================
# I added this decorator to cache the results of functions that return pandas DataFrames.
def cache_pandas_data(func):
    cache = {}
    
    def wrapper(*args, **kwargs):
        cache_key = (func.__name__, str(args), str(kwargs))
        
        if cache_key not in cache:
            cache[cache_key] = func(*args, **kwargs)
        
        return cache[cache_key].copy()  # I return a copy to prevent mutations.
    
    return wrapper

# ================== END OF FILE ====================