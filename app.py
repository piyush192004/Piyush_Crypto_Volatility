import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from risk_calculations import compute_metrics
from risk_classifier import classify_risk

# Header
st.set_page_config(page_title="Crypto Risk Analyzer", layout="wide")

#Coin Data
COIN_LOGOS = {
    "bitcoin": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
    "ethereum": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
    "solana": "https://assets.coingecko.com/coins/images/4128/large/solana.png",
    "dogecoin": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png",
    "cardano": "https://assets.coingecko.com/coins/images/975/large/cardano.png"
}

COIN_SYMBOLS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "solana": "SOL",
    "dogecoin": "DOGE",
    "cardano": "ADA"
}

coins = ["bitcoin", "ethereum", "solana", "dogecoin", "cardano"]

#Side Controls
st.sidebar.title("Controls")
selected = st.sidebar.selectbox("Select Cryptocurrency (Single View)", coins)
multi_select = st.sidebar.multiselect(
    "Select Cryptos for Comparison",
    coins,
    default=coins[:3]
)

date_range = st.sidebar.date_input("Select Date Range", [])
rolling_window = st.sidebar.slider("Rolling Volatility Window (Days)", 7, 60, 30)

#Loading Data
df = pd.read_csv(f"data/{selected}.csv", parse_dates=["timestamp"])
df.set_index("timestamp", inplace=True)

btc = pd.read_csv("data/bitcoin.csv", parse_dates=["timestamp"])
btc.set_index("timestamp", inplace=True)

#Display Coin Selection
logo_url = COIN_LOGOS.get(selected)
symbol = COIN_SYMBOLS.get(selected).upper()
coin_name = selected.capitalize()
latest_price = round(df["price"].iloc[-1], 2)

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:15px;">
        <img src="{logo_url}" width="48"/>
        <div>
            <h1 style="margin:0;">Crypto Volatility and Risk Analyzer</h1>
            <h3 style="color:#00ffcc; margin-top:4px;">
                {coin_name} ({symbol}) — ₹ {latest_price:,.2f}
            </h3>
        </div>
    </div>
    <hr>
    """,
    unsafe_allow_html=True
)

#Data Range
def apply_date_filter(data):
    if len(date_range) == 2:
        start, end = date_range
        return data.loc[start:end]
    return data

df = apply_date_filter(df)
btc = apply_date_filter(btc)

#Metrics
daily, annual, sharpe, beta = compute_metrics(df.copy(), btc.copy())
risk = classify_risk(daily, sharpe)

#Title
st.title("Crypto Volatility & Risk Analyzer")

#Metrics Display
st.subheader("Key Risk Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Daily Volatility", daily)
col2.metric("Annual Volatility", annual)
col3.metric("Sharpe Ratio", sharpe)
col4.metric("Beta (vs BTC)", beta if beta else "N/A")

st.info(f"Risk Level: *{risk}*")

#Price Trend Chart
st.subheader("Price Trend")

fig_price = px.line(df, y="price", title=f"{selected.upper()} Price Trend")
st.plotly_chart(fig_price, use_container_width=True)

#Volatility Chart
st.subheader("Rolling Volatility")

df["returns"] = df["price"].pct_change()
df["rolling_vol"] = df["returns"].rolling(rolling_window).std() * np.sqrt(365)

fig_vol = px.line(df, y="rolling_vol", title=f"{selected.upper()} Rolling Volatility")
st.plotly_chart(fig_vol, use_container_width=True)

#Multiple Coin Comparison Chart
st.subheader("Multi-Crypto Price Comparison")

compare_df = []

for coin in multi_select:
    temp = pd.read_csv(f"data/{coin}.csv", parse_dates=["timestamp"])
    temp.set_index("timestamp", inplace=True)
    temp = apply_date_filter(temp)
    temp["coin"] = coin
    compare_df.append(temp)

compare_df = pd.concat(compare_df)

fig_compare = px.line(
    compare_df,
    x=compare_df.index,
    y="price",
    color="coin",
    title="Multi-Crypto Price Comparison"
)
st.plotly_chart(fig_compare, use_container_width=True)

#Risk Return Scatter Chart
st.subheader("Risk vs Return Scatter Plot")

risk_data = []

for coin in multi_select:
    temp = pd.read_csv(f"data/{coin}.csv", parse_dates=["timestamp"])
    temp.set_index("timestamp", inplace=True)
    temp = apply_date_filter(temp)

    btc_ref = pd.read_csv("data/bitcoin.csv", parse_dates=["timestamp"])
    btc_ref.set_index("timestamp", inplace=True)
    btc_ref = apply_date_filter(btc_ref)

    d, a, s, b = compute_metrics(temp.copy(), btc_ref.copy())
    risk_data.append({
        "Coin": coin.upper(),
        "Annual Volatility": a,
        "Sharpe Ratio": s
    })

risk_df = pd.DataFrame(risk_data)
risk_df["BubbleSize"] = risk_df["Sharpe Ratio"].abs()

fig_scatter = px.scatter(
    risk_df,
    x="Annual Volatility",
    y="Sharpe Ratio",
    text="Coin",
    title="Risk-Return Map",
    size="BubbleSize",
)

fig_scatter.update_traces(textposition="top center")
st.plotly_chart(fig_scatter, use_container_width=True)
