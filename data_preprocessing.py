import pandas as pd

# Step 1: Load dataset
df = pd.read_csv("Final_Marks_Data.csv")


# Step 2: Convert internals to 25

df["Internal1_25"] = (
    df["Internal Test 1 (out of 40)"] / 40
) * 25


df["Internal2_25"] = (
    df["Internal Test 2 (out of 40)"] / 40
) * 25


# Step 3: Convert assignment to 5

df["Assignment_5"] = (
    df["Assignment Score (out of 10)"] / 10
) * 5


# Step 4: Calculate Internal_Total

df["Internal_Total"] = (
    (df["Internal1_25"] + df["Internal2_25"]) / 2
) + df["Assignment_5"]


# Step 5: Create Risk column

def risk_label(row):

    if row["Attendance (%)"] < 75:
        return "High"

    elif row["Internal_Total"] < 16:
        return "High"

    elif row["Final Exam Marks (out of 100)"] >= 75:
        return "Low"

    elif row["Final Exam Marks (out of 100)"] >= 50:
        return "Medium"

    else:
        return "High"


df["Risk"] = df.apply(risk_label, axis=1)


# Step 6: Save processed dataset

df.to_csv("risk_dataset_final.csv", index=False)


print("Preprocessing Completed")
print(df.head())