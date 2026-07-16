<div align="center">

# 📈 NIFTY100 Financial Analytics Platform

### Enterprise-Grade Financial Analytics & Business Intelligence Platform

Analyze, validate, and visualize financial performance of **NIFTY100 companies** through an end-to-end **ETL pipeline**, **SQLite database**, **SQL analytics**, and **Power BI dashboards**.

<p>

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![PyTest](https://img.shields.io/badge/PyTest-39_Passed-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

### ⭐ If you like this project, consider giving it a Star!

</div>

---

# 🚀 Overview

The **NIFTY100 Financial Analytics Platform** is a complete financial data engineering project that transforms raw company financial datasets into structured, validated, and analytics-ready information.

The project follows a real-world data engineering workflow:

```
Raw Financial Data
        │
        ▼
 ETL Pipeline
        │
        ▼
 Data Cleaning
        │
        ▼
 Data Validation
        │
        ▼
 SQLite Database
        │
        ▼
 SQL Analytics
        │
        ▼
 Power BI Dashboard
```

---

# ✨ Features

### 📥 ETL Pipeline

- Automated CSV Processing
- Data Cleaning
- Missing Value Handling
- Data Normalization
- Load Audit Generation

---

### 🗄 Database

- SQLite Database
- 12 Normalized Tables
- Optimized Schema
- Database Verification
- SQL-Based Analytics

---

### 📊 Financial Analytics

- Profit & Loss Analysis
- Balance Sheet Analysis
- Cash Flow Analysis
- Financial Ratios
- Market Capitalization
- Historical Stock Prices
- Company Performance

---

### ✅ Data Quality

- Primary Key Validation
- Duplicate Detection
- Year Validation
- Website Validation
- Annual Report Validation
- Market Cap Validation
- Financial Data Validation

---

### 📈 Business Intelligence

- Power BI Dashboard
- KPI Cards
- Trend Analysis
- Company Comparison
- Financial Reports

---

# 📂 Repository Structure

```text
📦 nifty100-financial-analytics
│
├── 📂 data
│   ├── 📂 raw
│   ├── 📂 processed
│   └── 📂 db
│
├── 📂 output
│
├── 📂 sql
│
├── 📂 src
│   ├── 📂 analytics
│   ├── 📂 dashboard
│   ├── 📂 db
│   └── 📂 etl
│
├── 📂 tests
│
├── README.md
└── requirements.txt
```

---

# 🗃 Database Design

| Table | Description |
|--------|-------------|
| companies | Company Information |
| sectors | Sector Classification |
| peer_groups | Peer Benchmarking |
| profitandloss | Profit & Loss Statements |
| balancesheet | Balance Sheet |
| cashflow | Cash Flow Statements |
| financial_ratios | Financial Ratios |
| market_cap | Market Capitalization |
| stock_prices | Historical Stock Prices |
| documents | Annual Reports |
| prosandcons | Company Strengths & Weaknesses |
| analysis | Financial Analysis |

---

# 📊 Dataset Summary

| Dataset | Records |
|---------|-------:|
| Companies | 92 |
| Profit & Loss | 1,276 |
| Balance Sheet | 1,312 |
| Cash Flow | 1,187 |
| Financial Ratios | 1,184 |
| Documents | 1,585 |
| Stock Prices | 5,520 |
| Market Capitalization | 552 |
| Sectors | 92 |
| Peer Groups | 56 |
| Pros & Cons | 16 |

### 📌 Total Records

## **12,892+ Financial Records**

---

# 📈 Project Statistics

```
🏢 Companies Analysed      92

📊 Financial Records       12,892+

🗄 Database Tables         12

🧪 Automated Tests         39 Passed

📑 Annual Reports          1,585

📈 Historical Prices       5,520

⚡ SQL Queries             20+

📊 Power BI Dashboards     In Progress
```

---

# 🧪 Testing

The project uses **PyTest** for automated testing.

Current Status

```
39 Tests Passed
```

Coverage includes:

- ETL Pipeline
- CSV Validation
- Database Verification
- SQLite Connectivity
- Schema Validation
- Data Integrity

---

# 📋 SQL Analytics

Included SQL scripts perform:

- Company Statistics
- Highest Revenue
- Highest Profit
- Market Capitalization
- PE Ratio Analysis
- ROE Analysis
- Sector Distribution
- Historical Price Trends
- Financial Ratio Analysis

---

# 💻 Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Database | SQLite |
| Data Analysis | Pandas, NumPy |
| Validation | Python |
| Visualization | Power BI |
| Testing | PyTest |
| Version Control | Git & GitHub |

---

# ⚡ Quick Start

Clone the repository

```bash
git clone https://github.com/sanvikakule/nifty100-financial-analytics.git
```

Navigate into the project

```bash
cd nifty100-financial-analytics
```

Create a virtual environment

```bash
python -m venv .venv
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the ETL pipeline

```bash
python src/db/create_database.py
```

```bash
python src/db/load_database.py
```

```bash
python src/db/check_database.py
```

```bash
python src/etl/validator.py
```

Run tests

```bash
pytest
```

---

# 🛣 Roadmap

- [x] ETL Pipeline
- [x] SQLite Database
- [x] Data Validation
- [x] SQL Analytics
- [x] Automated Testing
- [ ] Power BI Dashboard
- [ ] Financial KPI Engine
- [ ] Streamlit Dashboard
- [ ] REST API
- [ ] Docker Deployment

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Data Engineering
- ETL Development
- Financial Data Processing
- Database Design
- SQL
- Python
- Data Validation
- Business Intelligence
- Software Testing

---

# 👩‍💻 Author

## Sanvi Kakule

**Final Year B.E. Information Technology**

Interested in:

- Data Engineering
- Data Analytics
- Business Intelligence
- Financial Analytics
- Python Development

GitHub

**https://github.com/sanvikakule**

---

<div align="center">

### ⭐ Thanks for visiting this repository!

If you found this project useful, consider giving it a ⭐ on GitHub.

</div>