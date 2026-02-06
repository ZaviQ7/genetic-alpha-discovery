import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def vector_backtest(model, X_test, y_test, ticker_name="Asset"):
    alpha_score = model.predict(X_test)
    
    results = pd.DataFrame(index=X_test.index)
    results['Actual_Return'] = y_test
    results['AI_Score'] = alpha_score
    
    if 'Close_vs_EMA50' in X_test.columns:
        trend_col = X_test['Close_vs_EMA50']
        trend_is_up = trend_col > 1.0
    else:
        print(f"[{ticker_name}] Warning: 'Close_vs_EMA50' not found. Disabling Trend Filter.")
        trend_is_up = pd.Series(True, index=X_test.index)

    ai_says_buy = results['AI_Score'] > 0
    
    results['Position'] = np.where(trend_is_up & ai_says_buy, 1, 0)
    
    results['Strategy_Return'] = results['Position'] * results['Actual_Return']
    
    results['BuyHold_Cum'] = (1 + results['Actual_Return']).cumprod()
    results['Strategy_Cum'] = (1 + results['Strategy_Return']).cumprod()
    
    sharpe = results['Strategy_Return'].mean() / results['Strategy_Return'].std() * np.sqrt(365)
    total_return = (results['Strategy_Cum'].iloc[-1] - 1) * 100
    buy_hold_return = (results['BuyHold_Cum'].iloc[-1] - 1) * 100
    
    print(f"\n--- Backtest Results ({ticker_name}) ---")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Buy & Hold Return: {buy_hold_return:.2f}%")
    print(f"AI Strategy Return: {total_return:.2f}%")
    
    plt.figure(figsize=(12, 6))
    plt.plot(results['BuyHold_Cum'], label=f'{ticker_name} Buy & Hold', alpha=0.5)
    
    line_color = 'orange' if 'BTC' in ticker_name else 'blue'
    plt.plot(results['Strategy_Cum'], label='AI + Trend Filter', color=line_color, linewidth=2)
    
    plt.title(f"{ticker_name} Alpha Strategy (Sharpe: {sharpe:.2f})")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    img_name = f"{ticker_name.split('-')[0].lower()}_results.png"
    plt.savefig(img_name)
    print(f"Chart saved as {img_name}")
    
    plt.close()
    
    return {
        'ticker': ticker_name,
        'sharpe': sharpe,
        'return': total_return
    }