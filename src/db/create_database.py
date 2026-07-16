import sqlite3
from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parents[2]

DB_FOLDER = ROOT / "data" / "db"
DB_FOLDER.mkdir(parents=True, exist_ok=True)

DATABASE = DB_FOLDER / "nifty100.db"

SCHEMA = ROOT / "sql" / "schema.sql"

# ==========================================================
# CREATE DATABASE
# ==========================================================

def create_database():

    print("\n========== SQLite Database Creation ==========\n")

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    print("Connected to SQLite.")

    with open(SCHEMA, "r", encoding="utf-8") as file:

        sql_script = file.read()

    cursor.executescript(sql_script)

    conn.commit()

    conn.close()

    print("Database Created Successfully.")
    print(f"\nDatabase Location:\n{DATABASE}")

# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    create_database()