from pathlib import Path

import joblib
import inflection
import pandas as pd


class Fraud:

    def __init__(self):

        self.base_dir = Path(__file__).resolve().parent.parent

        self.model = joblib.load(
            self.base_dir / "artifacts" / "xgboost_fraud_detector.joblib"
        )

        print("Model loaded successfully")

    def data_cleaning(self, df):

        df = df.copy()

        df.columns = [
            inflection.underscore(col)
            for col in df.columns
        ]

        return df

    def feature_engineering(self, df):

        df["diff_new_old_balance"] = (
            df["newbalance_orig"]
            - df["oldbalance_org"]
        )

        df["diff_new_old_dest"] = (
            df["newbalance_dest"]
            - df["oldbalance_dest"]
        )

        return df

    def get_risk_level(self, probability):

        if probability < 0.30:
            return "Low"

        elif probability < 0.70:
            return "Medium"

        return "High"

    def predict(self, df):

        # Cleaning
        df1 = self.data_cleaning(df)

        # Feature Engineering
        df2 = self.feature_engineering(df1)

        # Pipeline handles preprocessing internally
        predictions = self.model.predict(df2)

        probabilities = self.model.predict_proba(df2)[:, 1]

        result = df.copy()

        result["prediction"] = predictions

        result["fraud_probability"] = probabilities

        result["risk_level"] = [
            self.get_risk_level(prob)
            for prob in probabilities
        ]

        return result