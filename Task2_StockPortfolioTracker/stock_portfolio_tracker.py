"""
CodeAlpha Internship — Task 2: Stock Portfolio Tracker
======================================================
• User inputs stock name + quantity.
• Prices are hardcoded in a dictionary.
• Displays a formatted portfolio summary.
• Saves results to portfolio_report.csv and portfolio_report.txt.
Key Concepts: dictionary, input/output, arithmetic, file handling.
"""

import csv
import os
from datetime import datetime

# ─────────────────────────────────────────
#  Hardcoded stock price dictionary (USD)
# ─────────────────────────────────────────
STOCK_PRICES = {
    "AAPL":  180.00,   # Apple
    "TSLA":  250.00,   # Tesla
    "GOOGL": 140.00,   # Alphabet (Google)
    "MSFT":  415.00,   # Microsoft
    "AMZN":  185.00,   # Amazon
    "NFLX":  620.00,   # Netflix
    "META":  500.00,   # Meta
    "NVDA":  875.00,   # NVIDIA
}

# ─────────────────────────────────────────
#  Helper: display available stocks
# ─────────────────────────────────────────
def show_available_stocks():
    print("\n  ┌─────────────────────────────────────┐")
    print("  │       Available Stocks & Prices     │")
    print("  ├──────────┬──────────────────────────┤")
    print("  │  Ticker  │  Price (USD)             │")
    print("  ├──────────┼──────────────────────────┤")
    for ticker, price in STOCK_PRICES.items():
        print(f"  │  {ticker:<8}│  ${price:<23.2f}│")
    print("  └──────────┴──────────────────────────┘\n")

# ─────────────────────────────────────────
#  Helper: get valid ticker from user
# ─────────────────────────────────────────
def get_ticker():
    while True:
        ticker = input("  Enter stock ticker (or 'done' to finish): ").strip().upper()
        if ticker == "DONE":
            return None
        if ticker in STOCK_PRICES:
            return ticker
        print(f"  ⚠  '{ticker}' not found. Choose from: {', '.join(STOCK_PRICES)}")

# ─────────────────────────────────────────
#  Helper: get valid quantity from user
# ─────────────────────────────────────────
def get_quantity(ticker):
    while True:
        try:
            qty = int(input(f"  How many shares of {ticker}? ").strip())
            if qty <= 0:
                print("  ⚠  Quantity must be a positive integer.")
            else:
                return qty
        except ValueError:
            print("  ⚠  Please enter a whole number.")

# ─────────────────────────────────────────
#  Helper: display portfolio summary
# ─────────────────────────────────────────
def display_portfolio(portfolio):
    print("\n  ╔══════════════════════════════════════════════════════╗")
    print("  ║              📊  PORTFOLIO SUMMARY                  ║")
    print("  ╠══════════╦══════════╦══════════════╦════════════════╣")
    print("  ║  Ticker  ║  Shares  ║  Price/Share ║  Total Value   ║")
    print("  ╠══════════╬══════════╬══════════════╬════════════════╣")

    grand_total = 0
    rows = []
    for ticker, qty in portfolio.items():
        price      = STOCK_PRICES[ticker]
        total      = price * qty
        grand_total += total
        rows.append((ticker, qty, price, total))
        print(f"  ║  {ticker:<8}║  {qty:<8}║  ${price:<11.2f}║  ${total:<13.2f}║")

    print("  ╠══════════╩══════════╩══════════════╬════════════════╣")
    print(f"  ║  TOTAL PORTFOLIO VALUE             ║  ${grand_total:<13.2f}║")
    print("  ╚════════════════════════════════════╩════════════════╝\n")
    return rows, grand_total

# ─────────────────────────────────────────
#  Save results to CSV
# ─────────────────────────────────────────
def save_csv(rows, grand_total, filename="portfolio_report.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Shares", "Price per Share (USD)", "Total Value (USD)"])
        for ticker, qty, price, total in rows:
            writer.writerow([ticker, qty, f"{price:.2f}", f"{total:.2f}"])
        writer.writerow([])
        writer.writerow(["", "", "GRAND TOTAL", f"{grand_total:.2f}"])
    print(f"  💾  CSV saved  → {os.path.abspath(filename)}")

# ─────────────────────────────────────────
#  Save results to TXT
# ─────────────────────────────────────────
def save_txt(rows, grand_total, portfolio, filename="portfolio_report.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "w") as f:
        f.write("=" * 55 + "\n")
        f.write("       STOCK PORTFOLIO REPORT\n")
        f.write(f"       Generated: {timestamp}\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"  {'Ticker':<10}{'Shares':<10}{'Price':>12}{'Total':>14}\n")
        f.write("  " + "-" * 48 + "\n")
        for ticker, qty, price, total in rows:
            f.write(f"  {ticker:<10}{qty:<10}${price:>11.2f}  ${total:>11.2f}\n")
        f.write("  " + "-" * 48 + "\n")
        f.write(f"  {'TOTAL PORTFOLIO VALUE':.<38}  ${grand_total:>11.2f}\n\n")
        f.write("=" * 55 + "\n")
    print(f"  📄  TXT saved  → {os.path.abspath(filename)}")

# ─────────────────────────────────────────
#  Main
# ─────────────────────────────────────────
def main():
    print("\n" + "=" * 55)
    print("   💹  STOCK PORTFOLIO TRACKER  —  CodeAlpha Task 2")
    print("=" * 55)

    show_available_stocks()
    print("  Add stocks to your portfolio. Type 'done' when finished.\n")

    portfolio = {}   # { ticker: quantity }

    while True:
        ticker = get_ticker()
        if ticker is None:
            if not portfolio:
                print("  ⚠  Portfolio is empty. Please add at least one stock.\n")
                continue
            break
        qty = get_quantity(ticker)

        # Accumulate (allow adding more of the same stock)
        portfolio[ticker] = portfolio.get(ticker, 0) + qty
        print(f"  ✅  Added {qty} share(s) of {ticker}. "
              f"(Total held: {portfolio[ticker]})\n")

    rows, grand_total = display_portfolio(portfolio)

    # Save to files
    save_csv(rows, grand_total)
    save_txt(rows, grand_total, portfolio)
    print("\n  ✅  Done! Your portfolio report has been saved.\n")


if __name__ == "__main__":
    main()
