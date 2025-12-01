import pandas as pd
import numpy as np

def compute_metrics(df, benchmark_df=None):
    # CALCULATE RETURNS FOR BOTH
    df["returns"] = np.log(df["price"] / df["price"].shift(1))

    if benchmark_df is not None:
        benchmark_df["returns"] = np.log(benchmark_df["price"] / benchmark_df["price"].shift(1))

    # Drop NaNs
    df.dropna(inplace=True)
    if benchmark_df is not None:
        benchmark_df.dropna(inplace=True)

    # Volatility
    daily_vol = df["returns"].std()
    annual_vol = daily_vol * np.sqrt(365)

    # Sharpe Ratio
    sharpe = (df["returns"].mean() / df["returns"].std()) * np.sqrt(365)

    # Beta calculation
    beta = None
    if benchmark_df is not None:
        merged = pd.merge(df["returns"], benchmark_df["returns"],
                          left_index=True, right_index=True,
                          suffixes=("", "_btc"))

        cov = merged.cov().iloc[0,1]
        beta = cov / merged["returns_btc"].var()

    return round(daily_vol,4), round(annual_vol,4), round(sharpe,4), round(beta,4) if beta else None
