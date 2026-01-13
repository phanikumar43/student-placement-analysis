# ==============================
# Student Performance & Placement Data Analysis
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

# ------------------------------
# 1. Load Dataset
# ------------------------------
DATA_PATH = "data/student_data.csv"
df = pd.read_csv(DATA_PATH)

print("First 5 rows of dataset:")
print(df.head())

# ------------------------------
# 2. Basic Data Understanding
# ------------------------------
print("\nDataset Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe(include="all"))

# ------------------------------
# 3. Data Cleaning
# ------------------------------

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Handle missing values
df["salary"] = df["salary"].fillna(0)

# Convert categorical placement column to numeric
df["placed"] = df["placed"].map({"Yes": 1, "No": 0})

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# ------------------------------
# 4. Feature Engineering
# ------------------------------

# Internship experience: Yes(1) / No(0)
df["internship_experience"] = df["internships"].apply(
    lambda x: 1 if x > 0 else 0
)

# CGPA categorization
df["cgpa_category"] = pd.cut(
    df["cgpa"],
    bins=[0, 6, 7.5, 10],
    labels=["Low", "Medium", "High"]
)

print("\nEngineered Columns Preview:")
print(df[["cgpa", "cgpa_category", "internship_experience"]].head())

# ------------------------------
# 5. Create Visuals Directory
# ------------------------------
VISUAL_PATH = "visuals"
os.makedirs(VISUAL_PATH, exist_ok=True)

# ------------------------------
# 6. Exploratory Data Analysis
# ------------------------------

# 6.1 Placement Count
df["placed"].value_counts().plot(kind="bar")
plt.title("Placement Count")
plt.xlabel("Placed (0 = No, 1 = Yes)")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(f"{VISUAL_PATH}/placement_count.png")
plt.show()

# 6.2 CGPA vs Placement Rate
df.groupby("cgpa_category")["placed"].mean().plot(kind="bar")
plt.title("Placement Rate by CGPA Category")
plt.xlabel("CGPA Category")
plt.ylabel("Placement Probability")
plt.tight_layout()
plt.savefig(f"{VISUAL_PATH}/cgpa_vs_placement.png")
plt.show()

# 6.3 Internship Experience vs Placement
df.groupby("internship_experience")["placed"].mean().plot(kind="bar")
plt.title("Internship Experience vs Placement")
plt.xlabel("Internship Experience (0 = No, 1 = Yes)")
plt.ylabel("Placement Probability")
plt.tight_layout()
plt.savefig(f"{VISUAL_PATH}/internship_vs_placement.png")
plt.show()

# 6.4 Salary Distribution (Placed Students Only)
df[df["salary"] > 0]["salary"].hist()
plt.title("Salary Distribution of Placed Students")
plt.xlabel("Salary")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(f"{VISUAL_PATH}/salary_distribution.png")
plt.show()

# ------------------------------
# 7. SQL Database Integration
# ------------------------------
DB_PATH = "data/student.db"
conn = sqlite3.connect(DB_PATH)

df.to_sql("students", conn, if_exists="replace", index=False)

print("\nData successfully stored in SQLite database.")

# ------------------------------
# 8. SQL Queries Execution
# ------------------------------

query_cgpa = """
SELECT cgpa_category, AVG(placed) AS placement_rate
FROM students
GROUP BY cgpa_category;
"""

query_internship = """
SELECT internship_experience, AVG(placed) AS placement_rate
FROM students
GROUP BY internship_experience;
"""

print("\nPlacement Rate by CGPA Category:")
print(pd.read_sql(query_cgpa, conn))

print("\nPlacement Rate by Internship Experience:")
print(pd.read_sql(query_internship, conn))

conn.close()

# ------------------------------
# 9. Final Insights (Console Output)
# ------------------------------
print("\nKey Insights:")
print("- Students with higher CGPA show better placement probability.")
print("- Internship experience positively impacts placement chances.")
print("- Placed students receive varied salary packages.")

print("\nProject execution completed successfully.")
