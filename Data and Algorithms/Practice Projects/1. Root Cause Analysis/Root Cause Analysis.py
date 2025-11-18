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

#10 Categorising Failure Types

# Isolate failed attempts
failed_attempts = merged_df[~merged_df['attempt_passed']].copy()

print(f"Analysing {len(failed_attempts)} failed attempts...")


# Categorise failure types
def categorise_failure(row):
    """
    Categorise each failed attempt by which check(s) failed.

    Returns:
        - 'doc_only': Document check failed, face check passed
        - 'face_only': Face check failed, document check passed
        - 'both_failed': Both checks failed
        - 'missing_data': One or both checks missing (data quality issue)
    """
    face_failed = row['result_face'] != 'clear'
    doc_failed = row['result_doc'] != 'clear'

    if pd.isna(row['result_face']) or pd.isna(row['result_doc']):
        return 'missing_data'
    elif face_failed and doc_failed:
        return 'both_failed'
    elif face_failed:
        return 'face_only'
    elif doc_failed:
        return 'doc_only'
    else:
        return 'unknown'


failed_attempts['failure_type'] = failed_attempts.apply(categorise_failure, axis=1)

print("\nFailure type distribution:")
print(failed_attempts['failure_type'].value_counts())
print("\nAs percentages:")
print(failed_attempts['failure_type'].value_counts(normalize=True) * 100)

#11 Temporal Evolution of Failure Types

# Compare early period (June) vs late period (October)
early_date = pd.to_datetime('2017-06-30')
late_date = pd.to_datetime('2017-10-01')

early_failures = failed_attempts[pd.to_datetime(failed_attempts['created_at_face']) < early_date]
late_failures = failed_attempts[pd.to_datetime(failed_attempts['created_at_face']) >= late_date]

print("Early period (before June 30) failure breakdown:")
print(early_failures['failure_type'].value_counts())
print(f"\nTotal early failures: {len(early_failures)}")

print("\nLate period (October onwards) failure breakdown:")
print(late_failures['failure_type'].value_counts())
print(f"\nTotal late failures: {len(late_failures)}")

# Calculate percentage shift
early_pct = early_failures['failure_type'].value_counts(normalize=True) * 100
late_pct = late_failures['failure_type'].value_counts(normalize=True) * 100

print("\nPercentage comparison:")
comparison_df = pd.DataFrame({
    'Early': early_pct,
    'Late': late_pct,
    'Change': late_pct - early_pct
}).round(1)
print(comparison_df)

#12 Visualsing Failure Type Evolution

import numpy as np

fig, ax = plt.subplots(figsize=(10, 6))

failure_types = ['Document Only', 'Face Only', 'Both Failed']
early_values = [29.4, 67.6, 2.9]
late_values = [91.7, 2.3, 6.0]

x = np.arange(len(failure_types))
width = 0.35

bars1 = ax.bar(x - width / 2, early_values, width, label='June (Baseline)', color='#3498db')
bars2 = ax.bar(x + width / 2, late_values, width, label='October (Problem)', color='#e74c3c')

ax.set_title('Failure Type Distribution: June vs October', fontsize=16, fontweight='bold', pad=20)
ax.set_ylabel('Percentage of Failures (%)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(failure_types, fontsize=11)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 100)

# Add value labels
for i, (e, l) in enumerate(zip(early_values, late_values)):
    ax.text(i - width / 2, e + 2, f'{e:.1f}%', ha='center', fontsize=10, fontweight='bold')
    ax.text(i + width / 2, l + 2, f'{l:.1f}%', ha='center', fontsize=10, fontweight='bold')

    # Add change arrow and percentage
    change = l - e
    color = '#e74c3c' if change > 0 else '#2ecc71'
    y_pos = max(e, l) + 10
    ax.annotate(f'{change:+.1f}%',
                xy=(i, y_pos),
                ha='center',
                fontsize=11,
                fontweight='bold',
                color=color)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/failure_type_comparison.png', dpi=300, bbox_inches='tight')
print("Chart saved to /mnt/user-data/outputs/failure_type_comparison.png")

#13 Document Sub-Check Breakdown

# List all document sub-check columns
doc_subchecks = [
    'visual_authenticity_result_doc',
    'image_integrity_result',
    'face_detection_result',
    'image_quality_result',
    'supported_document_result',
    'conclusive_document_quality_result'
]

# Analyse failures for document-only failures
doc_only_failures = failed_attempts[failed_attempts['failure_type'] == 'doc_only']

print(f"Analysing {len(doc_only_failures)} document-only failures\n")

# Count non-clear results for each sub-check
for subcheck in doc_subchecks:
    if subcheck in doc_only_failures.columns:
        non_clear = doc_only_failures[doc_only_failures[subcheck] != 'clear']
        if len(non_clear) > 0:
            print(f"{subcheck}:")
            print(f"  Total non-clear: {len(non_clear)}")
            print(f"  Value distribution:")
            print(f"  {non_clear[subcheck].value_counts().to_dict()}")
            print()

#14 Monthly Sub-Check Degradation

# Calculate monthly clear rates for key sub-checks
months = ['2017-05', '2017-06', '2017-07', '2017-08', '2017-09', '2017-10']

results = []

for month in months:
    month_data = merged_df[merged_df['month'] == month]

    # image_integrity_result
    img_int_total = month_data['image_integrity_result'].notna().sum()
    img_int_clear = (month_data['image_integrity_result'] == 'clear').sum()
    img_int_rate = (img_int_clear / img_int_total) if img_int_total > 0 else 0

    # image_quality_result
    img_qual_total = month_data['image_quality_result'].notna().sum()
    img_qual_clear = (month_data['image_quality_result'] == 'clear').sum()
    img_qual_rate = (img_qual_clear / img_qual_total) if img_qual_total > 0 else 0

    # visual_authenticity_result
    vis_auth_total = month_data['visual_authenticity_result_doc'].notna().sum()
    vis_auth_clear = (month_data['visual_authenticity_result_doc'] == 'clear').sum()
    vis_auth_rate = (vis_auth_clear / vis_auth_total) if vis_auth_total > 0 else 0

    # face_detection_result
    face_det_total = month_data['face_detection_result'].notna().sum()
    face_det_clear = (month_data['face_detection_result'] == 'clear').sum()
    face_det_rate = (face_det_clear / face_det_total) if face_det_total > 0 else 0

    results.append({
        'month': month,
        'image_integrity': img_int_rate * 100,
        'image_quality': img_qual_rate * 100,
        'visual_authenticity': vis_auth_rate * 100,
        'face_detection': face_det_rate * 100
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

#15 Visualising Sub-Check Degradation

fig, ax = plt.subplots(figsize=(12, 7))

# Plot each sub-check
ax.plot(results_df['month'], results_df['image_integrity'],
        marker='o', linewidth=3, markersize=10, label='image_integrity', color='#e74c3c')
ax.plot(results_df['month'], results_df['image_quality'],
        marker='s', linewidth=3, markersize=10, label='image_quality', color='#f39c12')
ax.plot(results_df['month'], results_df['visual_authenticity'],
        marker='^', linewidth=2, markersize=8, label='visual_authenticity', color='#2ecc71')
ax.plot(results_df['month'], results_df['face_detection'],
        marker='d', linewidth=2, markersize=8, label='face_detection', color='#3498db')

ax.set_title('Document Sub-Check Clear Rates Over Time', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month (2017)', fontsize=12)
ax.set_ylabel('Clear Rate (%)', fontsize=12)
ax.legend(fontsize=11, loc='lower left')
ax.grid(True, alpha=0.3)
ax.set_ylim(55, 105)

# Rotate x labels
plt.xticks(rotation=45, ha='right')

# Annotate the catastrophic drop
ax.annotate('Catastrophic\nDegradation',
            xy=(5, 61.7),
            xytext=(4, 70),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11,
            fontweight='bold',
            color='red',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='red'))

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/subcheck_degradation.png', dpi=300, bbox_inches='tight')
print("Chart saved to /mnt/user-data/outputs/subcheck_degradation.png")

#16 Month-to-Month Decline Rates

changes = []

for i in range(1, len(results_df)):
    prev_month = results_df.iloc[i - 1]
    curr_month = results_df.iloc[i]

    changes.append({
        'period': f"{prev_month['month']} → {curr_month['month']}",
        'image_integrity_change': curr_month['image_integrity'] - prev_month['image_integrity'],
        'image_quality_change': curr_month['image_quality'] - prev_month['image_quality']
    })

changes_df = pd.DataFrame(changes)
print("\nMonth-to-month changes (percentage points):")
print(changes_df.to_string(index=False))

# Calculate average monthly decline
avg_decline_integrity = changes_df['image_integrity_change'].mean()
avg_decline_quality = changes_df['image_quality_change'].mean()

print(f"\nAverage monthly decline:")
print(f"  image_integrity: {avg_decline_integrity:.2f} percentage points")
print(f"  image_quality: {avg_decline_quality:.2f} percentage points")

#17 Control Group Analysis, Face Check Sub-Results Over Time

# Calculate monthly clear rates for face sub-checks
face_results = []

for month in months:
    month_data = merged_df[merged_df['month'] == month]

    # facial_image_integrity_result
    facial_int_total = month_data['facial_image_integrity_result'].notna().sum()
    facial_int_clear = (month_data['facial_image_integrity_result'] == 'clear').sum()
    facial_int_rate = (facial_int_clear / facial_int_total) if facial_int_total > 0 else 0

    # face_comparison_result
    face_comp_total = month_data['face_comparison_result'].notna().sum()
    face_comp_clear = (month_data['face_comparison_result'] == 'clear').sum()
    face_comp_rate = (face_comp_clear / face_comp_total) if face_comp_total > 0 else 0

    face_results.append({
        'month': month,
        'facial_image_integrity': facial_int_rate * 100,
        'face_comparison': face_comp_rate * 100
    })

face_results_df = pd.DataFrame(face_results)
print("Face check clear rates over time:")
print(face_results_df.to_string(index=False))

#18 Comparative Visualisation, Documents vs Face Checks

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Left plot: Document image_integrity (declining)
ax1.plot(results_df['month'], results_df['image_integrity'],
         marker='o', linewidth=3, markersize=10, color='#e74c3c')
ax1.set_title('Document image_integrity\n(DECLINING)',
              fontsize=14, fontweight='bold', color='#e74c3c')
ax1.set_xlabel('Month (2017)', fontsize=11)
ax1.set_ylabel('Clear Rate (%)', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(60, 100)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Annotate start and end
ax1.text(0, 99.64, '99.64%', fontsize=10, fontweight='bold', ha='right')
ax1.text(5, 61.70, '61.70%', fontsize=10, fontweight='bold', ha='left')

# Right plot: Face facial_image_integrity (improving)
ax2.plot(face_results_df['month'], face_results_df['facial_image_integrity'],
         marker='o', linewidth=3, markersize=10, color='#2ecc71')
ax2.set_title('Face facial_image_integrity\n(IMPROVING)',
              fontsize=14, fontweight='bold', color='#2ecc71')
ax2.set_xlabel('Month (2017)', fontsize=11)
ax2.set_ylabel('Clear Rate (%)', fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(60, 100)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Annotate start and end
ax2.text(0, 95.65, '95.65%', fontsize=10, fontweight='bold', ha='right')
ax2.text(5, 97.29, '97.29%', fontsize=10, fontweight='bold', ha='left')

fig.suptitle('Control Group Analysis: Document Checks Degraded, Face Checks Improved',
             fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/control_group_comparison.png', dpi=300, bbox_inches='tight')
print("Chart saved to /mnt/user-data/outputs/control_group_comparison.png")

#19 Solution, Real Time Monitoring, to be deployed as an hourly cron job

class KYCSubCheckMonitor:
    """
    Alert if any sub-check clear rate drops >10% from
    7-day rolling baseline.
    """

    def check_hourly(self):
        for subcheck in all_subchecks:
            current_rate = get_last_hour_clear_rate(subcheck)
            baseline = get_7day_baseline(subcheck)

            if current_rate < (baseline - 0.10):
                send_pagerduty_alert(
                    severity='HIGH',
                    subcheck=subcheck,
                    current=current_rate,
                    baseline=baseline
                )


