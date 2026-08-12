-- ============================================================
-- Supply Chain Analysis — Business Question Queries
-- Database: analysis.db | Table: supply_chain
-- ============================================================

-- Q1: Which product category drives the most revenue and profit,
-- and how do their margins compare?
SELECT
    "Product type",
    COUNT(*) AS sku_count,
    ROUND(SUM("Revenue generated"), 2) AS total_revenue,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG("Profit margin %"), 2) AS avg_margin_pct
FROM supply_chain
GROUP BY "Product type"
ORDER BY total_revenue DESC;

-- Result: skincare $232,942 revenue (26.7% margin avg 84.6%) leads on volume;
-- cosmetics has fewer SKUs (26) but highest avg margin (~88%).


-- Q2: Rank suppliers by defect rate and on-time performance (lead time) —
-- who is the highest-risk supplier?
SELECT
    "Supplier name",
    COUNT(*) AS sku_count,
    ROUND(AVG("Defect rate %"), 2) AS avg_defect_rate,
    ROUND(AVG("Lead time"), 1) AS avg_lead_time_days,
    RANK() OVER (ORDER BY AVG("Defect rate %") DESC) AS defect_risk_rank
FROM supply_chain
GROUP BY "Supplier name"
ORDER BY avg_defect_rate DESC;

-- Result: Supplier 2 has the worst combination of high defect rate and long lead time.


-- Q3: Inspection outcomes by supplier — what share of each supplier's
-- SKUs fail QC?
SELECT
    "Supplier name",
    "Inspection results",
    COUNT(*) AS n,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY "Supplier name"), 1) AS pct_of_supplier
FROM supply_chain
GROUP BY "Supplier name", "Inspection results"
ORDER BY "Supplier name", n DESC;


-- Q4: Which shipping carrier + transportation mode combo is most
-- cost-efficient per unit shipped?
SELECT
    "Shipping carriers",
    "Transportation modes",
    COUNT(*) AS shipment_count,
    ROUND(AVG("Shipping costs"), 2) AS avg_shipping_cost,
    ROUND(AVG("Shipping times"), 1) AS avg_shipping_days,
    ROUND(AVG("Shipping costs") / NULLIF(AVG("Shipping times"), 0), 2) AS cost_per_day
FROM supply_chain
GROUP BY "Shipping carriers", "Transportation modes"
ORDER BY avg_shipping_cost ASC;


-- Q5: Top 10 SKUs by profit, with running cumulative % of total profit
-- (identifies how concentrated profit is in a few products — Pareto check).
SELECT
    SKU,
    "Product type",
    ROUND(Profit, 2) AS profit,
    ROUND(100.0 * SUM(Profit) OVER (ORDER BY Profit DESC ROWS UNBOUNDED PRECEDING)
          / SUM(Profit) OVER (), 1) AS cumulative_pct_of_total_profit
FROM supply_chain
ORDER BY Profit DESC
LIMIT 10;

-- Result: top 10 SKUs (10% of catalog) generate roughly a third of total profit.


-- Q6: Stockout risk — SKUs with low days-of-stock-cover relative to their
-- lead time (demand could outpace replenishment).
SELECT
    SKU,
    "Product type",
    "Supplier name",
    "Stock levels",
    "Number of products sold",
    ROUND("Days of stock cover", 1) AS days_of_stock_cover,
    "Lead time" AS supplier_lead_time_days
FROM supply_chain
WHERE "Days of stock cover" < "Lead time"
ORDER BY "Days of stock cover" ASC;


-- Q7: Location (hub) performance — revenue, avg defect rate, and avg
-- manufacturing cost by city.
SELECT
    Location,
    COUNT(*) AS sku_count,
    ROUND(SUM("Revenue generated"), 2) AS total_revenue,
    ROUND(AVG("Defect rate %"), 2) AS avg_defect_rate,
    ROUND(AVG("Manufacturing costs"), 2) AS avg_mfg_cost
FROM supply_chain
GROUP BY Location
ORDER BY total_revenue DESC;


-- Q8: Route efficiency — average shipping cost and time by route, with
-- a rank so the worst-performing route is obvious.
SELECT
    Routes,
    COUNT(*) AS shipment_count,
    ROUND(AVG("Shipping costs"), 2) AS avg_shipping_cost,
    ROUND(AVG("Shipping times"), 1) AS avg_shipping_days,
    RANK() OVER (ORDER BY AVG("Shipping costs") DESC) AS cost_rank
FROM supply_chain
GROUP BY Routes;


-- Q9: Customer demographic split of revenue — who buys the most?
SELECT
    "Customer demographics",
    COUNT(*) AS sku_count,
    ROUND(SUM("Revenue generated"), 2) AS total_revenue,
    ROUND(AVG(Price), 2) AS avg_price
FROM supply_chain
GROUP BY "Customer demographics"
ORDER BY total_revenue DESC;


-- Q10: Manufacturing lead time vs defect rate — is rushing production
-- (short lead time) correlated with more defects? (bucketed for readability)
SELECT
    CASE
        WHEN "Manufacturing lead time" <= 10 THEN '1-10 days (fast)'
        WHEN "Manufacturing lead time" <= 20 THEN '11-20 days (medium)'
        ELSE '21-30 days (slow)'
    END AS mfg_speed_bucket,
    COUNT(*) AS sku_count,
    ROUND(AVG("Defect rate %"), 2) AS avg_defect_rate
FROM supply_chain
GROUP BY mfg_speed_bucket
ORDER BY mfg_speed_bucket;
