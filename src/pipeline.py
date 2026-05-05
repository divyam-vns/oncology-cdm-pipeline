import pandas as pd
import numpy as np

def load_and_clean(df):
    df = df.copy()
    df.columns = df.columns.str.upper()
    return df

def compute_recist(tumor_df):
    def rule(x):
        change = ((x["CURRENT"] - x["BASELINE"]) / x["BASELINE"]) * 100
        if change <= -30:
            return "PR"
        elif change >= 20:
            return "PD"
        else:
            return "SD"
    tumor_df["RESPONSE"] = tumor_df.apply(rule, axis=1)
    return tumor_df
