def validate_dataset(df):

    validation = {
        "remaining_nulls": int(df.isnull().sum().sum()),
        "remaining_duplicates": int(df.duplicated().sum()),
        "rows": len(df),
        "columns": len(df.columns)
    }

    validation["is_clean"] = (
        validation["remaining_nulls"] == 0
        and validation["remaining_duplicates"] == 0
    )

    return validation