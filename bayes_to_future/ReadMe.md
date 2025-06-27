# 🩺 Heart Disease Risk Prediction using Bayesian Networks

Welcome to **MediMystery Labs**! This project is designed to detect and analyze the **risk of heart disease** using a probabilistic model built with a **Bayesian Network** powered by the `pgmpy` library.

## 🔍 Objective

Use a dataset of simulated patient records to:
- Clean and normalize the data
- Define a Bayesian Network structure (causal relationships)
- Train the model using Maximum Likelihood Estimation (MLE)
- Perform probabilistic inference based on user-provided inputs (like age, fasting blood sugar)
- Predict the likelihood of heart disease (`target`) and related features (`chol`, `thalach`)

---

## 📁 Files Included

| File | Description |
|------|-------------|
| `heart_disease.csv` | Raw dataset of patient medical records |
| `cleaned_heartdisease.csv` | Cleaned dataset (no nulls or duplicates) |
| `structure.json` | JSON file defining the Bayesian network structure |
| `heart_disease_bn.py` | Python script to build, train, and infer from the model |
| `README.md` | Project documentation (this file) |

---

## 🧠 Bayesian Network Structure

Defined in `structure.json` as:

age → fbs → target → chol, thalach

markdown
Copy
Edit

This means:
- `age` influences `fbs` (fasting blood sugar)
- `fbs` influences `target` (heart disease)
- `target` influences `chol` (cholesterol) and `thalach` (max heart rate)

---

## 🚀 How to Run

### 1. 🔧 Install Dependencies
pip install pandas scikit-learn pgmpy matplotlib networkx

### 2. 🧠 Run the Model

3. 🗣️ Input Evidence (Raw values)
When prompted, enter raw values like:
age=58, fbs=130
The script will normalize these values automatically and perform inference to predict other probabilities such as target, chol, and thalach.


📈 Visualizations
The Bayesian Network structure is also displayed graphically using networkx and matplotlib.
## Screenshot

![App Screenshot](imagecopy.png)

