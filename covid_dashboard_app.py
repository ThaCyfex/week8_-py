# COVID-19 ANALYSIS (ALL-IN-ONE)
# Combines: Data download, cleaning, analysis & dashboard
# Usage: python covid_analysis.py [--download] [--dashboard] [--display <country_name>]

# Dataset Sources:
# - Our World in Data (GitHub): https://github.com/owid/covid-19-data/tree/master/public/data
# - Kaggle COVID-19 Dataset: https://www.kaggle.com/datasets

# Feedback:
# - Submit an Issue on GitHub: https://github.com/your-repo/issues
# - Fill Out Our Feedback Form: https://forms.gle/example
# - Email: your-email@example.com

# I am importing the necessary libraries for data processing, visualization, and building the Streamlit dashboard.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path
import argparse
import sys
import urllib.request
import logging  # Added logging for better debugging
from covid_data_processing_utils import load_processed_data, get_data_path

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure the data directory and file exist
data_dir = Path("data")
data_file = data_dir / "owid-covid-data.csv"

if not data_file.exists():
    logging.error(f"Data file not found at {data_file}. Please ensure the file exists.")
    sys.exit(1)

# ======================
# 1. DATA DOWNLOADER
# ======================
def download_data(force=False):
    """Download the data file from GitHub if it doesn't exist or if forced."""
    data_dir.mkdir(exist_ok=True)
    data_path = data_dir / "owid-covid-data.csv"
    
    if not data_path.exists() or force:
        url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
        try:
            logging.info("Downloading data...")
            urllib.request.urlretrieve(url, data_path)
            logging.info(f"Data saved to {data_path}")
        except Exception as e:
            logging.error(f"Download failed: {str(e)}")
            sys.exit(1)
    else:
        logging.info("Data file already exists. Use --download to force re-download.")
    return data_path

# ======================
# 2. ANALYSIS FUNCTIONS
# ======================
def plot_global_trends(df):
    """Generate a global trends plot for cases and deaths."""
    global_df = df.groupby('date').sum(numeric_only=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(global_df['total_cases'], label='Cases', color='blue')
    ax.plot(global_df['total_deaths'], label='Deaths', color='red')
    ax.set_title("Global COVID-19 Trends")
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.legend()
    return fig

# ======================
# 3. STREAMLIT DASHBOARD
# ======================
def run_dashboard(df):
    """Launch the Streamlit dashboard."""
    try:
        st.set_page_config(layout="wide")
        st.title("COVID-19 Dashboard")
        
        country = st.selectbox("Country", df['location'].unique())
        country_data = df[df['location'] == country].set_index('date')
        
        st.line_chart(country_data[['total_cases', 'total_deaths']])
        st.metric("Max Vaccination %", f"{country_data['pct_fully_vaccinated'].max():.1f}%")
        st.subheader("ICU and Vaccination Trends")
        st.line_chart(country_data[['icu_patients', 'pct_fully_vaccinated']])
    except Exception as e:
        logging.error(f"Error running Streamlit dashboard: {str(e)}")
        st.error("An error occurred while running the dashboard. Please check the logs.")

# ======================
# 4. MAIN EXECUTION
# ======================
def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="Force data download")
    parser.add_argument("--dashboard", action="store_true", help="Launch Streamlit dashboard")
    parser.add_argument("--display", type=str, help="Display data for a specific country")
    args = parser.parse_args()
    
    if args.download:
        download_data(force=True)
    
    try:
        df, latest = load_processed_data()
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        sys.exit(1)
    
    if args.dashboard:
        try:
            import streamlit.cli as stcli
            stcli.main(["streamlit", "run", __file__])
        except Exception as e:
            logging.error(f"Error launching Streamlit: {str(e)}")
            sys.exit(1)
    elif args.display:
        country = args.display
        country_data = df[df['location'] == country]
        if country_data.empty:
            logging.warning(f"No data found for country: {country}")
        else:
            print(country_data)
    else:
        fig = plot_global_trends(df)
        plt.show()
        logging.info("Data loaded successfully. Use --dashboard for interactive mode.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Execution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
