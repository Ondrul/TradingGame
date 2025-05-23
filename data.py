import yfinance as yf

Tesla = yf.download("TSLA", start="2021-04-14", end="2025-01-01")
Tesla.reset_index(inplace=True)

Nvidia = yf.download("NVDA", start="2021-04-14", end="2025-01-01")
Nvidia.reset_index(inplace=True)

Coinbase = yf.download("COIN", start="2021-04-14", end="2025-01-01")
Coinbase.reset_index(inplace=True)

Marathon = yf.download("MARA", start="2021-04-14", end="2025-01-01")
Marathon.reset_index(inplace=True)

Rivian = yf.download("RIVN", start="2021-04-14", end="2025-01-01")
Rivian.reset_index(inplace=True)

Lucid = yf.download("LCID", start="2021-04-14", end="2025-01-01")
Lucid.reset_index(inplace=True)

Gamestop = yf.download("GME", start="2021-04-14", end="2025-01-01")
Gamestop.reset_index(inplace=True)

Palantir = yf.download("PLTR", start="2021-04-14", end="2025-01-01")
Palantir.reset_index(inplace=True)

BeyondMeat = yf.download("BYND", start="2021-04-14", end="2025-01-01")
BeyondMeat.reset_index(inplace=True)

VirginGalactic = yf.download("SPCE", start="2021-04-14", end="2025-01-01")
VirginGalactic.reset_index(inplace=True)

stocks = {
    "Tesla": Tesla,
    "Nvidia": Nvidia,
    "Coinbase": Coinbase,
    "Marathon": Marathon,
    "Rivian": Rivian,
    "Lucid": Lucid,
    "Gamestop": Gamestop,
    "Palantir": Palantir,
    "BeyondMeat": BeyondMeat,
    "VirginGalactic": VirginGalactic
}
print(Gamestop)
