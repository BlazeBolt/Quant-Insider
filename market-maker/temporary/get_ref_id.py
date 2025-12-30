from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.refdata.instruments import InstrumentData

nubra = InitNubraSdk(NubraEnv.UAT, env_creds=True)
instruments = InstrumentData(nubra)

df = instruments.get_instruments_dataframe()

# Filter strictly for NIFTY options expiring on 6 Jan 2026
nifty_2026 = df[
    (df["asset"] == "NIFTY") &
    (df["derivative_type"] == "OPT") &
    (df["exchange"] == "NSE") &
    (df["expiry"] == 20260106)
]

print("Total NIFTY options expiring 6 Jan 2026:", len(nifty_2026))

# Sort by strike to visually inspect ATM region
print(
    nifty_2026[
        ["ref_id", "nubra_name", "strike_price", "option_type", "lot_size", "tick_size"]
    ]
    .sort_values("strike_price")
)
# Get approximate ATM using median strike
atm_strike = nifty_2026["strike_price"].median()
print("Approx ATM strike:", atm_strike)

# Show ATM CE & PE
atm = nifty_2026[
    nifty_2026["strike_price"] == atm_strike
]

print("\nATM Options:")
print(atm[["ref_id", "nubra_name", "option_type", "lot_size", "tick_size"]])
# Convert strike to index points (for sanity check only)
nifty_2026["strike_index"] = nifty_2026["strike_price"] / 100

# Approximate NIFTY spot from middle of strikes
approx_spot = nifty_2026["strike_price"].median()

# Find closest strike
nifty_2026["dist"] = abs(nifty_2026["strike_price"] - approx_spot)
atm_row = nifty_2026.sort_values("dist").iloc[0]

print("\nSelected ATM option:")
print(atm_row[["ref_id", "nubra_name", "strike_price", "option_type", "lot_size", "tick_size"]])
