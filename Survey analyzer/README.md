# Survey Data Analyzer

## Overview
The **Survey Data Analyzer** is a Python application designed to import survey results, perform statistical analysis, generate visualizations, and export the analysis in JSON format. This tool provides insights into survey responses, helping users glean actionable information from their data.

## Features
- Import survey data from CSV files.
- Perform data analysis, including calculating response counts, unique responses, missing values, and basic statistics (mean, median, standard deviation) for numeric data.
- Generate visualizations of the data, including histograms for numeric data and bar charts for categorical data.
- Export analysis results to a JSON file.
- Display summary statistics of the survey data.

## How to Use

### 1. Import Survey Data
You can import data from a CSV file by entering the file name when prompted. The program will display the number of responses imported. The CSV file has to be in the same directory as the program.

### 2. Analyze Data
Once the data is imported, the program will analyze the survey results, generating basic statistics for each question in the survey.

### 3. Generate Visualizations
Visualizations are generated for each question and saved as PNG files in the specified folder. Numeric data will be visualized as histograms, and categorical data will be shown as bar charts.

### 4. Export Results
The analysis results can be exported to a JSON file, providing a structured output of the survey insights.

### 5. Show Summary Statistics
You can view a summary of the survey data, including the total number of responses, the number of questions, and the number of complete responses.

### 6. Exit Program
You can exit the program by selecting this option from the menu.

## Requirements
- Python 3.x
- Required libraries: `pandas`, `matplotlib`, `numpy`

Install the required libraries via pip:
```bash
pip install pandas matplotlib numpy
