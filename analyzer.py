import pandas as pd


def analyze_dataset(df):
    report = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "columns": list(df.columns)
    }

    return report