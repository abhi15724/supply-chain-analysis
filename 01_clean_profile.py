"""
Step 1: Load, profile, and clean the supply chain dataset.
Dataset: 100 SKUs across haircare/skincare/cosmetics, sold by 5 suppliers
across 5 Indian hubs, with pricing, quality (defect/inspection), and
logistics (carrier/route/mode/lead time) data.
"""
import pandas as pd

df = pd.read_csv('/home/claude/supply-chain-project/data/raw_data.csv')

print("SHAPE:", df.shape)
print("\nDTYPES:\n", df.dtypes)
print("\nMISSING VALUES:\n", df.isna().sum().sum(), "total")
print("\nDUPLICATE SKUs:", df['SKU'].duplicated().sum())

# Clean column names -> snake_case for SQL/Python friendliness, keep an Excel-friendly
# label map separately so the Excel workbook still shows human-readable headers.
df.columns = [c.strip() for c in df.columns]

# Standardize text categories (strip whitespace, consistent casing where relevant)
text_cols = df.select_dtypes(include='object').columns
for c in text_cols:
    df[c] = df[c].astype(str).str.strip()

# Derived fields used across SQL/Python/Excel layers
df['Profit'] = df['Revenue generated'] - df['Manufacturing costs'] - df['Shipping costs'] - df['Costs']
df['Profit margin %'] = (df['Profit'] / df['Revenue generated']) * 100
df['Total logistics cost'] = df['Shipping costs'] + df['Costs']
df['Days of stock cover'] = df['Stock levels'] / (df['Number of products sold'] / 30).replace(0, 0.01)
df['Defect rate %'] = df['Defect rates']  # already a percentage-like figure in source

# Data quality note: Inspection results has a 'Pending' category alongside Pass/Fail —
# kept as-is (not imputed) since it's a legitimate real-world status, not missing data.

df.to_csv('/home/claude/supply-chain-project/data/cleaned_data.csv', index=False)

print("\nSaved cleaned_data.csv:", df.shape)
print("\nCategory counts:")
for c in ['Product type', 'Supplier name', 'Location', 'Shipping carriers', 'Transportation modes', 'Routes', 'Inspection results']:
    print(f"\n{c}:")
    print(df[c].value_counts())

print("\nProfit summary:")
print(df[['Profit', 'Profit margin %']].describe())
