# Author: Mike Allen 25119947
import pandas as pd
import numpy as np

# Data pre-processing

def df_init():
    df = pd.read_excel('[5442] EcoMoveMobility.xlsx', sheet_name='Dataset', header=0, index_col=0)
    # Convert Excel serial date to datetime
    df['Date'] = pd.to_datetime(df['Date'], unit='D', origin='1899-12-30')
    
    #check for missing values in the entire DataFrame
    df.isnull().sum()

    #show all the categorical columns with missing values
    categorical_cols = df.select_dtypes(include=['object']).columns
    missing_values = df[categorical_cols].isnull().sum()
    if missing_values[missing_values > 0].empty:
        print("No categorical columns with missing values.")
    else:
        print("Categorical columns with missing values:")
        print(missing_values[missing_values > 0])

    #show all the numerical columns with missing values
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    missing_values = df[numerical_cols].isnull().sum()
    if missing_values[missing_values > 0].empty:
        print("No numerical columns with missing values.")
    else:
        print("Numerical columns with missing values:")
        print(missing_values[missing_values > 0])

    df.dtypes

    #Exporting the cleaned and prepared dataset for use in the interactive dashboard
    df.to_excel('cleaned_ds.xlsx')
    df_cleaned = pd.read_excel('cleaned_ds.xlsx')

df_init()