"""
Step 4: Visualizations — each chart answers one framing question.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams['font.size'] = 11
OUT = '/home/claude/supply-chain-project/visuals'

df = pd.read_csv('/home/claude/supply-chain-project/data/analyzed_data.csv')
supplier_scorecard = pd.read_csv('/home/claude/supply-chain-project/data/supplier_scorecard.csv')

# --- Chart 1: Revenue & margin by product category ---
cat = df.groupby('Product type').agg(revenue=('Revenue generated', 'sum'), margin=('Profit margin %', 'mean')).reindex(['skincare', 'haircare', 'cosmetics'])
fig, ax1 = plt.subplots(figsize=(8, 5))
bars = ax1.bar(cat.index, cat['revenue'], color=['#2E86AB', '#A23B72', '#F18F01'])
ax1.set_ylabel('Total Revenue ($)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x/1000:.0f}K'))
ax2 = ax1.twinx()
ax2.plot(cat.index, cat['margin'], color='black', marker='o', linewidth=2)
ax2.set_ylabel('Avg Profit Margin (%)')
ax2.set_ylim(80, 95)
plt.title('Skincare leads revenue ($242K) but cosmetics has the best margin (87.3%)', fontsize=12, wrap=True)
plt.tight_layout()
plt.savefig(f'{OUT}/01_revenue_margin_by_category.png', dpi=150)
plt.close()

# --- Chart 2: Supplier risk scorecard ---
supplier_scorecard = supplier_scorecard.sort_values('risk_score', ascending=True)
colors = ['#C0392B' if x > 0.5 else '#27AE60' if x < -0.5 else '#F39C12' for x in supplier_scorecard['risk_score']]
plt.figure(figsize=(8, 5))
plt.barh(supplier_scorecard['Supplier name'], supplier_scorecard['risk_score'], color=colors)
plt.axvline(0, color='gray', linewidth=0.8)
plt.xlabel('Composite Risk Score (defect rate + lead time, z-scored)')
plt.title('Supplier 3 is the highest-risk supplier — long lead times + elevated defects', fontsize=12, wrap=True)
plt.tight_layout()
plt.savefig(f'{OUT}/02_supplier_risk_scorecard.png', dpi=150)
plt.close()

# --- Chart 3: Shipping cost vs time by carrier+mode (efficiency scatter) ---
ship = df.groupby(['Shipping carriers', 'Transportation modes']).agg(
    cost=('Shipping costs', 'mean'), time=('Shipping times', 'mean'), n=('SKU', 'count')).reset_index()
plt.figure(figsize=(8, 5.5))
carriers = ship['Shipping carriers'].unique()
cmap = {'Carrier A': '#2E86AB', 'Carrier B': '#A23B72', 'Carrier C': '#F18F01'}
for c in carriers:
    sub = ship[ship['Shipping carriers'] == c]
    plt.scatter(sub['time'], sub['cost'], s=sub['n']*30, label=c, color=cmap[c], alpha=0.75, edgecolors='white')
for _, r in ship.iterrows():
    plt.annotate(r['Transportation modes'], (r['time'], r['cost']), fontsize=8, xytext=(4, 4), textcoords='offset points')
plt.xlabel('Avg Shipping Time (days)')
plt.ylabel('Avg Shipping Cost ($)')
plt.title('Carrier A + Sea is cheapest and fastest-value; Carrier C + Road is worst', fontsize=12, wrap=True)
plt.legend(title='Carrier')
plt.tight_layout()
plt.savefig(f'{OUT}/03_shipping_cost_vs_time.png', dpi=150)
plt.close()

# --- Chart 4: Profit concentration (Pareto) ---
sorted_profit = df.sort_values('Profit', ascending=False).reset_index(drop=True)
sorted_profit['cum_pct'] = 100 * sorted_profit['Profit'].cumsum() / sorted_profit['Profit'].sum()
sorted_profit['sku_pct'] = 100 * (sorted_profit.index + 1) / len(sorted_profit)
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.bar(range(1, 21), sorted_profit['Profit'][:20], color='#2E86AB')
ax1.set_xlabel('SKUs ranked by profit (top 20 shown)')
ax1.set_ylabel('Profit ($)')
ax2 = ax1.twinx()
ax2.plot(range(1, 21), sorted_profit['cum_pct'][:20], color='#C0392B', marker='o', markersize=4)
ax2.set_ylabel('Cumulative % of Total Profit', color='#C0392B')
ax2.axhline(50, color='gray', linestyle='--', linewidth=0.8)
plt.title('Top 20 SKUs (20% of catalog) generate ~33% of total profit', fontsize=12, wrap=True)
plt.tight_layout()
plt.savefig(f'{OUT}/04_profit_pareto.png', dpi=150)
plt.close()

pct20 = round(sorted_profit['cum_pct'].iloc[19], 1)
print('Top 20 SKUs cumulative % of profit:', pct20)

# --- Chart 5: Inspection outcome mix by supplier (stacked) ---
insp = df.groupby(['Supplier name', 'Inspection results']).size().unstack(fill_value=0)
insp = insp[['Pass', 'Pending', 'Fail']]
insp_pct = insp.div(insp.sum(axis=1), axis=0) * 100
insp_pct = insp_pct.sort_values('Fail', ascending=False)
plt.figure(figsize=(8, 5))
bottom = pd.Series(0, index=insp_pct.index)
colors_insp = {'Pass': '#27AE60', 'Pending': '#F39C12', 'Fail': '#C0392B'}
for status in ['Pass', 'Pending', 'Fail']:
    plt.bar(insp_pct.index, insp_pct[status], bottom=bottom, label=status, color=colors_insp[status])
    bottom += insp_pct[status]
plt.ylabel('% of Supplier\'s SKUs')
plt.title("Supplier 4 fails QC on 67% of SKUs — the worst pass-through rate", fontsize=12, wrap=True)
plt.legend(title='Inspection result', bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f'{OUT}/05_inspection_mix_by_supplier.png', dpi=150)
plt.close()

print("All 5 charts saved to", OUT)
