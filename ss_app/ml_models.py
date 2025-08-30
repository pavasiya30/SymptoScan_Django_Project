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

        print(f"🔍 Diabetes Prediction Input: {features[0]}")
        print(f"🔍 Prediction: {prediction}, Probability: {probability}, Confidence: {confidence:.2f}%")

        # Use ML model prediction to determine risk level
        if prediction == 1:  # High risk prediction from model
            if confidence > 80:
                risk_level = 'high'
            elif confidence > 60:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        else:  # Low risk prediction from model
            if confidence > 90:
                risk_level = 'low'
            elif confidence > 70:
                risk_level = 'medium'
            else:
                risk_level = 'high'  # Low confidence in low risk = potential high risk

        print(f"🔍 Risk Level: {risk_level}")
        return risk_level, confidence


class HeartDiseasePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        """Train the heart disease prediction model with real CSV"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "heart.csv")
        MODEL_PATH = os.path.join(BASE_DIR, "heart_model.pkl")

        # Try to load existing model first (like other disease models)
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"✅ Loaded existing heart disease model: {MODEL_PATH}")
                return
            except Exception as e:
                print(f"⚠️ Error loading existing heart disease model: {str(e)}")
                # Continue to train new model

        # Train new model if no existing model found
        try:
            df = pd.read_csv(DATA_PATH)

            X = df[['age', 'sex', 'cp', 'trestbps', 'chol', 'thalach']]  # Only your 6
            y = df['target']

            # Print dataset info for debugging
            print(f"🔍 Heart Disease Dataset shape: {X.shape}")
            print(f"🔍 Heart Disease Target distribution: {y.value_counts()}")
            print(f"🔍 Heart Disease Features: {list(X.columns)}")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)

            # Test the model on training data
            train_pred = self.model.predict(X_train)
            train_acc = accuracy_score(y_train, train_pred)
            print(f"🔍 Heart Disease Training accuracy: {train_acc:.3f}")

            # Save trained model
            joblib.dump(self.model, MODEL_PATH)
            print(f"✅ Heart disease model trained and saved: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error training heart disease model: {str(e)}")
            # Create a dummy model for now
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def predict(self, age, sex, chest_pain, blood_pressure, cholesterol, max_heart_rate):
        """Make heart disease prediction"""
        features = np.array([[age, sex, chest_pain, blood_pressure, cholesterol, max_heart_rate]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]

        confidence = max(probability) * 100

        print(f"🔍 Heart Disease Prediction Input: {features[0]}")
        print(f"🔍 Prediction: {prediction}, Probability: {probability}, Confidence: {confidence:.2f}%")

        # Use ML model prediction to determine risk level
        if prediction == 1:  # High risk prediction from model
            if confidence > 80:
                risk_level = 'high'
            elif confidence > 60:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        else:  # Low risk prediction from model
            if confidence > 90:
                risk_level = 'low'
            elif confidence > 70:
                risk_level = 'medium'
            else:
                risk_level = 'high'  # Low confidence in low risk = potential high risk

        print(f"🔍 Risk Level: {risk_level}")
        return risk_level, confidence


class HypertensionPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        """Train the hypertension prediction model with real CSV"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "hypertension.csv")
        MODEL_PATH = os.path.join(BASE_DIR, "hypertension_model.pkl")

        # Try to load existing model first (like other disease models)
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"✅ Loaded existing hypertension model: {MODEL_PATH}")
                return
            except Exception as e:
                print(f"⚠️ Error loading existing hypertension model: {str(e)}")
                # Continue to train new model

        # Train new model if no existing model found
        try:
            df = pd.read_csv(DATA_PATH)

            X = df[['age', 'BMI', 'currentSmoker', 'sysBP', 'diaBP', 'heartRate']]
            y = df['Risk']

            # Print dataset info for debugging
            print(f"🔍 Hypertension Dataset shape: {X.shape}")
            print(f"🔍 Hypertension Target distribution: {y.value_counts()}")
            print(f"🔍 Hypertension Features: {list(X.columns)}")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)

            # Test the model on training data
            train_pred = self.model.predict(X_train)
            train_acc = accuracy_score(y_train, train_pred)
            print(f"🔍 Hypertension Training accuracy: {train_acc:.3f}")

            # Save trained model
            joblib.dump(self.model, MODEL_PATH)
            print(f"✅ Hypertension model trained and saved: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error training hypertension model: {str(e)}")
            # Create a dummy model for now
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def predict(self, age, bmi, current_smoker, sys_bp, dia_bp, heart_rate):
        """Make hypertension prediction"""
        features = np.array([[age, bmi, current_smoker, sys_bp, dia_bp, heart_rate]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]

        confidence = max(probability) * 100

        print(f"🔍 Hypertension Prediction Input: {features[0]}")
        print(f"🔍 Prediction: {prediction}, Probability: {probability}, Confidence: {confidence:.2f}%")

        # Use ML model prediction to determine risk level
        if prediction == 1:  # High risk prediction from model
            if confidence > 80:
                risk_level = 'high'
            elif confidence > 60:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        else:  # Low risk prediction from model
            if confidence > 90:
                risk_level = 'low'
            elif confidence > 70:
                risk_level = 'medium'
            else:
                risk_level = 'high'  # Low confidence in low risk = potential high risk

        print(f"🔍 Risk Level: {risk_level}")
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
        MODEL_PATH = os.path.join(BASE_DIR, "asthma_model.pkl")

        # Try to load existing model first (like other disease models)
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"✅ Loaded existing asthma model: {MODEL_PATH}")
                return
            except Exception as e:
                print(f"⚠️ Error loading existing asthma model: {str(e)}")
                # Continue to train new model

        # Train new model if no existing model found
        try:
            df = pd.read_csv(DATA_PATH)

            # Make sure these columns match your form fields and dataset
            X = df[['Age', 'Gender', 'ShortnessOfBreath', 'Coughing', 'ChestTightness', 'Wheezing', 'FamilyHistoryAsthma']]
            y = df['Diagnosis']  # Target variable should be named 'Risk' (0 or 1)

            # Print dataset info for debugging
            print(f"🔍 Asthma Dataset shape: {X.shape}")
            print(f"🔍 Asthma Target distribution: {y.value_counts()}")
            print(f"🔍 Asthma Features: {list(X.columns)}")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)

            # Test the model on training data
            train_pred = self.model.predict(X_train)
            train_acc = accuracy_score(y_train, train_pred)
            print(f"🔍 Asthma Training accuracy: {train_acc:.3f}")

            # Save trained model
            joblib.dump(self.model, MODEL_PATH)
            print(f"✅ Asthma model trained and saved: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error training asthma model: {str(e)}")
            # Create a dummy model for now
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def predict(self, age, gender, shortness_of_breath, coughing, chest_tightness, wheezing, allergy_history):
        """Make asthma prediction from input"""
        features = np.array([[int(age), int(gender), int(shortness_of_breath), int(coughing),
                              int(chest_tightness), int(wheezing), int(allergy_history)]])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        confidence = max(probability) * 100

        print(f"🔍 Asthma Prediction Input: {features[0]}")
        print(f"🔍 Prediction: {prediction}, Probability: {probability}, Confidence: {confidence:.2f}%")

        # Use ML model prediction to determine risk level
        if prediction == 1:  # High risk prediction from model
            if confidence > 80:
                risk_level = 'high'
            elif confidence > 60:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        else:  # Low risk prediction from model
            if confidence > 90:
                risk_level = 'low'
            elif confidence > 70:
                risk_level = 'medium'
            else:
                risk_level = 'high'  # Low confidence in low risk = potential high risk

        print(f"🔍 Risk Level: {risk_level}")
        return risk_level, confidence

class StrokePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, 'data', 'stroke-data.csv')  # Make sure stroke.csv exists
        MODEL_PATH = os.path.join(BASE_DIR, 'stroke_model.pkl')

        # Try to load existing model first (like other disease models)
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"✅ Loaded existing stroke model: {MODEL_PATH}")
                return
            except Exception as e:
                print(f"⚠️ Error loading existing stroke model: {str(e)}")
                # Continue to train new model

        # Train new model if no existing model found
        try:
            df = pd.read_csv(DATA_PATH)

            # Convert categorical columns if needed
            df.dropna(inplace=True)

            df['gender'] = df['gender'].map({'Female': 0, 'Male': 1, 'Other': 2})
            df['smoking_status'] = df['smoking_status'].map({
                'never smoked': 0, 'formerly smoked': 1, 'smokes': 2, 'Unknown': 3
            })

            X = df[['age', 'gender', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status']]
            y = df['stroke']  # Target column

            # Print dataset info for debugging
            print(f"🔍 Stroke Dataset shape: {X.shape}")
            print(f"🔍 Stroke Target distribution: {y.value_counts()}")
            print(f"🔍 Stroke Features: {list(X.columns)}")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)

            # Test the model on training data
            train_pred = self.model.predict(X_train)
            train_acc = accuracy_score(y_train, train_pred)
            print(f"🔍 Stroke Training accuracy: {train_acc:.3f}")

            joblib.dump(self.model, MODEL_PATH)
            print(f"✅ Stroke model trained and saved to: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error training stroke model: {str(e)}")
            # Create a dummy model for now
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

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

        print(f"🔍 Stroke Prediction Input: {input_data[0]}")
        print(f"🔍 Prediction: {prediction}, Probability: {proba}, Confidence: {confidence:.2f}%")

        # Use ML model prediction to determine risk level
        if prediction == 1:  # High risk prediction from model
            if confidence > 80:
                risk_level = 'high'
            elif confidence > 60:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        else:  # Low risk prediction from model
            if confidence > 90:
                risk_level = 'low'
            elif confidence > 70:
                risk_level = 'medium'
            else:
                risk_level = 'high'  # Low confidence in low risk = potential high risk

        print(f"🔍 Risk Level: {risk_level}")
        return risk_level, confidence


class KidneyDiseasePredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_model()

    def _train_model(self):
        """Train the kidney disease prediction model using CSV dataset"""
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_PATH = os.path.join(BASE_DIR, "data", "kidney_disease_dataset.csv")
        MODEL_PATH = os.path.join(BASE_DIR, "kidney_disease_model.pkl")

        # Try to load existing model first (like other disease models)
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                print(f"✅ Loaded existing kidney disease model: {MODEL_PATH}")
                return
            except Exception as e:
                print(f"⚠️ Error loading existing model: {str(e)}")
                # Continue to train new model

        # Train new model if no existing model found
        try:
            df = pd.read_csv(DATA_PATH)
            
            # Clean the data - remove rows with missing values
            df.dropna(inplace=True)
            
            # Convert categorical columns to numeric
            df['Hypertension (yes/no)'] = df['Hypertension (yes/no)'].map({'yes': 1, 'no': 0})
            df['Diabetes mellitus (yes/no)'] = df['Diabetes mellitus (yes/no)'].map({'yes': 1, 'no': 0})
            
            # Select the 7 features we want to use - using exact column names from CSV
            X = df[['Age of the patient', 'Blood pressure (mm/Hg)', 'Serum creatinine (mg/dl)', 'Blood urea (mg/dl)', 'Hemoglobin level (gms)', 'Hypertension (yes/no)', 'Diabetes mellitus (yes/no)']]
            y = df['Target']  # Target column

            # Print dataset info for debugging
            print(f"🔍 Dataset shape: {X.shape}")
            print(f"🔍 Target distribution: {y.value_counts()}")
            print(f"🔍 Features: {list(X.columns)}")

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)

            # Test the model on training data
            train_pred = self.model.predict(X_train)
            train_acc = accuracy_score(y_train, train_pred)
            print(f"🔍 Training accuracy: {train_acc:.3f}")

            # Save trained model
            joblib.dump(self.model, MODEL_PATH)
            print(f"✅ Kidney disease model trained and saved: {MODEL_PATH}")
        except Exception as e:
            print(f"❌ Error training kidney disease model: {str(e)}")
            # Create a dummy model for now
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def predict(self, age, blood_pressure, serum_creatinine, blood_urea, hemoglobin, hypertension, diabetes):
        """Make kidney disease prediction from input"""
        features = np.array([[
            int(age),
            float(blood_pressure),
            float(serum_creatinine),
            float(blood_urea),
            float(hemoglobin),
            int(hypertension),
            int(diabetes)
        ]])
        
        print(f"🔍 Kidney Disease Prediction Input: {features[0]}")
        
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0]
        confidence = max(probability) * 100

        print(f"🔍 Prediction: {prediction}, Probability: {probability}, Confidence: {confidence:.2f}%")

        # Use ML model prediction to determine risk level
        if prediction == 1:  # High risk prediction from model
            if confidence > 80:
                risk_level = 'high'
            elif confidence > 60:
                risk_level = 'medium'
            else:
                risk_level = 'low'
        else:  # Low risk prediction from model
            if confidence > 90:
                risk_level = 'low'
            elif confidence > 70:
                risk_level = 'medium'
            else:
                risk_level = 'high'  # Low confidence in low risk = potential high risk

        print(f"🔍 Risk Level: {risk_level}")
        return risk_level, confidence

# Initialize predictors
diabetes_predictor = DiabetesPredictor()
heart_disease_predictor = HeartDiseasePredictor()
hypertension_predictor = HypertensionPredictor()
asthma_predictor=AsthmaPredictor()
stroke_predictor=StrokePredictor()
kidney_disease_predictor = KidneyDiseasePredictor()