import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")

print("Shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values per column:")
print(df.isnull().sum().sum())
salaries = df["MonthlyIncome"].to_numpy()

mean_salary = np.mean(salaries)
std_salary = np.std(salaries)
median_salary = np.median(salaries)

print(f"\nMean salary: {mean_salary:.2f}")
print(f"Median salary: {median_salary:.2f}")
print(f"Standard deviation: {std_salary:.2f}")

# Outlier detection: values beyond 2 standard deviations from the mean
outliers = salaries[(salaries > mean_salary + 2*std_salary) | (salaries < mean_salary - 2*std_salary)]
print(f"\nNumber of salary outliers (beyond 2 std dev): {len(outliers)}")
print("\n===== ATTRITION RATE BY DEPARTMENT =====")
dept_attrition = df.groupby("Department")["Attrition"].apply(
    lambda x: (x == "Yes").sum() / len(x) * 100  
).round(2).sort_values(ascending=False)
print(dept_attrition.sort_values(ascending=False))

print("\n===== AVERAGE INCOME BY JOB ROLE =====")
income_by_role = df.groupby("JobRole")["MonthlyIncome"].mean().round(2)
print(income_by_role.sort_values(ascending=False))

print("\n===== CORRELATION: SATISFACTION vs ATTRITION =====")
df["AttritionFlag"] = df["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)
correlation = df["JobSatisfaction"].corr(df["AttritionFlag"])
print(f"Correlation between Job Satisfaction and Attrition: {correlation:.3f}")
# Chart 1: Attrition rate by department
plt.figure(figsize=(8, 5))
dept_attrition.plot(kind="bar", color="steelblue")
plt.title("Attrition Rate by Department")
plt.xlabel("Department")
plt.ylabel("Attrition Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("attrition_by_department.png")
plt.show()

# Chart 2: Salary distribution histogram (shows the spread + outliers visually)
plt.figure(figsize=(8, 5))
plt.hist(salaries, bins=30, color="seagreen", edgecolor="black")
plt.title("Monthly Income Distribution")
plt.xlabel("Monthly Income")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig("salary_distribution.png")
plt.show()
print("\n" + "="*50)
print("KEY FINDINGS SUMMARY")
print("="*50)
print(f"""
1. Average monthly income across all employees: {mean_salary:.2f}
   (Median: {median_salary:.2f}, Std Dev: {std_salary:.2f})
   {len(outliers)} employees identified as salary outliers (2+ std dev from mean).

2. Highest attrition department: {dept_attrition.index[0]} at {dept_attrition.iloc[0]}%

3. Highest-paid job role on average: {income_by_role.index[0]} at {income_by_role.iloc[0]:.2f}

4. Correlation between job satisfaction and attrition: {correlation:.3f}
   {"This suggests lower satisfaction is linked to higher attrition." if correlation < 0 else "No strong negative relationship found."}
""")
