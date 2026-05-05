
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter

st.set_page_config(page_title="Oncology CDM Dashboard", layout="wide")

st.title("🧬 Oncology CDM Survival Dashboard")

# Load data
df = pd.read_csv("data/processed/final_cdm_dataset.csv")

st.subheader("Patient-Level CDM Data")
st.dataframe(df.head())

# -------------------------
# Risk Score
# -------------------------
biomarkers = [
    "FRACTION_GENOME_ALTERED",
    "TMB_NONSYNONYMOUS",
    "MSI_SCORE_MANTIS",
    "ANEUPLOIDY_SCORE"
]

for c in biomarkers:
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

df["RISK_SCORE"] = (
    df["FRACTION_GENOME_ALTERED"] * 0.3 +
    df["TMB_NONSYNONYMOUS"] * 0.3 +
    df["MSI_SCORE_MANTIS"] * 0.2 +
    df["ANEUPLOIDY_SCORE"] * 0.2
)

median = df["RISK_SCORE"].median()
df["RISK_GROUP"] = np.where(df["RISK_SCORE"] >= median, "High Risk", "Low Risk")

# -------------------------
# Kaplan–Meier Plot
# -------------------------
st.subheader("📉 Kaplan–Meier Survival Curve")

kmf = KaplanMeierFitter()
fig, ax = plt.subplots()

for g in df["RISK_GROUP"].unique():
    mask = df["RISK_GROUP"] == g
    kmf.fit(df[mask]["TIME"], df[mask]["EVENT"], label=g)
    kmf.plot(ax=ax)

st.pyplot(fig)

# -------------------------
# Cox Model
# -------------------------
st.subheader("⚖️ Cox Proportional Hazards Model")

cox_df = df[["TIME", "EVENT"] + biomarkers + ["RISK_SCORE"]].dropna()

cph = CoxPHFitter(penalizer=0.1)
cph.fit(cox_df, duration_col="TIME", event_col="EVENT")

st.dataframe(cph.summary)
