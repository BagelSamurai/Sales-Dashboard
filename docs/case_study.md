# Case Study: Optimizing Supply Chain & Retention for a UK Retailer

**Role:** Data Analyst (Solo Project)
**Tools:** Python, Pandas, Streamlit, Plotly
**Impact:** Identified 20% of customers driving 77% of revenue, pinpointed seasonal inventory risks.

## 💼 Business Problem
A UK-based online retailer faced two core challenges:
1.  **Inventory Management:** They struggled to predict seasonal demand, leading to potential stockouts during peak months.
2.  **Customer Retention:** They treated all customers equally, missing opportunities to retain high-value "Whales."

## 📊 Solution & Approach
I built an interactive dashboard to visualize 1M+ transactions from 2009-2011.
* **Data Pipeline:** Engineered a robust ETL pipeline to clean messy Excel data, handling cancellations and missing values.
* **Seasonality Analysis:** Aggregated sales by month, day, and hour to find operational peaks.
* **RFM Segmentation:** Applied K-Means logic (Recency, Frequency, Monetary) to categorize 5,900+ customers into actionable segments.

## 💡 Key Insights
1.  **The "November Effect":** Sales triple in November compared to the yearly average.
    * *Recommendation:* Inventory orders must be placed by September; warehouse staffing must increase by 40% in October.
2.  **The "Thursday Rush":** Thursday is surprisingly the highest volume day, with a peak at 12:00 PM (Lunch Break).
    * *Recommendation:* Schedule marketing emails for Thursday at 11:30 AM to capture peak intent.
3.  **The "Pareto" Reality:** The top 20% of customers generate 77% of total revenue.
    * *Recommendation:* Shift marketing budget from "Hibernating" users to a VIP loyalty program for the top 800 "Champions."

## 🛠️ Tech Stack
* **Python/Pandas:** For cleaning 500k+ rows of transaction data.
* **Streamlit:** For deploying the analysis as a self-service tool for stakeholders.
* **Plotly:** For interactive time-series and distribution charts.

## 🔮 Next Steps
* **Forecasting:** Implement a Prophet model to predict next month's sales with 95% confidence intervals.
* **Basket Analysis:** Use Association Rules (Apriori) to find which products are frequently bought together.