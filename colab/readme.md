# 📊 Exploratory Data Analysis (EDA) with Pandas & Matplotlib

This project demonstrates basic **Exploratory Data Analysis (EDA)** using Python’s `pandas` and `matplotlib` libraries. It involves loading a dataset, computing statistics, and visualizing feature distributions through histograms.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/appalameenakshisindhuja/hack_week/blob/main/iris_eda.ipynb)


---

## 📁 Features

✔️ Load dataset using `pandas`  
✔️ Perform basic statistical summary  
✔️ Calculate mean, median, and standard deviation  
✔️ Generate `.describe()` summary  
✔️ Visualize each feature using histograms with `matplotlib`

---

## 📚 Libraries Used

- `pandas`
- `matplotlib.pyplot`

You can install them using:
pip install pandas matplotlib

## 🔍 EDA Steps
Load the Dataset
Load data from a CSV file using pandas.read_csv().

## Basic Stats:
Mean: df.mean()
Median: df.median()
Standard Deviation: df.std()
Summary: df.describe()

## Data Visualization
Generate histograms for all numeric features:
import matplotlib.pyplot as plt
df.hist(figsize=(10, 8), bins=20)
plt.tight_layout()
plt.show()

## ▶️ How to Run
Clone this repository or open the notebook in Google Colab.
Run all cells to perform EDA.
Explore printed stats and visualizations.

## 📌 Example Output
Feature-wise summary:
- Mean: ...
- Median: ...
- Std: ...
