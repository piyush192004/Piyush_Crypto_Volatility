def classify_risk(volatility, sharpe):
    if volatility > 0.08 and sharpe < 1:
        return "High Risk"
    elif volatility > 0.04:
        return "Medium Risk"
    else:
        return "Low Risk"
