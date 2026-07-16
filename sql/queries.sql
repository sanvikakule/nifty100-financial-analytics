SELECT COUNT(*) AS total_companies
FROM companies;

SELECT
company_id,
year,
sales
FROM profitandloss
ORDER BY sales DESC
LIMIT 10;

SELECT
company_id,
year,
net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

SELECT
company_id,
year,
return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;

SELECT
company_name,
book_value
FROM companies
ORDER BY book_value DESC;

SELECT
company_id,
year,
total_debt_cr
FROM financial_ratios
ORDER BY total_debt_cr DESC
LIMIT 10;

SELECT
AVG(sales) AS average_sales
FROM profitandloss;

SELECT
AVG(net_profit) AS average_profit
FROM profitandloss;

SELECT
company_id,
SUM(net_cash_flow) AS total_cash_flow
FROM cashflow
GROUP BY company_id
ORDER BY total_cash_flow DESC;

SELECT
company_id,
year,
dividend_payout
FROM profitandloss
ORDER BY dividend_payout DESC
LIMIT 10;