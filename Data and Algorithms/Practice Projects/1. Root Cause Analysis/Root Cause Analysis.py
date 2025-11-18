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

#2 Data Grain and Temporal Coverage

# Verify matching
print(f"Unique attempt_ids in face checks: {face_df['attempt_id'].nunique()}")
print(f"Unique attempt_ids in doc checks: {doc_df['attempt_id'].nunique()}")
print(f"Unique user_ids: {face_df['user_id'].nunique()}")

# Check temporal range
face_df['created_at'] = pd.to_datetime(face_df['created_at'])
doc_df['created_at'] = pd.to_datetime(doc_df['created_at'])

print(f"\nTemporal coverage:")
print(f"Start: {face_df['created_at'].min()}")
print(f"End: {face_df['created_at'].max()}")
print(f"Duration: {(face_df['created_at'].max() - face_df['created_at'].min()).days} days")

#3 Data Quality Assessment

# Missing values
print("Missing values in face checks:")
print(face_df.isnull().sum()[face_df.isnull().sum() > 0])

print("\nMissing values in document checks:")
print(doc_df.isnull().sum()[doc_df.isnull().sum() > 0])

#4 Merging the Dataset

# Merge on attempt_id to link face and document checks
merged_df = pd.merge(
    face_df,
    doc_df,
    on='attempt_id',
    suffixes=('_face', '_doc'),
    how='outer'
)

print(f"Merged dataset shape: {merged_df.shape}")
print(f"Rows with both checks: {(merged_df['result_face'].notna() & merged_df['result_doc'].notna()).sum()}")
print(f"Rows with only face check: {(merged_df['result_face'].notna() & merged_df['result_doc'].isna()).sum()}")
print(f"Rows with only doc check: {(merged_df['result_face'].isna() & merged_df['result_doc'].notna()).sum()}")

#5 Understanding Result Values
print("Face check results:")
print(face_df['result'].value_counts())

print("\nDocument check results:")
print(doc_df['result'].value_counts())

print("\nDocument sub_result breakdown:")
print(doc_df['sub_result'].value_counts())

#6 Defining Pass Logic
# Define pass/fail at attempt level
merged_df['attempt_passed'] = (
    (merged_df['result_face'] == 'clear') &
    (merged_df['result_doc'] == 'clear')
)

# Calculate attempt-level pass rate
attempt_pass_rate = merged_df['attempt_passed'].mean()
print(f"Attempt-level pass rate: {attempt_pass_rate:.2%}")
print(f"Total attempts: {len(merged_df)}")
print(f"Passed attempts: {merged_df['attempt_passed'].sum()}")
print(f"Failed attempts: {(~merged_df['attempt_passed']).sum()}")


