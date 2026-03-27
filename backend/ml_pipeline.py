import pandas as pd
import numpy as np
import joblib
import os

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.feature_selection import VarianceThreshold


# -----------------------------
# Paths
# -----------------------------

DATA_PATH = "data/cleaned_dataset.csv"
MODEL_DIR = "../models/"


print("Starting ML pipeline...")

# -----------------------------
# Load Dataset
# -----------------------------

print("Loading cleaned dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# -----------------------------
# Remove Low Variance Features
# -----------------------------

print("Removing low variance features...")

selector = VarianceThreshold(threshold=0.01)

X = selector.fit_transform(df)

print("Features after variance filter:", X.shape)


# -----------------------------
# Feature Scaling
# -----------------------------

print("Scaling features...")

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

joblib.dump(scaler, MODEL_DIR + "scaler.pkl")


# -----------------------------
# Train Isolation Forest
# -----------------------------

print("Training Isolation Forest...")

iso_model = IsolationForest(
    n_estimators=150,
    contamination=0.02,
    random_state=42,
    n_jobs=-1
)

iso_model.fit(X_scaled)

joblib.dump(iso_model, MODEL_DIR + "isolation_forest.pkl")


# -----------------------------
# Train Local Outlier Factor
# -----------------------------

print("Training Local Outlier Factor...")

lof_model = LocalOutlierFactor(
    n_neighbors=20,
    novelty=True
)

lof_model.fit(X_scaled)

joblib.dump(lof_model, MODEL_DIR + "lof_model.pkl")


# -----------------------------
# Train One-Class SVM
# -----------------------------

print("Training One-Class SVM...")

svm_model = OneClassSVM(
    kernel="rbf",
    gamma="auto",
    nu=0.02
)

svm_model.fit(X_scaled)

joblib.dump(svm_model, MODEL_DIR + "ocsvm_model.pkl")


print("ML Training Complete!")
