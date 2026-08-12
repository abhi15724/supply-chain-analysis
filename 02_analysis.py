"""
Step 3: Deeper analysis — correlations and segmentation that are
awkward to express in SQL but easy in pandas.
"""
import pandas as pd

df = pd.read_csv('/home/claude/supply-chain-project/data/cleaned_data.csv')

# --- Correlation matrix among the key numeric levers ---
cols = ['Price', 'Defect rate %', 'Lead time', 'Manufacturing lead time',
        'Manufacturing costs', 'Shipping costs', 'Profit margin %', 'Revenue generated']
corr = df[cols].corr(numeric_only=True).round(2)
print("CORRELATION MATRIX:\n", corr.to_string())

# Key relationships worth calling out
print("\nManufacturing lead time vs Defect rate correlation:",
      round(df['Manufacturing lead time'].corr(df['Defect rate %']), 3))
print("Price vs Profit margin % correlation:",
      round(df['Price'].corr(df['Profit margin %']), 3))
print("Shipping cost vs Shipping time correlation:",
      round(df['Shipping costs'].corr(df['Shipping times']), 3))

# --- Segmentation: high-value vs at-risk SKUs ---
# High-value = top-quartile profit; At-risk = bottom-quartile stock cover AND failed/pending inspection
profit_q75 = df['Profit'].quantile(0.75)
df['segment'] = 'Standard'
df.loc[df['Profit'] >= profit_q75, 'segment'] = 'High-value (top 25% profit)'
df.loc[(df['Days of stock cover'] < df['Lead time']) & (df['Inspection results'] != 'Pass'), 'segment'] = 'At-risk (low stock cover + QC concern)'

seg_summary = df.groupby('segment').agg(
    sku_count=('SKU', 'count'),
    total_revenue=('Revenue generated', 'sum'),
    avg_margin=('Profit margin %', 'mean'),
    avg_defect_rate=('Defect rate %', 'mean')
).round(2)
print("\nSEGMENT SUMMARY:\n", seg_summary.to_string())

# --- Supplier scorecard: composite risk score (z-scored defect rate + lead time) ---
supplier_agg = df.groupby('Supplier name').agg(
    sku_count=('SKU', 'count'),
    avg_defect_rate=('Defect rate %', 'mean'),
    avg_lead_time=('Lead time', 'mean'),
    fail_rate_pct=('Inspection results', lambda s: (s == 'Fail').mean() * 100),
    total_revenue=('Revenue generated', 'sum')
).round(2)
supplier_agg['defect_z'] = (supplier_agg['avg_defect_rate'] - supplier_agg['avg_defect_rate'].mean()) / supplier_agg['avg_defect_rate'].std()
supplier_agg['leadtime_z'] = (supplier_agg['avg_lead_time'] - supplier_agg['avg_lead_time'].mean()) / supplier_agg['avg_lead_time'].std()
supplier_agg['risk_score'] = (supplier_agg['defect_z'] + supplier_agg['leadtime_z']).round(2)
supplier_agg = supplier_agg.sort_values('risk_score', ascending=False)
print("\nSUPPLIER RISK SCORECARD:\n", supplier_agg.to_string())

df.to_csv('/home/claude/supply-chain-project/data/analyzed_data.csv', index=False)
supplier_agg.to_csv('/home/claude/supply-chain-project/data/supplier_scorecard.csv')
seg_summary.to_csv('/home/claude/supply-chain-project/data/segment_summary.csv')
print("\nSaved analyzed_data.csv, supplier_scorecard.csv, segment_summary.csv")
