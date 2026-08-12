# Business Insights & Recommendations
### Supply Chain Performance & Cost Analysis — Beauty & Personal Care

Dataset: 100 SKUs, 3 product categories, 5 suppliers, 5 Indian distribution hubs (Mumbai, Delhi, Bangalore, Chennai, Kolkata).

---

## 1. Cosmetics is the most profitable category but the least invested in

**Finding:** Skincare leads on revenue ($241,628, 40 SKUs) but Cosmetics has the highest average profit margin (87.3%) with only 26 SKUs — the smallest catalog of the three categories. Haircare sits in between on both metrics (34 SKUs, $174,455 revenue, 85.3% margin).

**Why it matters:** The category generating the best margin per SKU has the fewest SKUs to sell. If Cosmetics converts revenue to profit more efficiently than Skincare, the business is likely leaving profit on the table by not expanding this line.

**Recommendation:** Pilot a Cosmetics SKU expansion (5-10 new products) sourced from the lowest-risk supplier (see #2), and track margin retention as volume scales — margin sometimes compresses with volume, so this should be validated, not assumed.

---

## 2. Supplier 3 is the highest-risk supplier; Supplier 4 has a hidden QC problem

**Finding:** A composite risk score (z-scored defect rate + lead time) ranks **Supplier 3** as riskiest — 20.1-day average lead time (worst of all 5) combined with a 2.47% defect rate. But **Supplier 4** has a different problem: its average defect rate looks mid-pack (2.34%), yet **67% of its SKUs fail formal QC inspection** — the worst pass-through rate of any supplier, more than double the average.

**Why it matters:** These are two different risk profiles requiring different responses. Supplier 3's risk is a *speed* problem (slow replenishment inflates stockout exposure). Supplier 4's risk is a *quality-control* problem that a simple average defect rate metric masks — it would be missed by anyone screening suppliers on defect rate alone.

**Recommendation:** Open a corrective-action conversation with Supplier 4 specifically about inspection failures, not just defect rates. For Supplier 3, negotiate lead-time SLAs or begin qualifying a backup supplier for its SKUs, especially the ones already flagged in the Stockout Risk tab.

---

## 3. Route and carrier choice creates a 69% swing in shipping cost per shipment

**Finding:** The cheapest carrier/mode combination (Carrier A + Sea) averages $3.88 per shipment at 7.0 days transit. The most expensive (Carrier C + Road) averages $6.55 — a 69% premium — while actually being a *shorter*-haul mode (3.7-day average transit). Carrier C + Road is paying a premium for speed it isn't consistently delivering relative to other Road options.

**Why it matters:** With ~530 average total logistics cost per SKU across the dataset, a systematic shift toward cheaper carrier/mode pairings compounds across hundreds of shipments a year.

**Recommendation:** Audit which SKUs are currently routed through Carrier C + Road non-urgently, and reassign price-insensitive shipments to Carrier B + Rail or Carrier A + Sea, which offer better cost-per-day value. Reserve premium carriers for genuinely time-sensitive SKUs only.

---

## 4. Profit is concentrated in a fifth of the catalog

**Finding:** The top 20 SKUs by profit (20% of the 100-SKU catalog) generate approximately 33% of total profit. The single highest earner is SKU2 (Haircare, $9,397 profit).

**Why it matters:** This isn't extreme concentration, but it's meaningful — a stockout or quality failure on one of these 20 SKUs has outsized impact on total profitability compared to a failure among the long tail.

**Recommendation:** Give these 20 SKUs priority in inventory planning (higher safety stock, tighter supplier monitoring) rather than treating all 100 SKUs uniformly. Cross-reference this list against the Stockout Risk tab — several high-profit SKUs already show thin stock cover.

---

## 5. A majority of SKUs carry more stockout exposure than their lead time allows for

**Finding:** 92 of 100 SKUs have "days of stock cover" (current stock ÷ daily sell-through) shorter than their supplier's own lead time — meaning if current sales pace holds, stock would run out *before* a reorder could arrive. 25 of these have less than 1 day of cover.

**Why it matters:** This is the single largest operational risk surfaced in the data. It suggests either reorder points are set too low, safety stock isn't scaled to lead time, or replenishment cycles aren't syncing with actual sell-through.

**Recommendation:** Treat this as the top priority action item. Recalculate reorder points as a function of (daily sell-through × supplier lead time × safety buffer) rather than a fixed stock level, starting with the SKUs in the Stockout Risk tab that show under 1 day of cover.

---

## Summary priority order for action
1. Fix reorder points for the 92 at-risk SKUs (Insight 5) — highest urgency, affects nearly the whole catalog.
2. Address Supplier 4's QC fail rate and Supplier 3's lead times (Insight 2) — root-cause driver of #1 for many SKUs.
3. Re-route non-urgent shipments off Carrier C + Road (Insight 3) — quick cost win, low execution risk.
4. Prioritize the top-20-profit SKUs for stock and supplier attention (Insight 4).
5. Evaluate a Cosmetics catalog expansion once the above are stabilized (Insight 1) — a growth move, not urgent.
