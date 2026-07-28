from pathlib import Path
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_DIR = PROJECT_ROOT / "Datasets"
REPORT_DIR = PROJECT_ROOT / "reports"

# Create reports folder if it doesn't exist
REPORT_DIR.mkdir(exist_ok=True)

# ==========================================================
# Load Datasets
# ==========================================================
fund_master = pd.read_csv(DATASET_DIR / "01_fund_master.csv")
nav_history = pd.read_csv(DATASET_DIR / "02_nav_history.csv")

# ==========================================================
# Referential Integrity Check
# ==========================================================
master_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_in_nav = master_codes - nav_codes
missing_in_master = nav_codes - master_codes

# ==========================================================
# Display Results
# ==========================================================
print("=" * 80)
print("AMFI CODE VALIDATION REPORT")
print("=" * 80)

print(f"\nTotal AMFI Codes in Fund Master : {len(master_codes)}")
print(f"Total AMFI Codes in NAV History : {len(nav_codes)}")

print("\nCodes in Fund Master but missing from NAV History:")
print(missing_in_nav if missing_in_nav else "None")

print("\nCodes in NAV History but missing from Fund Master:")
print(missing_in_master if missing_in_master else "None")

# ==========================================================
# Overall Status
# ==========================================================
if not missing_in_nav and not missing_in_master:
    status = "PASS"
    summary = (
        "All AMFI codes in the Fund Master dataset are present "
        "in the NAV History dataset. Referential integrity is maintained."
    )
else:
    status = "FAIL"
    summary = (
        "Mismatch detected between Fund Master and NAV History datasets."
    )

print(f"\nValidation Status: {status}")

# ==========================================================
# Save Report
# ==========================================================
report_path = REPORT_DIR / "data_quality_day1.txt"

with open(report_path, "w", encoding="utf-8") as report:
    report.write("DATA QUALITY REPORT - DAY 1\n")
    report.write("=" * 50 + "\n\n")

    report.write(f"Fund Master Records : {len(fund_master)}\n")
    report.write(f"NAV History Records : {len(nav_history)}\n\n")

    report.write(f"Unique AMFI Codes (Fund Master): {len(master_codes)}\n")
    report.write(f"Unique AMFI Codes (NAV History): {len(nav_codes)}\n\n")

    report.write(f"Validation Status: {status}\n\n")

    report.write("Codes missing in NAV History:\n")
    if missing_in_nav:
        for code in sorted(missing_in_nav):
            report.write(f"- {code}\n")
    else:
        report.write("None\n")

    report.write("\nCodes missing in Fund Master:\n")
    if missing_in_master:
        for code in sorted(missing_in_master):
            report.write(f"- {code}\n")
    else:
        report.write("None\n")

    report.write("\nSummary:\n")
    report.write(summary + "\n")

print(f"\n✅ Report saved to: {report_path}")