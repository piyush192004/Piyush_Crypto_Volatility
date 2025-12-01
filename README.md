# Crypto Volatility & Risk Analyzer 🚀

A **Crypto Volatility & Risk Analyzer** built with Python + Streamlit — fetches cryptocurrency price data, computes risk & return metrics, and provides interactive charts + dashboards for analysis and comparison.

---

## 📁 Repository Structure

```
Piyush_Crypto_Volatility/
│
├── data/                   ← Folder containing CSV files with historical price data (one file per coin)
├── app.py                  ← Main Streamlit dashboard application
├── data_fetcher.py         ← Script to fetch data (e.g. from APIs) and store CSVs
├── risk_calculations.py    ← Core logic: compute volatility, returns, Sharpe, beta, etc.
├── risk_classifier.py      ← Risk‑level classification logic (Low / Medium / High)
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## 🚀 Getting Started — How to Run the Dashboard Locally

### 1. Clone the repository

```bash
git clone https://github.com/piyush192004/Piyush_Crypto_Volatility.git
cd Piyush_Crypto_Volatility
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Ensure Data Availability

Make sure you have historical CSV files inside the `data/` directory.  
Use `data_fetcher.py` to fetch data if not present.

### 4. Run the Streamlit app

```bash
python -m streamlit run app.py
```

### 5. Open the dashboard

Open your browser and visit:  
http://localhost:8501

---

## ✅ Features

- 📈 Price Charts – Visualize historical price trends
- 📉 Rolling Volatility Charts – Monitor changing volatility
- 🎯 Risk–Return Scatter – Compare risk vs return across coins
- 🔁 Multi-Crypto Comparison – View multiple currencies together
- 📊 Risk Metrics – Volatility, Sharpe Ratio, Beta, Risk Level
- 🗓️ Date Filter & Rolling Window Control

---

## 🧰 Tech Stack

- Python 3.x
- Pandas / NumPy
- Plotly Express
- Streamlit

---

## ⚙️ How It Works

1. Fetch price data (API or CSV)
2. Calculate returns and volatility
3. Derive risk metrics
4. Visualize using Streamlit and Plotly

---

## 📈 Why Use This Project?

✅ Simple and clear crypto risk analysis  
✅ Beginner & analyst friendly  
✅ Supports multiple cryptocurrencies  
✅ Fully open-source and self‑hosted

---

## 💡 Future Enhancements

- Value at Risk (VaR)
- Real-time data updates
- Export reports (CSV / PDF)
- Web deployment
- Correlation heatmaps

---

## 👤 Author

**Piyush** — This project is part of Intern at Infosys Springboard

---

## 📄 License

This project is open-source. You are free to use, modify, and distribute it.
