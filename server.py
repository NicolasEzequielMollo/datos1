from flask import Flask, jsonify, request
import pandas as pd
import yfinance as yf

app = Flask(__name__)

@app.get("/yfinance")
def yfinance_last5():
    tickers = request.args.get("tickers",
                               ",".join([
                                   # ÍNDICES
                                   "^GSPC",  # S&P 500
                                   "^DJI",  # Dow Jones
                                   "^IXIC",  # Nasdaq
                                   "^RUT",  # Russell 2000
                                   "^VIX",  # Volatilidad
                                   "000001.SS",  # Shanghai Composite
                                   "^HSI",  # Hang Seng
                                   "^N225",  # Nikkei 225
                                   "^BVSP",  # Bovespa
                                   "^MERV",  # MERVAL

                                   # ACCIONES USA (mega caps)
                                   "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V",
                                   "JNJ", "WMT", "XOM", "PG", "MA", "HD", "UNH", "BAC", "KO", "PFE",

                                   # ACCIONES CHINA
                                   "BABA", "JD", "PDD", "BIDU", "TCEHY", "NIO", "LI", "XPEV",

                                   # PRINCIPALES ETFs
                                   "SPY", "QQQ", "DIA", "IWM", "EEM", "VTI", "ARKK", "XLF", "XLK", "XLE",
                                   "SMH", "SOXX", "HYG", "LQD", "TLT", "SHY", "IEF",

                                   # CRIPTOS (vía Yahoo, pares contra USD)
                                   "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD", "XRP-USD", "DOGE-USD",

                                   # MERVAL (BYMA, .BA)
                                   "GGAL.BA", "YPFD.BA", "PAMP.BA", "TXAR.BA", "CEPU.BA", "BMA.BA",
                                   "TGSU2.BA", "SUPV.BA", "EDN.BA", "MIRG.BA", "LOMA.BA", "CRES.BA",

                                   # BOVESPA (Brasil, .SA)
                                   "PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "ABEV3.SA",

                                   # BONOS DEL TESORO (USA)
                                   "^TNX",  # 10 años yield
                                   "^TYX",  # 30 años yield
                                   "^IRX",  # 13 semanas yield

                                   # COMMODITIES
                                   "GC=F",  # Oro
                                   "SI=F",  # Plata
                                   "CL=F",  # Petróleo WTI
                                   "BZ=F",  # Petróleo Brent
                                   "NG=F",  # Gas Natural
                                   "HG=F",  # Cobre
                                   "ZC=F",  # Maíz
                                   "ZW=F",  # Trigo
                                   "ZS=F",  # Soja
                               ])
                               )

    tickers = [t.strip().upper() for t in tickers.split(",")]
    data = yf.download(tickers, period="7d", interval="1d", progress=False)
    closes = data["Close"].tail(5).reset_index()
    closes["Date"] = closes["Date"].dt.strftime("%Y-%m-%d")

    rows = []
    for _, r in closes.iterrows():
        fecha = r["Date"]
        for sym in tickers:
            val = r.get(sym)
            if pd.notna(val):
                rows.append({"Symbol": sym, "Fecha": fecha, "Close": float(val)})
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

