
import pandas as pd
import numpy as np
import os

# -----------------------------
# File Paths
# -----------------------------

INPUT_FILE = "network_dataset.csv"
OUTPUT_FILE = "cleaned_dataset.csv"

print("Starting dataset cleaning...")

# -----------------------------
# Load Dataset
# -----------------------------

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE, low_memory=False)

print("Original Shape:", df.shape)

# -----------------------------
# Drop Non-Numeric Columns
# -----------------------------

print("Removing non-numeric columns...")

df = df.select_dtypes(include=[np.number])

print("After removing text columns:", df.shape)

# -----------------------------
# Replace Infinity Values
# -----------------------------

print("Replacing infinite values...")

df.replace([np.inf, -np.inf], np.nan, inplace=True)

# -----------------------------
# Drop NaN Rows
# -----------------------------

print("Dropping NaN rows...")

df.dropna(inplace=True)

print("After cleaning NaN:", df.shape)

# -----------------------------
# Dataset Sampling
# -----------------------------

sample_size = min(100000, len(df))

print(f"Sampling {sample_size} rows for training...")

df = df.sample(n=sample_size, random_state=42)

# -----------------------------
# Memory Optimization
# -----------------------------

print("Converting to float32 for memory efficiency...")

df = df.astype("float32")

# -----------------------------
# Save Cleaned Dataset
# -----------------------------

print("Saving cleaned dataset...")

df.to_csv(OUTPUT_FILE, index=False)

print("Cleaning Complete!")

print("Final Dataset Shape:", df.shape)
print("Saved as:", OUTPUT_FILE)