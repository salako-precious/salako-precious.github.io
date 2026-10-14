
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(page_title="Systolic BP Predictor", page_icon="🩺", layout="centered")

st.title("🩺 Systolic Blood Pressure Predictor")
st.write(
    "This app uses the health variables from your notebook to estimate "
    "systolic blood pressure (SBP) with Ridge regression."
)
st.info(
    "Educational/research prototype only. This is not a medical diagnostic "
    "or treatment tool."
)

uploaded = st.file_uploader(
    "Upload the original health_bp_dataset.csv",
    type=["csv"]
)

@st.cache_resource
def train_model(file_bytes):
    from io import BytesIO

    df = pd.read_csv(BytesIO(file_bytes)).copy()

    # Same target used in the notebook
    target = "systolic_bp"

    # Clean column names
    df.columns = df.columns.str.strip()

    # Basic cleaning following the notebook
    if "visit_date" in df.columns:
        df = df.drop(columns=["visit_date"])

    if "patient_id" in df.columns:
        df = df.drop(columns=["patient_id"])

    if "height_cm" in df.columns:
        df["height_cm"] = (
            df["height_cm"].astype(str).str.replace("cm", "", regex=False)
            .str.strip().replace({"nan": np.nan})
        )
        df["height_cm"] = pd.to_numeric(df["height_cm"], errors="coerce")

    if "weight_kg" in df.columns:
        df["weight_kg"] = (
            df["weight_kg"].astype(str).str.replace("kg", "", regex=False)
            .str.strip().replace({"nan": np.nan})
        )
        df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")

    # Standardize the categorical values more consistently than the notebook
    if "sex" in df.columns:
        df["sex"] = (
            df["sex"].astype(str).str.strip().str.lower()
            .replace({
                "f": "Female",
                "female": "Female",
                "m": "Male",
                "male": "Male",
            })
        )

    if "family_history_hypertension" in df.columns:
        df["family_history_hypertension"] = (
            df["family_history_hypertension"].astype(str).str.strip().str.lower()
            .replace({
                "n": "No",
                "no": "No",
                "y": "Yes",
                "yes": "Yes",
            })
        )

    if "smoking_status" in df.columns:
        df["smoking_status"] = (
            df["smoking_status"].astype(str).str.strip().str.lower()
            .replace({
                "never": "Never",
                "non_smoker": "Never",
                "non-smoker": "Never",
                "no": "Never",
                "current": "Current",
                "smoker": "Current",
                "former": "Former",
                "ex-smoker": "Former",
                "ex smoker": "Former",
                "quit": "Former",
            })
        )

    # Keep the same age filtering used in the notebook
    if "age" in df.columns:
        df = df[df["age"] <= 90]

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Drop rows where target is missing
    df = df.dropna(subset=[target])

    X = df.drop(columns=[target])
    y = df[target]

    categorical_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

    # IMPORTANT: preprocessing is fitted only on training data.
    # This avoids the data leakage present in the original notebook,
    # where StandardScaler was fitted before train_test_split.
    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", drop=None)),
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_pipe, numeric_cols),
        ("cat", categorical_pipe, categorical_cols),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("ridge", Ridge(alpha=1.0)),
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {
        "MAE": mean_absolute_error(y_test, predictions),
        "RMSE": np.sqrt(mean_squared_error(y_test, predictions)),
        "R2": r2_score(y_test, predictions),
        "n_train": len(X_train),
        "n_test": len(X_test),
    }

    return model, df, metrics, numeric_cols, categorical_cols


if uploaded is None:
    st.markdown("""
    ### How to use it

    1. Run the app.
    2. Upload the `health_bp_dataset.csv` file you used for your notebook.
    3. Enter a person's health information.
    4. Click **Predict systolic BP**.
    5. The app will display the model's estimated systolic blood pressure.

    The app also shows the model's test-set performance so you can see how
    well the model performed on data it did not train on.
    """)
    st.stop()

try:
    model, df, metrics, numeric_cols, categorical_cols = train_model(
        uploaded.getvalue()
    )
except Exception as e:
    st.error(f"Could not train the model: {e}")
    st.stop()

st.subheader("Model performance")

c1, c2, c3 = st.columns(3)
c1.metric("R²", f"{metrics['R2']:.3f}")
c2.metric("MAE", f"{metrics['MAE']:.2f} mmHg")
c3.metric("RMSE", f"{metrics['RMSE']:.2f} mmHg")

st.caption(
    f"Test set: {metrics['n_test']} observations. "
    "Performance is dataset-specific and should not be interpreted as clinical accuracy."
)

st.divider()
st.subheader("Enter patient information")

# Use dataset medians/modes as sensible starting values.
def median_value(col, default=0.0):
    values = pd.to_numeric(df[col], errors="coerce").dropna()
    return float(values.median()) if len(values) else default

age = st.number_input("Age (years)", min_value=1.0, max_value=120.0,
                      value=min(max(median_value("age", 40), 1), 120), step=1.0)
height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0,
                         value=min(max(median_value("height_cm", 170), 50), 250), step=0.5)
weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0,
                         value=min(max(median_value("weight_kg", 70), 20), 300), step=0.5)
bmi = st.number_input("BMI", min_value=10.0, max_value=80.0,
                      value=min(max(median_value("bmi", 25), 10), 80), step=0.1)
exercise = st.number_input("Exercise hours/week", min_value=0.0, max_value=40.0,
                           value=min(max(median_value("exercise_hours_per_week", 3), 0), 40), step=0.1)
sodium = st.number_input("Sodium intake (mg/day)", min_value=0.0, max_value=20000.0,
                         value=min(max(median_value("sodium_intake_mg", 3000), 0), 20000), step=50.0)
sleep = st.number_input("Sleep hours/night", min_value=0.0, max_value=24.0,
                        value=min(max(median_value("sleep_hours", 7), 0), 24), step=0.1)
alcohol = st.number_input("Alcohol units/week", min_value=0.0, max_value=100.0,
                          value=min(max(median_value("alcohol_units_per_week", 2), 0), 100), step=0.1)
stress = st.number_input("Stress level", min_value=0.0, max_value=10.0,
                         value=min(max(median_value("stress_level", 5), 0), 10), step=1.0)
heart_rate = st.number_input("Resting heart rate (bpm)", min_value=30.0, max_value=220.0,
                             value=min(max(median_value("resting_heart_rate", 70), 30), 220), step=1.0)

sex = st.selectbox("Sex", ["Female", "Male"])
smoking = st.selectbox("Smoking status", ["Never", "Current", "Former"])
family_history = st.selectbox("Family history of hypertension", ["No", "Yes"])

input_df = pd.DataFrame([{
    "age": age,
    "sex": sex,
    "height_cm": height,
    "weight_kg": weight,
    "bmi": bmi,
    "smoking_status": smoking,
    "family_history_hypertension": family_history,
    "exercise_hours_per_week": exercise,
    "sodium_intake_mg": sodium,
    "sleep_hours": sleep,
    "alcohol_units_per_week": alcohol,
    "stress_level": stress,
    "resting_heart_rate": heart_rate,
}])

if st.button("Predict systolic BP", type="primary"):
    prediction = float(model.predict(input_df)[0])

    st.success(f"Estimated systolic BP: **{prediction:.1f} mmHg**")

    if prediction < 120:
        st.write("The model's estimate is below 120 mmHg.")
    elif prediction < 130:
        st.write("The model's estimate is in the 120–129 mmHg range.")
    else:
        st.write("The model's estimate is 130 mmHg or higher.")

    st.caption(
        "These ranges are displayed only as a simple reference to the predicted "
        "number. They are not a diagnosis and should not be used to make "
        "medical decisions."
    )
