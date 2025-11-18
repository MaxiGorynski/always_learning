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

#7 User-Level Pass Rate
# Use whichever user_id is not null
merged_df['user_id'] = merged_df['user_id_face'].fillna(merged_df['user_id_doc'])

# Group by user
user_attempts = merged_df.groupby('user_id').agg({
    'attempt_id': 'count',
    'attempt_passed': 'any'  # User passes if ANY attempt passes
}).rename(columns={'attempt_id': 'num_attempts', 'attempt_passed': 'user_passed'})

print(f"Total unique users: {len(user_attempts)}")
print(f"Users who passed: {user_attempts['user_passed'].sum()}")
print(f"User-level pass rate: {user_attempts['user_passed'].mean():.2%}")

print("\nAttempts per user:")
print(user_attempts['num_attempts'].value_counts().sort_index())

#8 Monthly Pass Rate Trends
# Extract month for grouping
merged_df['date'] = pd.to_datetime(merged_df['created_at_face']).dt.date
merged_df['month'] = pd.to_datetime(merged_df['date']).dt.to_period('M')

# Calculate monthly statistics
monthly_stats = merged_df.groupby('month').agg({
    'attempt_id': 'count',
    'attempt_passed': ['sum', 'mean']
}).round(4)
monthly_stats.columns = ['total_attempts', 'passed_attempts', 'pass_rate']

print(monthly_stats)

#9 Visualising the Decline
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

months = [str(m) for m in monthly_stats.index]
pass_rates = monthly_stats['pass_rate'].values * 100

ax.plot(months, pass_rates, marker='o', linewidth=3, markersize=10, color='#e74c3c')
ax.axhline(y=85, color='green', linestyle='--', label='Target (85%)', alpha=0.7, linewidth=2)

ax.set_title('Monthly KYC Pass Rate Decline', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month (2017)', fontsize=12)
ax.set_ylabel('Pass Rate (%)', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_ylim(50, 100)

# Annotate values
for i, rate in enumerate(pass_rates):
    ax.annotate(f'{rate:.1f}%',
                xy=(i, rate),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold')

plt.tight_layout()
plt.savefig('monthly_pass_rate_decline.png', dpi=300, bbox_inches='tight')
