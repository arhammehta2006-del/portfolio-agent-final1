"""
config.py - all the tunable numbers in ONE place.
Change a number here and the whole app follows, so every choice is easy to explain in the viva.
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- The nine asset classes the portfolios are built from ----
# REVISED (Oct-2026): real-data-based, 2016-2025 - see Portfolio_Methodology.xlsx ('2. Assumptions' /
# 'Assumption Calculations' / 'Market Data' sheets) for full sourcing and calculations.
ASSETS = ["Liquid Fund", "Debt Fund", "Gold", "Real Estate", "Equity",
          "Large Cap Mutual Fund", "Mid Cap Mutual Fund", "Small Cap Mutual Fund", "Flexi Cap Mutual Fund"]

# ---- Return / risk assumptions -------------------------------------------------
# Loaded from data/assumptions.csv. Falls back to these (same real-data figures) if that file is
# missing or malformed - see build_assumptions.py for how they were computed.
_DEFAULTS = {
    "Liquid Fund": (0.054, 0.015),
    "Debt Fund": (0.069, 0.030),
    "Gold": (0.115, 0.215),
    "Real Estate": (0.119, 0.090),
    "Equity": (0.134, 0.165),
    "Large Cap Mutual Fund": (0.129, 0.165),
    "Mid Cap Mutual Fund": (0.153, 0.235),
    "Small Cap Mutual Fund": (0.162, 0.315),
    "Flexi Cap Mutual Fund": (0.131, 0.165),
}


def load_assumptions():
    """Return (dict asset -> (expected_return, volatility), source_note)."""
    path = os.path.join(BASE_DIR, "data", "assumptions.csv")
    try:
        df = pd.read_csv(path)
        out = {r["asset"]: (float(r["expected_return"]), float(r["volatility"])) for _, r in df.iterrows()}
        for a in ASSETS:
            if a not in out:
                raise ValueError(f"{a} missing in assumptions.csv")
        note = "Loaded from data/assumptions.csv"
        if df["source"].astype(str).str.contains("PLACEHOLDER").any():
            note += " (contains PLACEHOLDER values - replace with your own historical data)"
        return out, note
    except Exception as e:  # never crash the demo because of a data file
        return dict(_DEFAULTS), f"Using built-in placeholder assumptions ({e})"


ASSUMPTIONS, ASSUMPTIONS_NOTE = load_assumptions()

# Correlations between asset classes, computed from real 2016-2025 return series - see
# Portfolio_Methodology.xlsx 'Assumption Calculations'. Order matches ASSETS above:
#            Liquid   Debt     Gold     RE       Equity   LCMF     MCMF     SCMF     FCMF
CORR = [
    [1.000000, 0.268688, 0.099785, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],  # Liquid Fund
    [0.268688, 1.000000, 0.269267, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],  # Debt Fund
    [0.099785, 0.269267, 1.000000, 0.563535, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000],  # Gold
    [0.000000, 0.000000, 0.563535, 1.000000, 0.153333, 0.153333, 0.153333, 0.153333, 0.153333],  # Real Estate
    [0.000000, 0.000000, 0.000000, 0.153333, 1.000000, 0.988224, 0.905402, 0.878006, 0.958663],  # Equity
    [0.000000, 0.000000, 0.000000, 0.153333, 0.988224, 1.000000, 0.945435, 0.921797, 0.986208],  # Large Cap MF
    [0.000000, 0.000000, 0.000000, 0.153333, 0.905402, 0.945435, 1.000000, 0.991152, 0.985054],  # Mid Cap MF
    [0.000000, 0.000000, 0.000000, 0.153333, 0.878006, 0.921797, 0.991152, 1.000000, 0.971088],  # Small Cap MF
    [0.000000, 0.000000, 0.000000, 0.153333, 0.958663, 0.986208, 0.985054, 0.971088, 1.000000],  # Flexi Cap MF
]

# ---- Planning assumptions ------------------------------------------------------
INFLATION = 0.05            # yearly rise in costs (goal costs are entered in today's rupees)
PLANNING_MARGIN = 0.01      # we plan with returns 1 percentage point lower than expected (prudence)
RETIREMENT_MULTIPLE = 25    # retirement corpus = 25 x yearly expenses (the "4% rule")
DEFAULT_WEALTH_YEARS = 15   # horizon used for surplus money with no goal attached
N_SIMS = 2000               # number of simulated futures for the probability estimates
SEED = 42                   # fixed seed -> same inputs always give the same numbers (good for demos)

# ---- Horizon buckets (years) ----------------------------------------------------
CAPITAL_PROTECTION_YEARS = 1   # goals this close are held 100% in liquid funds
SHORT_MAX_YEARS = 3            # up to 3 years = short term
MEDIUM_MAX_YEARS = 7           # more than 3 up to 7 years = medium term, above 7 = long term

# ---- Risk-score labels -----------------------------------------------------------
CONSERVATIVE_BELOW = 4.0
AGGRESSIVE_FROM = 7.0
PROFILES = ["Conservative", "Moderate", "Aggressive"]

# =========================================================================
# ADDITIONS BELOW THIS LINE support the expanded financial-profile,
# emergency-fund, debt, goal-priority, step-up-SIP and risk-metric features.
# Every number here is a stated, documented assumption — see the
# "Assumptions & Methodology" panel the app renders from this file.
# =========================================================================

# ---- Goal priority tiers (used to decide funding order under a budget constraint) ----
PRIORITIES = ["Essential", "Important", "Aspirational"]
PRIORITY_ORDER = {p: i for i, p in enumerate(PRIORITIES)}   # Essential funded first

# ---- Goal-type-specific inflation (item 23: different expenses inflate differently) ----
# PLACEHOLDER figures — replace with RBI/CPI sub-index data if available for your submission.
GOAL_INFLATION = {
    "General": 0.05,
    "Education": 0.08,
    "Healthcare": 0.09,
    "Travel": 0.05,
    "Housing": 0.06,
}
DEFAULT_GOAL_INFLATION_CATEGORY = "General"

# ---- Employment types and how they affect risk CAPACITY and emergency-fund months ----
EMPLOYMENT_TYPES = ["Salaried", "Self-employed / business owner", "Freelancer / professional", "Student", "Retired", "Other"]

# Months of essential expenses recommended in the emergency fund, by employment stability.
# These are PLACEHOLDER planning norms (commonly cited retail financial-planning heuristics),
# not a regulatory requirement — stated explicitly so the assumption is visible, not silent.
EMERGENCY_MONTHS_BASE = {
    "Salaried": 4,
    "Self-employed / business owner": 8,
    "Freelancer / professional": 8,
    "Student": 3,
    "Retired": 6,
    "Other": 6,
}
EMERGENCY_MONTHS_PER_DEPENDENT = 1     # +1 month of buffer per financial dependent
EMERGENCY_MONTHS_CAP = 12              # don't ask for more than a year's buffer

# Employment-type effect on risk CAPACITY points (1-10 scale, same scale as age/dependents/etc in risk.py).
# Stable, predictable income supports more capacity for market risk; irregular or no income reduces it.
EMPLOYMENT_CAPACITY_PTS = {
    "Salaried": 7,
    "Self-employed / business owner": 5,
    "Freelancer / professional": 4,
    "Student": 5,
    "Retired": 3,
    "Other": 5,
}

# ---- Debt / affordability checks ----
HIGH_EMI_BURDEN_RATIO = 0.40     # EMIs above this share of monthly income are flagged as a high debt burden
HIGH_INTEREST_DEBT_RATE = 0.12   # loans costlier than this are flagged as "consider repaying before investing more"

# ---- Existing-portfolio awareness (item 19) ----
# How much new-money allocation is pulled toward asset classes the client is currently underweight in,
# when they report an already-concentrated existing portfolio. 0 = ignore existing holdings, 1 = fully offset them.
EXISTING_PORTFOLIO_OFFSET = 0.5

# ---- Risk metrics (item 14) ----
RISK_FREE_RATE = 0.053   # Real-data based — approx short-term G-Sec/liquid-fund yield, for the Sharpe ratio calc only

# ---- Step-up SIP default ----
DEFAULT_SIP_STEP_UP_ENABLED = False   # off unless the user turns it on
DEFAULT_SIP_STEP_UP = 0.0             # 0% unless the user says otherwise

# ---- Income/expense growth (new) ----
# Expenses are assumed to grow with general inflation, plus this fraction of any REAL (above-
# inflation) income growth - a commonly-cited "lifestyle creep" planning heuristic (people
# typically save 60-70% of a raise). Documented explicitly rather than silently assumed -
# see allocation.expense_growth_rate().
LIFESTYLE_CREEP_FACTOR = 0.3
