# Power BI Dashboard — Setup Guide & DAX Measures

This project doesn't ship a `.pbix` binary (Power BI Desktop isn't available in this
environment to author one directly), but everything needed to build the report in
Power BI Desktop in under 15 minutes is here: a clean data model and ready-to-paste
DAX measures matching the same analysis used in the Excel workbook and HTML dashboard.

---

## 1. Load the data

1. Open Power BI Desktop → **Get Data** → **Text/CSV**
2. Select `powerbi_data_model.csv` (100 rows, 30 columns — the same cleaned/enriched
   dataset used everywhere else in this project)
3. Click **Load** (no transforms needed — it's already clean)

## 2. Create measures

Go to **Modeling → New Measure** and paste each of these one at a time. They
reproduce the KPIs and tables seen in the Excel workbook and the HTML dashboard.

```dax
Total Revenue = SUM('powerbi_data_model'[Revenue generated])

Total Profit = SUM('powerbi_data_model'[Profit])

Avg Profit Margin % = AVERAGE('powerbi_data_model'[Profit margin %])

Avg Defect Rate % = AVERAGE('powerbi_data_model'[Defect rate %])

SKU Count = DISTINCTCOUNT('powerbi_data_model'[SKU])

SKUs At Risk =
CALCULATE(
    [SKU Count],
    FILTER(
        'powerbi_data_model',
        'powerbi_data_model'[Days of stock cover] < 'powerbi_data_model'[Lead time]
            || 'powerbi_data_model'[Inspection results] = "Fail"
    )
)

QC Fail Rate % =
DIVIDE(
    CALCULATE([SKU Count], 'powerbi_data_model'[Inspection results] = "Fail"),
    [SKU Count]
)

Supplier Risk Score =
VAR AvgDefect = [Avg Defect Rate %]
VAR AvgLead = AVERAGE('powerbi_data_model'[Lead time])
VAR DefectZ = DIVIDE(AvgDefect - CALCULATE([Avg Defect Rate %], ALL('powerbi_data_model'[Supplier name])), 1)
VAR LeadZ = DIVIDE(AvgLead - CALCULATE(AVERAGE('powerbi_data_model'[Lead time]), ALL('powerbi_data_model'[Supplier name])), 1)
RETURN DefectZ + LeadZ

Cumulative Profit % =
VAR CurrentProfit = [Total Profit]
VAR TotalProfitAll = CALCULATE([Total Profit], ALL('powerbi_data_model'))
RETURN DIVIDE(CurrentProfit, TotalProfitAll)
```

## 3. Recommended report pages (mirrors the HTML dashboard)

| Page | Visuals |
|---|---|
| **Overview** | KPI cards (Total Revenue, Total Profit, Avg Margin, SKUs At Risk), clustered column chart (Revenue by Product type), line chart (cumulative profit %) |
| **Suppliers** | Scatter chart (Avg Defect Rate % vs Avg Lead Time, bubble size = Revenue), stacked bar (Inspection results by Supplier), table (Supplier Scorecard) |
| **Logistics** | Scatter chart (Shipping costs vs Shipping times by Carrier), bar chart (avg cost by Route) |
| **Stockout Risk** | Table filtered to `Days of stock cover < Lead time`, sorted ascending, conditional formatting (red/amber/green) on the Days of stock cover column |

## 4. Suggested slicers (for the "clickable/filterable" experience)

Add slicers for `Product type`, `Supplier name`, and `Location` at the top of each
page — Power BI cross-filters all visuals on the page automatically when a slicer
value is clicked, which is the native equivalent of the filter chips in the HTML
dashboard.

## 5. Conditional formatting tip for the Risk table

On the `Days of stock cover` column: **Column → Conditional formatting → Background
color → Rules**:
- < 1 → red (`#FF6259`)
- 1–3 → amber (`#F2A93B`)
- > 3 → teal (`#35C9C1`)

This matches the Critical / High / Watch status pills used in the HTML dashboard.
