# 1 Preliminary Data Exploration

import pandas as pd

# Load datasets
face_df = pd.read_csv('face_reports_sample.csv')
doc_df = pd.read_csv('doc_reports_sample.csv')

print(f"Face reports shape: {face_df.shape}")
print(f"Document reports shape: {doc_df.shape}")

# Check key columns
print("\nFace check columns:")
print(face_df.columns.tolist())

print("\nDocument check columns:")
print(doc_df.columns.tolist())