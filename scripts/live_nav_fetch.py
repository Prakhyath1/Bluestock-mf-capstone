from pathlib import Path
import requests
import pandas as pd
import json

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Mutual Fund Schemes
# -----------------------------
schemes = {
    "HDFC_Top100_Direct": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_LargeCap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

# -----------------------------
# Fetch NAV Data
# -----------------------------
BASE_URL = "https://api.mfapi.in/mf/"

for scheme_name, amfi_code in schemes.items():

    print("=" * 80)
    print(f"Fetching: {scheme_name}")
    print(f"AMFI Code: {amfi_code}")

    url = f"{BASE_URL}{amfi_code}"

    try:
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            print(f"❌ Request Failed (Status Code: {response.status_code})")
            continue

        # Parse JSON
        response_json = response.json()

        # Optional: Save raw JSON (useful for debugging)
        with open(
            OUTPUT_DIR / f"{scheme_name}.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(response_json, file, indent=4)

        # Extract NAV history
        nav_data = response_json.get("data", [])

        if not nav_data:
            print("❌ No NAV data found.")
            continue

        # Convert to DataFrame
        df = pd.DataFrame(nav_data)

        # Add metadata
        df["scheme_name"] = scheme_name
        df["amfi_code"] = amfi_code

        # Save CSV
        csv_path = OUTPUT_DIR / f"live_nav_{scheme_name}.csv"
        df.to_csv(csv_path, index=False)

        print("✅ CSV Saved:", csv_path.name)
        print(f"Rows: {len(df)}")

        print("\nFirst 5 Rows:")
        print(df.head())

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

print("\n🎉 Live NAV data fetching completed.")