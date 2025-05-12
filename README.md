# week8_-py

# COVID-19 Global Data Analysis & Reporting

This project provides an interactive data analysis and reporting notebook (and dashboard) that tracks global COVID-19 trends. It analyzes cases, deaths, recoveries, and vaccinations across countries and time, using real-world data. The project includes data cleaning, exploratory data analysis (EDA), insights generation, and visualizations.

## Objectives

- Import and clean global COVID-19 data
- Analyze time trends (cases, deaths, vaccinations)
- Compare metrics across countries/regions
- Visualize trends with charts and maps
- Communicate findings in a Jupyter Notebook report

## Tools & Libraries Used

- Python 3.x
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- ipywidgets
- streamlit

## How to Run / View the Project

### Jupyter Notebook

1. Open `covid_visualizations_and_insights.ipynb` or `covid_data_analysis_report.ipynb` in Jupyter Notebook or VS Code with the Jupyter extension.
2. Run the cells sequentially to load data, perform analysis, and view interactive visualizations.
3. **Tip:** If you encounter missing package errors, install them using `pip install <package-name>`.

### Streamlit Dashboard

1. Ensure all dependencies are installed (`pip install -r requirements.txt`).
2. Run the dashboard with:
   ```
   python covid_dashboard_app.py --dashboard
   ```
3. Follow the on-screen instructions to interact with the dashboard.
4. **Robust Feature:** The dashboard includes error handling for missing data files and invalid country input.

### Data

- Download the latest `owid-covid-data.csv` from [Our World in Data](https://github.com/owid/covid-19-data/tree/master/public/data) and place it in the `data/` directory.
- **Robust Feature:** The code checks for the presence of the data file and provides clear error messages if it is missing.

### Additional Robust Features

- **User Input Validation:** Interactive widgets in the notebooks validate country and date input, and display helpful messages if data is unavailable.
- **Error Handling:** All scripts and notebooks include error handling for missing files, invalid input, and data loading issues.
- **Caching:** Data loading utilities use caching to improve performance when re-running analyses.
- **Reproducibility:** All notebooks are designed to run from start to finish without manual intervention.

---

**Author:** Thembelani Bukali  
**Contact:** siphothagreat@gmail.com  
**Date:** 2025-05-05

