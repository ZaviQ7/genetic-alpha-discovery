import matplotlib
matplotlib.use('Agg')

from src.market_data import download_data, prepare_features
from src.genetic_engine import run_genetic_search
from src.backtest import vector_backtest
import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    assets = ["BTC-USD", "ETH-USD"]
    summary_stats = []

    print(f"\n{'='*40}")
    print(f"🧬 GENETIC ALPHA DISCOVERY ENGINE")
    print(f"{'='*40}")

    for ticker in assets:
        print(f"\n📍 Analyzing {ticker}...")

        raw_df = download_data(ticker, start="2019-01-01", end="2026-02-01")
        X, y = prepare_features(raw_df)
        
        model, X_test, y_test = run_genetic_search(X, y)
        
        stats = vector_backtest(model, X_test, y_test, ticker)
        summary_stats.append(stats)

    print(f"\n{'='*40}")
    print("🏆 FINAL PORTFOLIO RESULTS")
    print(f"{'='*40}")
    print(f"{'ASSET':<10} | {'SHARPE':<8} | {'AI RETURN':<10}")
    print("-" * 34)
    for s in summary_stats:
        print(f"{s['ticker']:<10} | {s['sharpe']:<8.2f} | {s['return']:<10.2f}%")
    print(f"{'='*40}")