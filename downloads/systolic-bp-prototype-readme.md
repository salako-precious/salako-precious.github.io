# Systolic BP Predictor

This is a small Streamlit app based on the regression project in `Health_data.ipynb`.

## What it does

- Uses the same general target: `systolic_bp`
- Uses the health predictors from the notebook
- Cleans the categorical and height/weight values
- Uses one-hot encoding for categorical variables
- Uses StandardScaler for numerical features
- Trains a Ridge regression model (`alpha=1.0`)
- Splits the data into training and testing sets
- Displays MAE, RMSE and R²
- Lets you enter a new person's information and estimate systolic BP

## Important improvement over the notebook

In the notebook, `StandardScaler` was fitted before `train_test_split`, which can cause data leakage.

This app puts preprocessing inside a scikit-learn Pipeline, so the scaler and imputers are fitted only on the training data.

## Run it

1. Install Python packages:

   `pip install -r requirements.txt`

2. Put `app.py` and `requirements.txt` in the same folder.

3. Run:

   `streamlit run app.py`

4. Upload your original `health_bp_dataset.csv`.

This is an educational/research prototype, not a medical diagnostic tool.
