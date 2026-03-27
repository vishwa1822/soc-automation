import joblib
import numpy as np
import os


MODEL_PATH = "../models/"


class MLAnomalyEngine:

    def __init__(self):

        print("Loading ML models...")

        self.iso = joblib.load(os.path.join(MODEL_PATH, "isolation_forest.pkl"))
        self.lof = joblib.load(os.path.join(MODEL_PATH, "lof_model.pkl"))
        self.svm = joblib.load(os.path.join(MODEL_PATH, "ocsvm_model.pkl"))
        self.scaler = joblib.load(os.path.join(MODEL_PATH, "scaler.pkl"))


    def adjust_features(self, features):

        # get expected feature size from scaler
        expected_size = self.scaler.mean_.shape[0]

        current_size = len(features)

        if current_size < expected_size:

            # pad with zeros
            padding = [0] * (expected_size - current_size)
            features = features + padding

        elif current_size > expected_size:

            # trim extra values
            features = features[:expected_size]

        return features


    def predict(self, feature_vector):

        try:

            feature_vector = self.adjust_features(feature_vector)

            X = np.array(feature_vector).reshape(1, -1)

            X_scaled = self.scaler.transform(X)

            iso_pred = self.iso.predict(X_scaled)[0]
            lof_pred = self.lof.predict(X_scaled)[0]
            svm_pred = self.svm.predict(X_scaled)[0]

            iso_score = 1 if iso_pred == -1 else 0
            lof_score = 1 if lof_pred == -1 else 0
            svm_score = 1 if svm_pred == -1 else 0

            anomaly_score = (
                iso_score * 0.4 +
                lof_score * 0.3 +
                svm_score * 0.3
            )

            return {
                "is_anomaly": anomaly_score >= 0.7,
                "anomaly_score": anomaly_score
            }

        except Exception as e:

            return {
                "is_anomaly": False,
                "anomaly_score": 0,
                "error": str(e)
            }