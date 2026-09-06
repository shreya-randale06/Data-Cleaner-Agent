import pandas as pd
import numpy as np


class DataCleaner:

    def __init__(self, df):
        self.df = df.copy()
        self.removed_duplicates = 0
        self.missing_values_handled = 0

    def clean_column_names(self):
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    def remove_duplicates(self):
        before = len(self.df)

        self.df = self.df.drop_duplicates()

        after = len(self.df)

        self.removed_duplicates = before - after

    def handle_missing_values(self):

        before = int(self.df.isnull().sum().sum())

        numeric_columns = self.df.select_dtypes(
            include=np.number
        ).columns

        categorical_columns = self.df.select_dtypes(
            exclude=np.number
        ).columns

        for column in numeric_columns:
            self.df[column] = self.df[column].fillna(
                self.df[column].median()
            )

        for column in categorical_columns:
            mode = self.df[column].mode()

            if not mode.empty:
                self.df[column] = self.df[column].fillna(mode[0])
            else:
                self.df[column] = self.df[column].fillna("Unknown")

        after = int(self.df.isnull().sum().sum())

        self.missing_values_handled = before - after

    def clean_text(self):

        text_columns = self.df.select_dtypes(
            include=["object"]
        ).columns

        for column in text_columns:
            self.df[column] = (
                self.df[column]
                .astype(str)
                .str.strip()
            )

    def run(self):

        self.clean_column_names()
        self.remove_duplicates()
        self.handle_missing_values()
        self.clean_text()

        return self.df