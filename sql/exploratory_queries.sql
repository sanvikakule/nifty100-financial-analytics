-- =====================================================
-- NIFTY100 Financial Analytics
-- Exploratory SQL Queries
-- =====================================================

--------------------------------------------------------
-- 1. Total Companies
--------------------------------------------------------

SELECT COUNT(*) AS total_companies
FROM companies;

--------------------------------------------------------
-- 2. Total Profit & Loss Records
--------------------------------------------------------

SELECT COUNT(*) AS total_profit_loss_records
FROM profitandloss;

--------------------------------------------------------
-- 3. Total Balance Sheet Records
--------------------------------------------------------

SELECT COUNT(*) AS total_balance_sheet_records
FROM balancesheet;

--------------------------------------------------------
-- 4. Top 10 Companies by Market Capitalization
--------------------------------------------------------

SELECT
    company_id,
    market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

--------------------------------------------------------
-- 5. Highest ROE
--------------------------------------------------------

SELECT
    company_id,
    roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

--------------------------------------------------------
-- 6. Highest Book Value
--------------------------------------------------------

SELECT
    company_id,
    book_value
FROM companies
ORDER BY book_value DESC
LIMIT 10;

--------------------------------------------------------
-- 7. Highest Sales
--------------------------------------------------------

SELECT
    company_id,
    year,
    sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

--------------------------------------------------------
-- 8. Highest Net Profit
--------------------------------------------------------

SELECT
    company_id,
    year,
    net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

--------------------------------------------------------
-- 9. Highest EPS
--------------------------------------------------------

SELECT
    company_id,
    year,
    earnings_per_share
FROM financial_ratios
ORDER BY earnings_per_share DESC
LIMIT 10;

--------------------------------------------------------
-- 10. Highest PE Ratio
--------------------------------------------------------

SELECT
    company_id,
    pe_ratio
FROM market_cap
ORDER BY pe_ratio DESC
LIMIT 10;

--------------------------------------------------------
-- 11. Highest Dividend Yield
--------------------------------------------------------

SELECT
    company_id,
    dividend_yield_pct
FROM market_cap
ORDER BY dividend_yield_pct DESC
LIMIT 10;

--------------------------------------------------------
-- 12. Companies by Sector
--------------------------------------------------------

SELECT
    broad_sector,
    COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC;

--------------------------------------------------------
-- 13. Companies by Market Cap Category
--------------------------------------------------------

SELECT
    market_cap_category,
    COUNT(*) AS companies
FROM sectors
GROUP BY market_cap_category;

--------------------------------------------------------
-- 14. Average PE Ratio
--------------------------------------------------------

SELECT
    AVG(pe_ratio) AS average_pe_ratio
FROM market_cap;

--------------------------------------------------------
-- 15. Average PB Ratio
--------------------------------------------------------

SELECT
    AVG(pb_ratio) AS average_pb_ratio
FROM market_cap;

--------------------------------------------------------
-- 16. Average ROE
--------------------------------------------------------

SELECT
    AVG(roe_percentage) AS average_roe
FROM companies;

--------------------------------------------------------
-- 17. Average ROCE
--------------------------------------------------------

SELECT
    AVG(roce_percentage) AS average_roce
FROM companies;

--------------------------------------------------------
-- 18. Total Stock Price Records
--------------------------------------------------------

SELECT COUNT(*)
FROM stock_prices;

--------------------------------------------------------
-- 19. Year-wise Profit Records
--------------------------------------------------------

SELECT
    year,
    COUNT(*) AS records
FROM profitandloss
GROUP BY year
ORDER BY year;

--------------------------------------------------------
-- 20. Database Summary
--------------------------------------------------------

SELECT
    'Companies' AS Table_Name,
    COUNT(*) AS Rows
FROM companies

UNION ALL

SELECT 'Profit & Loss', COUNT(*) FROM profitandloss

UNION ALL

SELECT 'Balance Sheet', COUNT(*) FROM balancesheet

UNION ALL

SELECT 'Cash Flow', COUNT(*) FROM cashflow

UNION ALL

SELECT 'Financial Ratios', COUNT(*) FROM financial_ratios

UNION ALL

SELECT 'Documents', COUNT(*) FROM documents

UNION ALL

SELECT 'Stock Prices', COUNT(*) FROM stock_prices

UNION ALL

SELECT 'Market Cap', COUNT(*) FROM market_cap

UNION ALL

SELECT 'Sectors', COUNT(*) FROM sectors

UNION ALL

SELECT 'Peer Groups', COUNT(*) FROM peer_groups

UNION ALL

SELECT 'Pros & Cons', COUNT(*) FROM prosandcons;