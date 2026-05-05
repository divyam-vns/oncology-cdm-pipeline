
# 🧬 Oncology CDM Pipeline

End-to-end Clinical Data Management (CDM) and survival analysis pipeline using TCGA BRCA data from cBioPortal.

## Features
- CDM transformation (long → patient-level)
- AE coding (MedDRA-style simulation)
- RECIST tumor response modeling
- Kaplan–Meier survival analysis

## Structure
- notebooks/ → main analysis notebook
- data/ → raw + processed datasets
- outputs/ → plots and results
- src/ → reusable scripts

## Run
pip install -r requirements.txt
