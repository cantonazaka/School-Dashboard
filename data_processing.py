import pandas as pd
import numpy as np

def read_data(filepath):
    df = pd.read_csv(filepath)
    return df

def get_numerical_data(df):
    numerical_columns_df = df.select_dtypes(exclude='object').drop('StudentID', axis=1)
    numerical_columns_filtered_df = numerical_columns_df.drop(['absences', 'FinalGrade' , 'age'], axis=1)
    other_numerical_columns_filtered_df = numerical_columns_df[['absences', 'FinalGrade' , 'age']]
    return numerical_columns_df , numerical_columns_filtered_df , other_numerical_columns_filtered_df

def get_categorical_data(df):
    object_columns_df = df.select_dtypes(include='object').drop(['FirstName', 'FamilyName'], axis=1)
    return object_columns_df
