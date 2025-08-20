import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import random
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score

# Path to your saved model (put your trained .pkl here)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "trained_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "diabetes.csv")


class DiabetesPredictor:
    def __init__(self):
        # Try to load existing model
        if os.path.exists(MODEL_PATH):
            # os.remove(MODEL_PATH)
            self.model = joblib.load(MODEL_PATH)
            print("✅ Loaded existing model!")
        else:
            print("⚠️ No saved model found, training a new one...")
            self.train_model()

    def train_model(self):
        df = pd.read_csv(DATA_PATH)

        # Train only on 6 features
        X = df[["Glucose", "BloodPressure", "BMI", "Age", "Pregnancies", "Insulin"]]
        y = df["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier()
        self.model.fit(X_train, y_train)

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"✅ Model trained. Accuracy: {acc:.2f}")

        # Save the trained model
        joblib.dump(self.model, MODEL_PATH)
        print(f"✅ Model saved at: {MODEL_PATH}")

    def predict(self, glucose, blood_pressure, bmi, age, pregnancies, insulin):
        features = np.array([[glucose, blood_pressure, bmi, age, pregnancies, insulin]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]

        confidence = max(probability) * 100

        if prediction == 1:
            if confidence > 70:
                risk_level = 'high'
            else:
                risk_level = 'medium'
        else:
            risk_level = 'low'

        return risk_level, confidence


class HeartDiseasePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        """Train the heart disease prediction model with real CSV"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "heart.csv")

        df = pd.read_csv(DATA_PATH)

        X = df[['age', 'sex', 'cp', 'trestbps', 'chol', 'thalach']]  # Only your 6
        y = df['target']


        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        # ✅ Optional: Save your model
        import joblib
        MODEL_PATH = os.path.join(BASE_DIR, "heart_model.pkl")
        joblib.dump(self.model, MODEL_PATH)
        print(f"✅ Model trained and saved: {MODEL_PATH}")

    def predict(self, age, sex, chest_pain, blood_pressure, cholesterol, max_heart_rate):
        """Make heart disease prediction"""
        features = np.array([[age, sex, chest_pain, blood_pressure, cholesterol, max_heart_rate]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]

        confidence = max(probability) * 100

        if prediction == 1:
            if confidence > 70:
                risk_level = 'high'
            else:
                risk_level = 'medium'
        else:
            risk_level = 'low'

        return risk_level, confidence


class HypertensionPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        """Train the hypertension prediction model with real CSV"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "hypertension.csv")

        df = pd.read_csv(DATA_PATH)

        X = df[['age', 'BMI', 'currentSmoker', 'sysBP', 'diaBP', 'heartRate']]
        y = df['Risk']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        # ✅ Optional: Save your model
        import joblib
        MODEL_PATH = os.path.join(BASE_DIR, "hypertension_model.pkl")
        joblib.dump(self.model, MODEL_PATH)
        print(f"✅ Hypertension model trained and saved: {MODEL_PATH}")

    def predict(self, age, bmi, current_smoker, sys_bp, dia_bp, heart_rate):
        """Make hypertension prediction"""
        features = np.array([[age, bmi, current_smoker, sys_bp, dia_bp, heart_rate]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]

        confidence = max(probability) * 100

        if prediction == 1:
            if confidence > 75:
                risk_level = 'high'
            else:
                risk_level = 'medium'
        else:
            risk_level = 'low'

        return risk_level, confidence

# import os
# import joblib
# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier

class AsthmaPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        """Train the asthma prediction model using CSV dataset"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "asthma.csv")

        df = pd.read_csv(DATA_PATH)

        # Make sure these columns match your form fields and dataset
        X = df[['Age', 'Gender', 'ShortnessOfBreath', 'Coughing', 'ChestTightness', 'Wheezing', 'FamilyHistoryAsthma']]
        y = df['Diagnosis']  # Target variable should be named 'Risk' (0 or 1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        # Save trained model
        MODEL_PATH = os.path.join(BASE_DIR, "asthma_model.pkl")
        joblib.dump(self.model, MODEL_PATH)
        print(f"✅ Asthma model trained and saved: {MODEL_PATH}")

    def predict(self, age, gender, shortness_of_breath, coughing, chest_tightness, wheezing, allergy_history):
        """Make asthma prediction from input"""
        features = np.array([[int(age), int(gender), int(shortness_of_breath), int(coughing),
                              int(chest_tightness), int(wheezing), int(allergy_history)]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        confidence = max(probability) * 100

        if prediction == 1:
            risk_level = 'high' if confidence > 70 else 'medium'
        else:
            risk_level = 'low'

        return risk_level, confidence

class StrokePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, 'data', 'stroke-data.csv')  # Make sure stroke.csv exists

        df = pd.read_csv(DATA_PATH)

        # Convert categorical columns if needed
        df.dropna(inplace=True)

        df['gender'] = df['gender'].map({'Female': 0, 'Male': 1, 'Other': 2})
        df['smoking_status'] = df['smoking_status'].map({
            'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3
        })

        X = df[['age', 'gender', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status']]
        y = df['stroke']  # Target column

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

        MODEL_PATH = os.path.join(BASE_DIR, 'stroke_model.pkl')
        joblib.dump(self.model, MODEL_PATH)
        print(f"✅ Stroke model trained and saved to: {MODEL_PATH}")

    def predict(self, age, gender, hypertension, heart_disease, avg_glucose_level, bmi, smoking_status):
        """Predict stroke and return risk level + confidence"""
        input_data = np.array([[
            int(age),
            int(gender),
            int(hypertension),
            int(heart_disease),
            float(avg_glucose_level),
            float(bmi),
            int(smoking_status)
        ]])

        prediction = self.model.predict(input_data)[0]
        proba = self.model.predict_proba(input_data)[0]
        confidence = max(proba) * 100

        if prediction == 1:
            risk_level = 'high' if confidence > 70 else 'medium'
        else:
            risk_level = 'low'

        return risk_level, confidence


# Initialize predictors
diabetes_predictor = DiabetesPredictor()
heart_disease_predictor = HeartDiseasePredictor()
hypertension_predictor = HypertensionPredictor()
asthma_predictor=AsthmaPredictor()
stroke_predictor=StrokePredictor()