import pandas as pd
import numpy as np

np.random.seed(42)
n_rows = 30000

print("Generating realistic tiered student data...")

# Calculate exact row counts based on your percentages
n_topper = int(n_rows * 0.28)   # 8,400 students
n_avg = int(n_rows * 0.32)      # 9,600 students
n_below = int(n_rows * 0.18)    # 5,400 students
n_poor = int(n_rows * 0.22)     # 6,600 students

# Helper function to generate a specific group
def generate_group(n, study_mean, phone_mean, sleep_mean, att_mean, ai_mean):
    study = np.random.normal(study_mean, 1.0, n).clip(0, 10)
    phone = np.random.normal(phone_mean, 1.5, n).clip(0, 14)
    sleep = np.random.normal(sleep_mean, 1.0, n).clip(4, 10)
    ai = np.random.normal(ai_mean, 0.8, n).clip(0, 5)
    att = np.random.normal(att_mean, 8, n).clip(10, 100)
    
    # Calculate Scores mathematically based on their habits
    focus = 50 + (sleep * 4.5) - (phone * 2.5) + np.random.normal(0, 4, n)
    focus = focus.clip(10, 100)
    
    prod = 30 + (study * 4.0) + (focus * 0.3) + (ai * 2.5) + np.random.normal(0, 4, n)
    prod = prod.clip(10, 100)
    
    exam = 15 + (att * 0.35) + (study * 3.0) + (prod * 0.35) + np.random.normal(0, 3, n)
    exam = exam.clip(0, 100)
    
    return pd.DataFrame({
        'Study_Hours_Daily': np.round(study, 1),
        'Phone_Usage_Hours_Daily': np.round(phone, 1),
        'Sleep_Hours_Daily': np.round(sleep, 1),
        'AI_Tool_Usage_Hours_Daily': np.round(ai, 1),
        'Attendance_Pct': np.round(att, 1),
        'Focus_Score': np.round(focus, 1),
        'Productivity_Score': np.round(prod, 1),
        'Exam_Score': np.round(exam, 1)
    })

# 1. Generate the 4 distinct groups
toppers_df = generate_group(n_topper, study_mean=5.5, phone_mean=1.5, sleep_mean=8.0, att_mean=96, ai_mean=2.0)
average_df = generate_group(n_avg, study_mean=3.0, phone_mean=4.0, sleep_mean=7.0, att_mean=82, ai_mean=1.2)
below_df = generate_group(n_below, study_mean=1.5, phone_mean=6.5, sleep_mean=6.0, att_mean=68, ai_mean=0.8)
poor_df = generate_group(n_poor, study_mean=0.5, phone_mean=9.0, sleep_mean=5.5, att_mean=45, ai_mean=0.2)

# 2. Combine all groups into one dataset
df_combined = pd.concat([toppers_df, average_df, below_df, poor_df])

# 3. Shuffle the rows randomly so they aren't all clustered together
df_shuffled = df_combined.sample(frac=1, random_state=42).reset_index(drop=True)

# 4. Add Demographics and IDs *after* shuffling
df_shuffled.insert(0, 'Student_ID', [f"STU{str(i).zfill(5)}" for i in range(1, n_rows + 1)])
df_shuffled.insert(1, 'Gender', np.random.choice(['Male', 'Female', 'Other'], p=[0.48, 0.48, 0.04], size=n_rows))
df_shuffled.insert(2, 'Age', np.random.randint(18, 26, size=n_rows))

# 5. Export to CSV
output_filename = 'ultimate_student_metrics_30k.csv'
df_shuffled.to_csv(output_filename, index=False)

print(f"Success! Overwrote '{output_filename}'.")
print("New tiered preview:")
print(df_shuffled.head(10))
