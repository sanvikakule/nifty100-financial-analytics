import sqlite3
import pandas as pd

DATABASE = "data/db/nifty100.db"

# Higher value is better?
METRICS = {
    "net_profit_margin_pct": True,
    "operating_profit_margin_pct": True,
    "return_on_equity_pct": True,
    "debt_to_equity": False,          # Lower is better
    "interest_coverage": True,
    "asset_turnover": True,
    "free_cash_flow_cr": True,
    "earnings_per_share": True,
    "book_value_per_share": True,
    "dividend_payout_ratio_pct": True,
    "cash_from_operations_cr": True
}


class PeerAnalytics:

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)

    def load_data(self):

        peer = pd.read_sql(
            "SELECT company_id, peer_group_name, is_benchmark FROM peer_groups",
            self.conn
        )

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn
        )

        return ratios.merge(peer, on="company_id", how="inner")

    def calculate_peer_statistics(self):

        df = self.load_data()

        output = []

        for metric, higher_is_better in METRICS.items():

            for (_, year), yearly_df in df.groupby(["peer_group_name", "year"]):

                values = yearly_df[metric]

                if values.empty:
                    continue

                peer_avg = values.mean()

                if higher_is_better:
                    percentile = values.rank(pct=True) * 100
                else:
                    percentile = values.rank(ascending=False, pct=True) * 100

                temp = yearly_df[
                      ["company_id", "peer_group_name", "year"]
                      ].copy()
                temp["value"] = yearly_df[metric].values
                temp["peer_average"] = peer_avg
                temp["percentile"] = percentile.values

                temp["metric"] = metric
                temp["peer_average"] = peer_avg
                temp["percentile"] = percentile.values

                output.append(temp)

        return pd.concat(output, ignore_index=True)

    def export(self, filename="outputs/peer_comparison.csv"):

        result = self.calculate_peer_statistics()

        result.to_csv(filename, index=False)

        print(f"\nSaved -> {filename}")
        print(result.head())

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    pa = PeerAnalytics()

    pa.export()

    pa.close()