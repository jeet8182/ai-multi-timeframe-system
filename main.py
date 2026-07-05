from fastapi import FastAPI

app = FastAPI()

# ---------------- 4H TREND ----------------
def get_4h_trend():
    # replace later with real data
    return "BULLISH"

# ---------------- 1H LEVELS ----------------
def get_1h_levels():
    return {
        "support": 100,
        "resistance": 110,
        "fvg": True,
        "order_block": True,
        "mitigation_block": True,
        "premium_zone": True
    }

# ---------------- M1 DATA ----------------
def get_m1_candles():
    return [
        {"open": 100, "close": 101},
        {"open": 101, "close": 100},
        {"open": 100, "close": 102}
    ]

# ---------------- FLCC ----------------
def flcc(c):
    if len(c) < 3:
        return False
    return (
        c[-3]["close"] < c[-3]["open"] and
        c[-2]["close"] > c[-2]["open"] and
        c[-1]["close"] < c[-1]["open"]
    )

# ---------------- REVERSAL ----------------
def reversal(c):
    return c[-1]["close"] > c[-1]["open"]

# ---------------- ENTRY LOGIC ----------------
def generate_signal():

    trend = get_4h_trend()
    levels = get_1h_levels()
    m1 = get_m1_candles()

    price_touch = True  # assume price is at level (simulation)

    flcc_ok = flcc(m1)
    reversal_ok = reversal(m1)

    if trend != "BULLISH":
        return {"signal": "SKIP", "reason": "Not in 4H trend"}

    if not price_touch:
        return {"signal": "SKIP", "reason": "No level touch"}

    if flcc_ok and reversal_ok:
        return {
            "signal": "CALL",
            "trend": trend,
            "reason": "FLCC + Reversal confirmed"
        }

    return {
        "signal": "SKIP",
        "trend": trend,
        "reason": "No valid M1 setup"
    }

# ---------------- API ----------------
@app.get("/")
def home():
    return {"status": "Multi-Timeframe System Running"}

@app.get("/signal")
def signal():
    return generate_signal()
