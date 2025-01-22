import pandas as pd
import numpy as np

def clean_data(df):
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    return df

def transform_data(df):
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    return df

def load_data(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data loaded to {filename}")

if __name__ == "__main__":
    data = pd.read_csv('raw_data.csv')
    clean = clean_data(data)
    transformed = transform_data(clean)
    load_data(transformed, 'processed_data.csv')
