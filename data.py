import yfinance as yf
import numpy as np

def normalize_price(df, min_price=20, max_price=100):
    # Kopírujeme dataframe aby se neměnil originál
    df = df.copy()
    
    # Normalizujeme ceny do rozsahu min_price-max_price
    min_val = df['Close'].min()
    max_val = df['Close'].max()
    df['Close'] = min_price + (df['Close'] - min_val) * (max_price - min_price) / (max_val - min_val)
    
    # Přidáme malou volatilitu
    df['Close'] = df['Close'] * np.random.uniform(0.95, 1.05, len(df))
    
    # Zajistíme minimální cenu
    df['Close'] = df['Close'].clip(lower=min_price, upper=max_price)
    
    return df

try:
    # Načtení a normalizace dat
    Bitcoin = yf.download("BTC-USD", start="2020-01-01", end="2025-01-01", auto_adjust=True)
    Bitcoin.reset_index(inplace=True)
    Bitcoin = normalize_price(Bitcoin)

    Ethereum = yf.download("ETH-USD", start="2020-01-01", end="2025-01-01", auto_adjust=True)
    Ethereum.reset_index(inplace=True)
    Ethereum = normalize_price(Ethereum)

    Dogecoin = yf.download("DOGE-USD", start="2020-01-01", end="2025-01-01", auto_adjust=True)
    Dogecoin.reset_index(inplace=True)
    Dogecoin = normalize_price(Dogecoin)

    Solana = yf.download("SOL-USD", start="2020-01-01", end="2025-01-01", auto_adjust=True)
    Solana.reset_index(inplace=True)
    Solana = normalize_price(Solana)

    Cardano = yf.download("ADA-USD", start="2020-01-01", end="2025-01-01", auto_adjust=True)
    Cardano.reset_index(inplace=True)
    Cardano = normalize_price(Cardano)

    # Slovník pro výběr náhodné kryptoměny
    stocks = {
        "Bitcoin": Bitcoin,
        "Ethereum": Ethereum,
        "Dogecoin": Dogecoin,
        "Solana": Solana,
        "Cardano": Cardano
    }
except Exception as e:
    print(f"Chyba při načítání dat: {e}")
    # Vytvoříme záložní data pokud načítání selže
    from datetime import datetime, timedelta
    import pandas as pd
    
    # Vytvoříme základní testovací data
    dates = [datetime(2020, 1, 1) + timedelta(days=x) for x in range(1000)]
    base_price = 50
    prices = [base_price]
    
    # Generujeme náhodné ceny mezi 20 a 100
    for _ in range(999):
        change = np.random.uniform(-5, 5)
        new_price = max(20, min(100, prices[-1] + change))
        prices.append(new_price)
    
    # Vytvoříme DataFrame s testovacími daty
    test_data = pd.DataFrame({
        'Date': dates,
        'Close': prices
    })
    
    # Použijeme stejná testovací data pro všechny kryptoměny
    stocks = {
        "Bitcoin": test_data.copy(),
        "Ethereum": test_data.copy(),
        "Dogecoin": test_data.copy(),
        "Solana": test_data.copy(),
        "Cardano": test_data.copy()
    }
