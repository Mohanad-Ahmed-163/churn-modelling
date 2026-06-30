<div align="center">

# 🏦 Churn Modelling API

**End-to-End Machine Learning Project with FastAPI & Docker**

Predict whether a bank customer is likely to churn using machine learning models deployed through a secure FastAPI REST API.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-orange?logo=scikitlearn)
![XGBoost](https://img.shields.io/badge/XGBoost-Latest-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-success)

[Overview](#-project-overview) •
[Features](#-features) •
[Dataset](#-dataset) •
[Results](#-model-performance) •
[API](#-api-reference) •
[Installation](#%EF%B8%8F-installation) •
[Tech Stack](#%EF%B8%8F-technologies-used)

</div>

---

## 📖 Project Overview

Customer churn prediction is one of the most valuable machine learning applications in the banking industry — retaining an existing customer is far cheaper than acquiring a new one.

This project implements a complete ML pipeline that predicts whether a customer will leave a bank, based on their demographic and financial profile. Beyond model training, it demonstrates how to package a trained model into a **production-ready REST API** using FastAPI, secure it with API key authentication, and prepare it for containerized deployment with Docker.

---

## ✨ Features

- 📊 Exploratory data analysis & visualization
- 🧹 Data cleaning and feature engineering
- 📈 Statistical feature selection (ANOVA & Chi-Square)
- ⚙️ Scikit-Learn preprocessing pipeline
- ⚖️ Imbalanced dataset handling (class weights & SMOTE)
- 🤖 Multiple models: Logistic Regression, Random Forest, XGBoost
- 🎯 Hyperparameter tuning (GridSearchCV / RandomizedSearchCV)
- 🌳 Feature importance analysis
- 🚀 REST API built with FastAPI
- 🔐 API key authentication
- 🐳 Docker support
- 🧱 Modular, production-style project structure

---

## 📂 Dataset

**Source:** [Kaggle — Churn Modelling Dataset](https://www.kaggle.com/)

The dataset contains records for **10,000 bank customers**.

| Feature | Description |
|---|---|
| `CreditScore` | Customer credit score |
| `Geography` | Customer country |
| `Gender` | Male / Female |
| `Age` | Customer age |
| `Tenure` | Years with the bank |
| `Balance` | Current account balance |
| `NumOfProducts` | Number of bank products held |
| `HasCrCard` | Owns a credit card (0/1) |
| `IsActiveMember` | Active customer (0/1) |
| `EstimatedSalary` | Estimated yearly salary |

**Target variable**

| Target | Description |
|---|---|
| `Exited` | `1` = customer left the bank, `0` = customer stayed |

### Dataset Summary

| Metric | Value |
|---|---|
| Samples | 10,000 |
| Features | 10 |
| Missing values | None |
| Numerical features | 8 |
| Categorical features | 2 |

### Target Distribution

| Class | Percentage |
|---|---|
| Stayed | 79.63% |
| Churned | 20.37% |

The dataset is clearly **imbalanced**, which motivated experimenting with multiple imbalance-handling techniques.

---

## 🔎 Exploratory Data Analysis

Key visualizations performed during EDA:

- Age, salary, geography, and gender distributions
- Churn distribution
- Active members vs. churn
- Credit card ownership vs. churn
- Correlation analysis & outlier detection

**Key observations**

- Older customers tend to churn more frequently.
- Customers with fewer banking products have higher churn rates.
- Active members are significantly less likely to leave.
- Germany shows a higher churn rate than France and Spain.

---

## ⚙️ Data Preprocessing

Implemented using **Scikit-Learn Pipelines** and `ColumnTransformer`.

| Feature type | Steps |
|---|---|
| Numerical | Median imputation → Standard scaling |
| Categorical | Most-frequent imputation → One-hot encoding (drop first) |
| Other | Most-frequent imputation |

The fitted pipeline is persisted as `preprocessor.pkl` and reused at inference time inside the FastAPI app.

---

## 📈 Statistical Feature Analysis

| Test | Applied to | Significant features |
|---|---|---|
| ANOVA | Numerical features | Age, CreditScore, Balance, EstimatedSalary |
| Chi-Square | Categorical features | Gender, Geography |

Both tests confirmed meaningful relationships between the selected features and the target variable.

---

## ⚖️ Handling Class Imbalance

With only ~20% of customers churning, two strategies were evaluated and compared using the **F1 score** (more appropriate than accuracy for imbalanced classification):

1. **Class weighting** — used with Logistic Regression and Random Forest
2. **SMOTE oversampling** — applied to balance the training set before fitting

---

## 🤖 Models Trained

| Model | Purpose |
|---|---|
| Logistic Regression | Baseline model |
| Logistic Regression + Class Weight | Imbalance handling |
| Logistic Regression + SMOTE | Imbalance handling |
| Random Forest | Tree-based model |
| Random Forest + SMOTE | Improved RF |
| Tuned Random Forest | GridSearchCV |
| XGBoost | Gradient boosting |
| Tuned XGBoost | RandomizedSearchCV |

---

## 📊 Model Performance

| Model | Train F1 | Test F1 |
|---|---:|---:|
| Logistic Regression | 30.89% | 37.50% |
| Logistic + Class Weight | 49.81% | 49.91% |
| Logistic + SMOTE | 49.74% | 50.42% |
| Random Forest | 59.90% | 57.88% |
| Random Forest + SMOTE | 61.96% | 59.27% |
| **⭐ Tuned Random Forest** | **68.01%** | **62.37%** |
| XGBoost | 70.29% | 59.55% |
| Tuned XGBoost | 62.41% | 61.18% |

### ⭐ Best Model

Although XGBoost achieved a higher training score, the **tuned Random Forest** showed the strongest balance between training and test performance, indicating better generalization. It was selected as the primary deployed model.

```
Training F1: 68.01%
Testing F1:  62.37%
```

---

## 🌳 Feature Importance

Top predictors identified by the tuned Random Forest:

| Rank | Feature | Importance |
|---|---|---:|
| 1 | Age | 0.3703 |
| 2 | NumOfProducts | 0.2515 |
| 3 | Balance | 0.0911 |
| 4 | IsActiveMember | 0.0654 |
| 5 | Geography (Germany) | 0.0521 |
| 6 | CreditScore | 0.0520 |
| 7 | EstimatedSalary | 0.0511 |
| 8 | Tenure | 0.0295 |
| 9 | Gender | 0.0235 |
| 10 | Geography (Spain) | 0.0069 |
| 11 | HasCrCard | 0.0065 |

---

## 🚀 API Reference

The trained models are served via **FastAPI**, with interactive Swagger documentation auto-generated at:

```
http://127.0.0.1:8000/docs
```

### 🔐 Authentication

All prediction endpoints require an API key passed in the request header:

```
X_API_Key: YOUR_SECRET_KEY
```

The key is loaded securely from a `.env` file and never hardcoded.

### Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check / welcome message |
| `POST` | `/predict/forest` | Predict churn using the tuned Random Forest model |
| `POST` | `/predict/xgboost` | Predict churn using the tuned XGBoost model |

**Home response**

```json
{
  "Welcome": "Welcome to churn-modelling API v1.0"
}
```

**Example request**

```json
{
  "CreditScore": 650,
  "Geography": "France",
  "Gender": "Male",
  "Age": 35,
  "Tenure": 5,
  "Balance": 75000.5,
  "NumOfProducts": 2,
  "HasCrCard": 1,
  "IsActiveMember": 1,
  "EstimatedSalary": 85000.75
}
```

**Example response**

```json
{
  "churn prediction": false,
  "churn probability": 0.1846
}
```

---

## 📁 Project Structure

```
churn-modelling
│
├── DataSet
│   └── churn-data.csv
│
├── models
│   ├── forest_tuned.pkl
│   ├── xgb-tuned.pkl
│   └── preprocessor.pkl
│
├── Notebooks
│   └── notebook.ipynb
│
├── utils
│   ├── __init__.py
│   ├── config.py
│   ├── CustomerData.py
│   └── inference.py
│
├── main.py
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🐳 Docker Support

Build the image:

```bash
docker build -t churn-modelling-api .
```

Run the container:

```bash
docker run -p 8000:8000 churn-modelling-api
```

---

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/Mohanad-Ahmed-163/churn-modelling.git
cd churn-modelling
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```env
APP_NAME="churn-modelling"
VERSION="1.0"
SECRET_KEY="YOUR_SECRET_KEY"
```

**4. Run the application**

```bash
uvicorn main:app --reload
```

**5. Open the interactive docs**

```
http://127.0.0.1:8000/docs
```

---

## 🛠️ Technologies Used

| Category | Tools |
|---|---|
| Language | Python |
| Data Analysis | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Machine Learning | Scikit-Learn, XGBoost, Imbalanced-Learn |
| Model Persistence | Joblib |
| Backend | FastAPI, Pydantic |
| Deployment | Docker |
| Version Control | Git, GitHub |

---

## 📌 Future Improvements

- [ ] Deploy the API on AWS, Azure, or Google Cloud
- [ ] Integrate CI/CD with GitHub Actions
- [ ] Add model monitoring and logging
- [ ] Persist predictions to a database
- [ ] Build a React frontend
- [ ] Improve performance with CatBoost / LightGBM
- [ ] Add automated testing with Pytest
- [ ] Implement rate limiting and request logging
- [ ] Add Prometheus & Grafana monitoring
- [ ] Deploy using Kubernetes

---

## 👨‍💻 Author

**Mohanad Ahmed**
Artificial Intelligence Student · Machine Learning Engineer in Progress

Interested in: Machine Learning · Deep Learning · Generative AI · NLP · Computer Vision · MLOps

GitHub: [@Mohanad-Ahmed-163](https://github.com/Mohanad-Ahmed-163)

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub — it helps the project reach more people and motivates future improvements.

---

## 📜 License

This project is released under the **MIT License**. Feel free to use, modify, and distribute it for educational and research purposes.
