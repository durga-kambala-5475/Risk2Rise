# ===============================
# Risk2Rise - Model Training Code
# ===============================

# Step 1: Import libraries

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, classification_report

import joblib


# Step 2: Load preprocessed dataset

df = pd.read_csv("risk_dataset_final.csv")


# Step 3: Select input features (FINAL BEST FEATURES)

X = df[[
    "Attendance (%)",
    "Internal1_25",
    "Internal2_25",
    "Assignment_5",
    "Internal_Total",
    "Daily Study Hours"
]]


# Step 4: Select target label

y = df["Risk"]


# Step 5: Split dataset into training and testing

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,
    test_size=0.2,
    random_state=42
)


# Step 6: Create Random Forest model with tuning and balancing

model = RandomForestClassifier(

    n_estimators=400,       # number of trees

    max_depth=12,           # depth of trees

    min_samples_split=5,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=42
)


# Step 7: Train the model

model.fit(X_train, y_train)


# Step 8: Predict using test data

y_pred = model.predict(X_test)


# Step 9: Evaluate performance

print("\nFinal Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))


# Step 10: Save trained model

joblib.dump(model, "risk_model.pkl")


print("\n✅ Final Model saved as risk_model.pkl")