# 🌤️ Climate Temperature Prediction with Machine Learning

> **From weather measurements to machine learning predictions — and a comparison of four major regression algorithms.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Scikit--learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?logo=scikitlearn)
![Status](https://img.shields.io/badge/Project-Completed-success)

## 🚀 Project Overview

How accurately can we predict **mean daily temperature** from environmental measurements?

This project explores that question using a clean climate dataset and four regression approaches:

- 📈 Linear Regression
- 🌳 Decision Tree Regressor
- 🌲 Random Forest Regressor
- ⚡ Gradient Boosting Regressor

I also experimented with a **Stacking Regressor** to see whether combining different models could outperform the individual models.

The main goal was not simply to build a model, but to understand **why the models behave differently**, how feature relationships affect prediction, and how to identify the strongest model using unseen data.

---

## 🎯 Business / Real-World Problem

Imagine a weather and climate monitoring team that wants to estimate daily temperature from environmental measurements.

Instead of asking only:

> "Can I predict temperature?"

this project asks:

> **Which machine learning approach can capture the relationships between climate variables and temperature most effectively?**

### Target variable

`mean_temperature_c`

### Input features

| Feature | Description |
|---|---|
| `day_of_year` | Position within the year |
| `relative_humidity_pct` | Relative humidity (%) |
| `solar_radiation_w_m2` | Solar radiation (W/m²) |
| `wind_speed_kmh` | Wind speed (km/h) |
| `sea_level_pressure_hpa` | Sea-level atmospheric pressure (hPa) |
| `cloud_cover_pct` | Cloud cover (%) |
| `rainfall_mm` | Rainfall (mm) |
| `elevation_m` | Elevation (m) |
| `urban_heat_index` | Urban heat contribution |
| `vegetation_index` | Vegetation index |
| `enso_index` | ENSO-related climate indicator |
| `visibility_km` | Visibility (km) |

---

## 🧹 Data Cleaning & Validation

The dataset used in this project contains **1,200 observations and 13 columns**. During preprocessing, I inspected the dataset structure, data types, descriptive statistics, distributions, feature relationships, and correlation matrix before modelling.

The dataset was already clean: all 13 columns contained **1,200 non-null observations**, so no missing-value imputation was required.

I also separated the target variable from the predictors and created an **80/20 train-test split** with `random_state=42` to keep the experiment reproducible.

> **Why does this matter?**
>
> A model is only as trustworthy as the data preparation behind it. Before training a model, I first checked what the dataset contains, whether the variables are usable, and how the features relate to the target.

---

## 🔎 Exploratory Data Analysis

The exploratory analysis included:

- Dataset inspection with `info()` and `describe()`
- Distribution plots
- Pairwise relationships using a pair plot
- Correlation analysis
- Correlation heatmap
- Multicollinearity inspection

### 🔥 Important correlation findings

The strongest linear relationships with the target were:

| Feature | Correlation with mean temperature |
|---|---:|
| ☀️ `solar_radiation_w_m2` | **0.7091** |
| 📅 `day_of_year` | **0.4010** |
| 🏙️ `urban_heat_index` | 0.0969 |
| 🌎 `enso_index` | 0.0753 |
| 💧 `relative_humidity_pct` | -0.1093 |

An important lesson from the analysis was that **correlation alone does not tell the whole modelling story**. A feature can have a weak linear correlation and still contain useful nonlinear information.

---

## 🧠 Modelling Strategy

The modelling workflow was:

```text
Raw climate data
       ↓
Data inspection & validation
       ↓
Exploratory data analysis
       ↓
Correlation / multicollinearity analysis
       ↓
Feature-target separation
       ↓
80/20 train-test split
       ↓
Feature scaling
       ↓
Train multiple regression models
       ↓
Evaluate on unseen test data
       ↓
Compare models
       ↓
Inspect residuals & feature importance
       ↓
Select the best-performing model
```

### Models tested

#### 1. Linear Regression

Used as the baseline model. It assumes that the target can be reasonably represented as a linear combination of the predictors.

#### 2. Decision Tree Regressor

A tree can split the feature space into regions and therefore capture nonlinear relationships and thresholds that a straight-line model may miss.

#### 3. Random Forest Regressor

A collection of decision trees whose predictions are combined. This generally provides a more stable model than relying on one tree.

#### 4. Gradient Boosting Regressor

Builds trees sequentially, with later trees focusing on the errors made by earlier trees. This makes it powerful for structured nonlinear relationships.

#### 5. Stacking Regressor

A secondary experiment that combines predictions from several base models and feeds them into a final estimator.

---

## 📊 Model Leaderboard

The final test-set comparison from the notebook was:

| Model | R² ↑ | MSE ↓ | RMSE ↓ |
|---|---:|---:|---:|
| **Gradient Boosting** 🏆 | **0.9409** | **2.4761** | **1.5736** |
| Random Forest | 0.8562 | 6.0294 | 2.4555 |
| Decision Tree | 0.8264 | 7.2786 | 2.6979 |
| Stacking | 0.8860 | 4.7788 | 2.1861 |
| Linear Regression | 0.7716 | 9.5737 | 3.0941 |

### 🏆 Winner: Gradient Boosting

Gradient Boosting produced the best test-set performance in this experiment:

- **R² = 0.9409**
- **RMSE = 1.5736°C**
- **MSE = 2.4761**

That means it explained about **94% of the variation in the test-set temperatures** under this experimental setup.

---

## 🤔 Why did Gradient Boosting win?

The results suggest that the temperature relationships are not completely linear.

For example, **day of year** has a strong relationship with temperature, but that relationship does not need to be a straight line. Seasonal effects can change the relationship across different parts of the year.

Likewise, solar radiation can influence temperature differently under different environmental conditions.

### Linear Regression sees something like:

```text
Temperature = β₀ + β₁X₁ + β₂X₂ + ... + error
```

It tries to describe the relationship using one global linear equation.

### Tree-based models can instead learn rules such as:

```text
If day_of_year is in one region
    → temperature behaves one way

If day_of_year is in another region
    → temperature behaves differently

If solar radiation is high
    → the effect can change again
```

That ability to model **thresholds, interactions and nonlinear patterns** is a major reason tree ensembles can outperform Linear Regression on problems like this.

---

## 🌲 Feature Importance

The tree-based models showed a very clear pattern.

### Random Forest

The two dominant predictors were:

- `solar_radiation_w_m2` → **0.5042**
- `day_of_year` → **0.4899**

### Gradient Boosting

The dominant predictors were:

- `day_of_year` → **0.4902**
- `solar_radiation_w_m2` → **0.4478**

This is interesting because it agrees with the earlier correlation analysis: these two variables carry much of the predictive signal in this dataset.

---

## 📉 Residual Analysis

I also examined model residuals:

```text
Residual = Actual Temperature - Predicted Temperature
```

Residual analysis helps answer an important question:

> **Is the model making random errors, or is there still a systematic pattern that the model has not captured?**

Comparing residual behaviour across the models gives a better picture of model quality than looking at R² alone.

---

## ⚠️ Overfitting Check

Training and test scores were compared for several models.

For example:

| Model | Train R² | Test R² |
|---|---:|---:|
| Linear Regression | 0.7558 | 0.7716 |
| Decision Tree | 0.8407 | 0.8264 |
| Random Forest | 0.8895 | 0.8562 |

The Random Forest has a noticeable train-test gap, which is a useful reminder that ensemble models can still overfit depending on their hyperparameters.

The winning Gradient Boosting model achieved a much stronger test result in this experiment, but further cross-validation and tuning would be appropriate before using the approach for a real forecasting system.

---

## 🏁 Final Recommendation

### **Recommended model: Gradient Boosting Regressor**

I would select **Gradient Boosting** for this project because it achieved the strongest unseen-data performance among the models tested.

It also provides a good balance between predictive accuracy and the ability to model nonlinear relationships.

However, I would **not** automatically conclude that Gradient Boosting is always the best climate model. The recommendation is specific to this dataset and this experiment.

For a production-quality system, I would next add:

- Cross-validation
- Hyperparameter tuning
- Time-aware validation if the data represents a true time series
- Additional historical weather observations
- Better handling of seasonal/time features
- External validation on data from another period or location

---

## 🧪 What I Learned

This project helped me move beyond simply training models and focus on **why a model performs the way it does**.

### Key lessons

**1. Correlation is not the same as predictive power.**

A variable with weak linear correlation can still contribute through nonlinear effects or interactions.

**2. Start simple.**

Linear Regression gave me a useful baseline before moving to more complex models.

**3. Tree ensembles are powerful for nonlinear problems.**

Random Forest improved on the single Decision Tree, while Gradient Boosting improved much further.

**4. Always evaluate on unseen data.**

Training performance alone can make a model look better than it really is.

**5. Model comparison is part of the modelling process.**

The best model should be selected from evidence, not because it is a popular algorithm.

---

## 🛠️ Tech Stack

```text
Python
├── Pandas        → Data manipulation
├── NumPy         → Numerical computing
├── Matplotlib    → Visualization
├── Seaborn       → Exploratory data visualization
└── Scikit-learn  → Machine learning
```

---

## 📁 Project Structure

```text
climate-temperature-regression/
│
├── Climate.ipynb
├── climate_regression_practice.csv
├── climate_gradio_app.py
├── README.md
└── README_Climate_Gradio.md
```

---

## ▶️ Run the Project

Clone the repository:

```bash
git clone <your-repository-url>
cd climate-temperature-regression
```

Install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn gradio
```

Open the notebook:

```bash
jupyter notebook Climate.ipynb
```

### Optional: run the interactive Gradio app

```bash
python climate_gradio_app.py
```

The Gradio interface allows users to provide climate measurements and obtain temperature predictions from the trained models.

---

## 💬 Questions I Asked While Building This Project

<details>
<summary>Click to expand</summary>

**Why didn't Linear Regression win?**

Because the climate-target relationship contains patterns that are not fully represented by one global linear equation.

**Why was Random Forest better than one Decision Tree?**

Because combining multiple trees can produce a more stable prediction than relying on a single tree.

**Why did Gradient Boosting perform best?**

Because it sequentially learns from previous errors and can capture complex nonlinear relationships effectively.

**Why should I care about residuals?**

Because a good-looking R² score does not guarantee that the model has captured every important pattern.

</details>

---

## 🔭 Next Step

The next version of this project would move from **model comparison** to **model improvement**:

```text
Baseline models
      ↓
Cross-validation
      ↓
Hyperparameter tuning
      ↓
Feature engineering
      ↓
Time-aware validation
      ↓
Model interpretation
      ↓
Deployment
```

---

## ⭐ If you find this project useful

Feel free to explore the notebook, reproduce the results, and experiment with different hyperparameters.

**The goal of this project was not just to predict temperature — it was to understand the reasoning behind choosing a model.**
