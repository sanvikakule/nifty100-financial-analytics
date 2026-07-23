import sqlite3
import pandas as pd

DATABASE = "data/db/nifty100.db"


# =====================================================
# Database Connection
# =====================================================

def get_connection():
    return sqlite3.connect(DATABASE)


# =====================================================
# Dashboard KPIs
# =====================================================

def get_company_count():
    conn = get_connection()

    query = """
    SELECT COUNT(DISTINCT company_id) AS total
    FROM financial_ratios
    """

    total = pd.read_sql(query, conn).iloc[0]["total"]

    conn.close()

    return int(total)


def get_peer_group_count():
    conn = get_connection()

    query = """
    SELECT COUNT(DISTINCT peer_group_name) AS total
    FROM peer_groups
    """

    total = pd.read_sql(query, conn).iloc[0]["total"]

    conn.close()

    return int(total)


def get_latest_year():
    conn = get_connection()

    query = """
    SELECT MAX(year) AS latest
    FROM financial_ratios
    """

    latest = pd.read_sql(query, conn).iloc[0]["latest"]

    conn.close()

    return int(latest)


def get_metric_count():
    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM financial_ratios LIMIT 1",
        conn
    )

    conn.close()

    # Exclude id, company_id and year
    return len(df.columns) - 3


# =====================================================
# Company List
# =====================================================

def get_companies():
    conn = get_connection()

    query = """
    SELECT DISTINCT company_id
    FROM financial_ratios
    ORDER BY company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df["company_id"].tolist()


# =====================================================
# Company Financial Ratios
# =====================================================

def get_company_ratios(company):
    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return df


def get_company_metrics(company):
    conn = get_connection()

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    if df.empty:
        return None

    return df.iloc[0]


# =====================================================
# Peer Group
# =====================================================

def get_peer_group(company):
    conn = get_connection()

    query = """
    SELECT peer_group_name
    FROM peer_groups
    WHERE company_id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    if df.empty:
        return "Not Available"

    return df.iloc[0]["peer_group_name"]


# =====================================================
# Peer Comparison
# =====================================================

def get_peer_comparison(company):
    conn = get_connection()

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name = (
        SELECT peer_group_name
        FROM peer_groups
        WHERE company_id = ?
    )
    """

    peers = pd.read_sql(
        query,
        conn,
        params=[company]
    )

    conn.close()

    return peers


# =====================================================
# Top Companies by ROE
# =====================================================

def get_top_roe(limit=10):
    conn = get_connection()

    query = f"""
    SELECT
        company_id,
        return_on_equity_pct
    FROM financial_ratios
    WHERE year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    ORDER BY return_on_equity_pct DESC
    LIMIT {limit}
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# =====================================================
# Top Profit Margin
# =====================================================

def get_top_margin(limit=10):
    conn = get_connection()

    query = f"""
    SELECT
        company_id,
        net_profit_margin_pct
    FROM financial_ratios
    WHERE year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    ORDER BY net_profit_margin_pct DESC
    LIMIT {limit}
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# =====================================================
# Sector Distribution
# =====================================================

def get_sector_distribution():
    conn = get_connection()

    query = """
    SELECT
        peer_group_name,
        COUNT(*) AS companies
    FROM peer_groups
    GROUP BY peer_group_name
    ORDER BY companies DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def get_peer_analysis(company):
    """
    Returns the peer comparison data for a selected company.
    """

    conn = get_connection()

    query = """
    SELECT *
    FROM peer_comparison
    WHERE company_id = ?
    ORDER BY metric
    """

    try:
        df = pd.read_sql(query, conn, params=[company])
    except Exception:
        conn.close()
        return pd.DataFrame()

    conn.close()

    return df

# =====================================================
# Peer Comparison
# =====================================================

def get_peer_comparison(company):
    """
    Returns peer comparison data from peer_comparison.csv
    """

    try:
        df = pd.read_csv("outputs/peer_comparison.csv")
    except FileNotFoundError:
        return pd.DataFrame()

    return df[df["company_id"] == company]


def get_company_peer_group(company):
    conn = get_connection()

    query = """
    SELECT peer_group_name
    FROM peer_groups
    WHERE company_id = ?
    """

    df = pd.read_sql(query, conn, params=[company])

    conn.close()

    if df.empty:
        return ""

    return df.iloc[0]["peer_group_name"]