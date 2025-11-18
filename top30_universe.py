import requests

BINANCE_API = "https://api.binance.com/api/v3"

def get_exchange_info():
    r = requests.get(f"{BINANCE_API}/exchangeInfo")
    r.raise_for_status()
    return r.json()

def get_tickers_24hr():
    r = requests.get(f"{BINANCE_API}/ticker/24hr")
    r.raise_for_status()
    return r.json()

def get_top30_symbols():
    tickers = get_tickers_24hr()

    # Собираем монеты по объёму торгов USDT-пар
    volumes = {}
    for t in tickers:
        symbol = t["symbol"]
        if symbol.endswith("USDT"):
            base = symbol.replace("USDT", "")
            volumes[base] = float(t["quoteVolume"])

    # Сортируем по объёму и берём топ-30
    top30 = sorted(volumes.items(), key=lambda x: x[1], reverse=True)[:30]
    return [coin for coin, _ in top30]

def get_existing_pairs(top30_list):
    info = get_exchange_info()
    symbols = {
        s["symbol"]: (s["baseAsset"], s["quoteAsset"])
        for s in info["symbols"]
        if s["status"] == "TRADING"
    }

    # Оставляем только пары, где оба актива в топ-30
    valid_pairs = []
    for symbol, (base, quote) in symbols.items():
        if base in top30_list and quote in top30_list:
            valid_pairs.append(symbol)

    return valid_pairs


if __name__ == "__main__":
    top30 = get_top30_symbols()
    pairs = get_existing_pairs(top30)

    print("Top 30 coins:", top30)
    print("Pairs inside top30:", pairs)
    print("Total pairs:", len(pairs))
