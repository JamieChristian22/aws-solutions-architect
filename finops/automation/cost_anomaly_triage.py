def classify(delta_pct, monthly_impact):
    if delta_pct >= 30 and monthly_impact >= 5000: return "Critical"
    if delta_pct >= 15 and monthly_impact >= 1000: return "High"
    if delta_pct >= 8: return "Medium"
    return "Low"

if __name__ == "__main__":
    print(classify(22, 3200))
