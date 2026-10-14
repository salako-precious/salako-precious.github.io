from pathlib import Path

import numpy as np
import pandas as pd
import gradio as gr

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

DATA_PATH = Path(__file__).with_name("climate_regression_practice.csv")
RANDOM_STATE = 42
TARGET = "mean_temperature_c"

FEATURES = [
    "day_of_year",
    "relative_humidity_pct",
    "solar_radiation_w_m2",
    "wind_speed_kmh",
    "sea_level_pressure_hpa",
    "cloud_cover_pct",
    "rainfall_mm",
    "elevation_m",
    "urban_heat_index",
    "vegetation_index",
    "enso_index",
    "visibility_km",
]


def load_and_train():
    df = pd.read_csv(DATA_PATH)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE
    )

    # Linear Regression: use scaling, matching the learning workflow in the notebook.
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    linear = LinearRegression()
    linear.fit(X_train_scaled, y_train)

    # Tree models do not require feature scaling, so use the original feature values.
    tree = DecisionTreeRegressor(
        max_depth=4, min_samples_split=3, random_state=RANDOM_STATE
    )
    forest = RandomForestRegressor(
        n_estimators=100, max_depth=4, min_samples_split=3, random_state=RANDOM_STATE
    )
    boosting = GradientBoostingRegressor(
        n_estimators=100, max_depth=4, min_samples_split=3, random_state=RANDOM_STATE
    )

    for model in (tree, forest, boosting):
        model.fit(X_train, y_train)

    models = {
        "Linear Regression": linear,
        "Decision Tree": tree,
        "Random Forest": forest,
        "Gradient Boosting": boosting,
    }

    test_predictions = {
        "Linear Regression": linear.predict(X_test_scaled),
        "Decision Tree": tree.predict(X_test),
        "Random Forest": forest.predict(X_test),
        "Gradient Boosting": boosting.predict(X_test),
    }

    rows = []
    for name, preds in test_predictions.items():
        mse = mean_squared_error(y_test, preds)
        rows.append(
            {
                "Model": name,
                "R²": round(r2_score(y_test, preds), 4),
                "MAE": round(mean_absolute_error(y_test, preds), 4),
                "RMSE": round(np.sqrt(mse), 4),
            }
        )

    metrics_df = pd.DataFrame(rows).sort_values("RMSE").reset_index(drop=True)

    return df, scaler, models, metrics_df


DF, SCALER, MODELS, METRICS = load_and_train()


def predict_temperature(
    day_of_year,
    relative_humidity_pct,
    solar_radiation_w_m2,
    wind_speed_kmh,
    sea_level_pressure_hpa,
    cloud_cover_pct,
    rainfall_mm,
    elevation_m,
    urban_heat_index,
    vegetation_index,
    enso_index,
    visibility_km,
):
    values = [[
        day_of_year,
        relative_humidity_pct,
        solar_radiation_w_m2,
        wind_speed_kmh,
        sea_level_pressure_hpa,
        cloud_cover_pct,
        rainfall_mm,
        elevation_m,
        urban_heat_index,
        vegetation_index,
        enso_index,
        visibility_km,
    ]]

    X_new = pd.DataFrame(values, columns=FEATURES)

    linear_input = SCALER.transform(X_new)
    predictions = {
        "Linear Regression": MODELS["Linear Regression"].predict(linear_input)[0],
        "Decision Tree": MODELS["Decision Tree"].predict(X_new)[0],
        "Random Forest": MODELS["Random Forest"].predict(X_new)[0],
        "Gradient Boosting": MODELS["Gradient Boosting"].predict(X_new)[0],
    }

    result = pd.DataFrame(
        [
            {"Model": name, "Predicted Temperature (°C)": round(value, 2)}
            for name, value in predictions.items()
        ]
    )

    best_model = METRICS.iloc[0]["Model"]
    best_rmse = METRICS.iloc[0]["RMSE"]
    note = (
        f"Best model on the held-out test set: {best_model} "
        f"(RMSE = {best_rmse:.3f}°C)."
    )

    return result, note


with gr.Blocks(title="Climate Temperature Predictor") as demo:
    gr.Markdown(
        """
        # 🌦️ Climate Temperature Predictor
        Enter environmental measurements to compare predictions from four regression models.

        **Models:** Linear Regression, Decision Tree, Random Forest, Gradient Boosting.
        """
    )

    with gr.Row():
        with gr.Column():
            day_of_year = gr.Number(label="Day of year", value=180)
            relative_humidity_pct = gr.Number(label="Relative humidity (%)", value=68)
            solar_radiation_w_m2 = gr.Number(label="Solar radiation (W/m²)", value=520)
            wind_speed_kmh = gr.Number(label="Wind speed (km/h)", value=7)

        with gr.Column():
            sea_level_pressure_hpa = gr.Number(label="Sea-level pressure (hPa)", value=1012)
            cloud_cover_pct = gr.Number(label="Cloud cover (%)", value=48)
            rainfall_mm = gr.Number(label="Rainfall (mm)", value=5)
            elevation_m = gr.Number(label="Elevation (m)", value=25)

        with gr.Column():
            urban_heat_index = gr.Number(label="Urban heat index", value=1.6)
            vegetation_index = gr.Number(label="Vegetation index", value=0.55)
            enso_index = gr.Number(label="ENSO index", value=0)
            visibility_km = gr.Number(label="Visibility (km)", value=12)

    predict_button = gr.Button("Predict temperature")

    prediction_output = gr.Dataframe(
        headers=["Model", "Predicted Temperature (°C)"],
        label="Model predictions",
        interactive=False,
    )
    recommendation_output = gr.Markdown()

    gr.Markdown("## Test-set model comparison")
    gr.Dataframe(value=METRICS, interactive=False)

    predict_button.click(
        fn=predict_temperature,
        inputs=[
            day_of_year,
            relative_humidity_pct,
            solar_radiation_w_m2,
            wind_speed_kmh,
            sea_level_pressure_hpa,
            cloud_cover_pct,
            rainfall_mm,
            elevation_m,
            urban_heat_index,
            vegetation_index,
            enso_index,
            visibility_km,
        ],
        outputs=[prediction_output, recommendation_output],
    )


if __name__ == "__main__":
    demo.launch()
