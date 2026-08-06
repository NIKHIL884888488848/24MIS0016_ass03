import json
import os
from collections import defaultdict
class PortfolioManager:

    def __init__(self):
        self.records = [
            {
                "Investor ID": "INV001",
                "Stock Symbol": "AAPL",
                "Quantity": 10,
                "Buy Price": 150.0,
                "Current Price": 175.0,
                "Sector": "Technology",
                "Dividend Received": 5.0,
            },
            {
                "Investor ID": "INV001",
                "Stock Symbol": "TSLA",
                "Quantity": 5,
                "Buy Price": 200.0,
                "Current Price": 180.0,
                "Sector": "Automotive",
                "Dividend Received": 0.0,
            },
            {
                "Investor ID": "INV002",
                "Stock Symbol": "MSFT",
                "Quantity": 8,
                "Buy Price": 300.0,
                "Current Price": 350.0,
                "Sector": "Technology",
                "Dividend Received": 12.0,
            },
            {
                "Investor ID": "INV002",
                "Stock Symbol": "JPM",
                "Quantity": 15,
                "Buy Price": 130.0,
                "Current Price": 145.0,
                "Sector": "Finance",
                "Dividend Received": 20.0,
            },
        ]

    def calculate_metrics(self, row):
        """Calculates value, profit/loss, and returns for an individual record."""
        inv_value = row["Quantity"] * row["Buy Price"]
        cur_value = row["Quantity"] * row["Current Price"]
        profit_loss = (cur_value - inv_value) + row["Dividend Received"]
        pct_return = (profit_loss / inv_value) * 100 if inv_value > 0 else 0.0

        return {
            "Investment Value": inv_value,
            "Current Value": cur_value,
            "Profit/Loss": profit_loss,
            "Percentage Return": pct_return,
        }

    def get_extremes(self):
        """Finds both the best and worst performing stock records globally."""
        if not self.records:
            return None, None

        evaluated = [
            (r, self.calculate_metrics(r)["Percentage Return"])
            for r in self.records
        ]
        best = max(evaluated, key=lambda x: x[1])[0]
        worst = min(evaluated, key=lambda x: x[1])[0]
        return best, worst

    def sector_exposure(self):
        """Calculates aggregated monetary exposure across different industry sectors."""
        exposure = defaultdict(float)
        for row in self.records:
            metrics = self.calculate_metrics(row)
            exposure[row["Sector"]] += metrics["Current Value"]
        return dict(exposure)

    def rank_investors(self):
        """Aggregates and ranks overall percentage returns per individual investor."""
        investor_data = defaultdict(
            lambda: {"total_inv": 0.0, "total_profit_loss": 0.0}
        )

        for row in self.records:
            metrics = self.calculate_metrics(row)
            inv_id = row["Investor ID"]
            investor_data[inv_id]["total_inv"] += metrics["Investment Value"]
            investor_data[inv_id]["total_profit_loss"] += metrics["Profit/Loss"]

        rankings = []
        for inv_id, data in investor_data.items():
            overall_return = (
                (data["total_profit_loss"] / data["total_inv"]) * 100
                if data["total_inv"] > 0
                else 0.0
            )
            rankings.append((inv_id, overall_return))

        return sorted(rankings, key=lambda x: x[1], reverse=True)

    def generate_report(self):
        """Assembles all analytical computations into a structured document text string."""
        report = "=== SMART STOCK PORTFOLIO & RISK MANAGEMENT REPORT ===\n\n"

        report += f"{'Investor':<10} {'Symbol':<8} {'Inv Value':<10} {'Cur Value':<10} {'P/L':<10} {'Return %':<10}\n"
        report += "-" * 62 + "\n"

        for row in self.records:
            m = self.calculate_metrics(row)
            report += f"{row['Investor ID']:<10} {row['Stock Symbol']:<8} {m['Investment Value']:<10.2f} {m['Current Value']:<10.2f} {m['Profit/Loss']:<10.2f} {m['Percentage Return']:<10.2f}%\n"

        best, worst = self.get_extremes()
        if best and worst:
            report += f"\nBest Performing Stock: {best['Stock Symbol']} ({best['Investor ID']})\n"
            report += f"Worst Performing Stock: {worst['Stock Symbol']} ({worst['Investor ID']})\n"

        report += "\nSector-Wise Asset Exposure:\n"
        for sector, exposure in self.sector_exposure().items():
            report += f" - {sector}: ${exposure:,.2f}\n"

        report += "\nInvestor Leaderboard Rankings:\n"
        for rank, (inv_id, ret) in enumerate(self.rank_investors(), 1):
            report += f" {rank}. Investor {inv_id} | Total Return: {ret:.2f}%\n"

        return report

    def save_report_to_file(self, filename="portfolio_report.txt"):
        """Saves generated report to disk."""
        report_content = self.generate_report()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"[System] Report successfully written out to: {filename}")

    def read_report_from_file(self, filename="portfolio_report.txt"):
        """Reads and prints report back from disk."""
        if not os.path.exists(filename):
            print(f"[Error] Specified file target '{filename}' does not exist.")
            return
        with open(filename, "r", encoding="utf-8") as f:
            print("\n--- Displaying Saved File Records ---")
            print(f.read())


if __name__ == "__main__":
    manager = PortfolioManager()
    manager.save_report_to_file()
    manager.read_report_from_file()
