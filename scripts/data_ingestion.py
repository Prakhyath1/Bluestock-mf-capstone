from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_ROOT / "Datasets"

# ==========================================================
# List of CSV Files
# ==========================================================
csv_files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]

# ==========================================================
# Read Every Dataset
# ==========================================================
for filename in csv_files:

    file_path = DATASET_DIR / filename

    print("=" * 80)
    print(f"File: {filename}")

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        continue

    try:
        # ------------------------------------------------------
        # Load CSV
        # ------------------------------------------------------
        df = pd.read_csv(file_path)

        # ------------------------------------------------------
        # Basic Information
        # ------------------------------------------------------
        print(f"\nShape: {df.shape}")

        print("\nData Types:")
        print(df.dtypes)

        print("\nFirst 5 Rows:")
        print(df.head())

        # ======================================================
        # Exploratory Analysis for Fund Master
        # ======================================================
        if filename == "01_fund_master.csv":

            print("\n" + "=" * 80)
            print("EXPLORATORY DATA ANALYSIS - FUND MASTER")
            print("=" * 80)

            # Unique Fund Houses
            print("\nUnique Fund Houses:")
            print(df["fund_house"].unique())

            print(
                f"\nTotal Fund Houses (AMCs): {df['fund_house'].nunique()}"
            )

            # Category Distribution
            print("\nCategory Distribution:")
            print(df["category"].value_counts())

            # Sub-category Distribution
            print("\nSub-Category Distribution:")
            print(df["sub_category"].value_counts())

            # Risk Category Distribution
            print("\nRisk Category Distribution:")
            print(df["risk_category"].value_counts())

        # ------------------------------------------------------
        # Missing Values
        # ------------------------------------------------------
        print("\nMissing Values:")
        missing = df.isnull().sum()
        print(missing)

        # ------------------------------------------------------
        # Duplicate Rows
        # ------------------------------------------------------
        duplicates = df.duplicated().sum()
        print(f"\nDuplicate Rows: {duplicates}")

        # ======================================================
        # Anomaly Detection
        # ======================================================
        print("\nAnomaly Summary:")

        anomalies = []

        # Missing Values
        missing_cols = missing[missing > 0]

        if not missing_cols.empty:
            anomalies.append(
                f"Missing values found in: {', '.join(missing_cols.index)}"
            )

        # Duplicate Rows
        if duplicates > 0:
            anomalies.append(f"{duplicates} duplicate rows found.")

        # Data Type Checks
        for col in df.columns:

            col_lower = col.lower()

            # Date stored as text
            if "date" in col_lower and df[col].dtype == "object":
                anomalies.append(
                    f"{col}: Date column stored as text."
                )

            # NAV stored as text
            if "nav" in col_lower and df[col].dtype == "object":
                anomalies.append(
                    f"{col}: NAV column stored as text."
                )

            # AMFI Code
            if "amfi" in col_lower and "code" in col_lower:
                anomalies.append(
                    f"{col}: Data type is {df[col].dtype}"
                )

        if anomalies:
            for anomaly in anomalies:
                print(f"- {anomaly}")
        else:
            print("No obvious anomalies detected.")

    except Exception as e:
        print(f"❌ Error reading file: {e}")

# ==========================================================
# Completed
# ==========================================================
print("\n✅ Data ingestion completed successfully.")