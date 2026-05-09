import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Korea ADR Arbitrage Tracker", layout="wide")
st.title("Korea ADR Arbitrage Tracker")

if st.button("🔄 Refresh Prices"):
    with st.spinner("Fetching latest prices..."):

        # --- Exchange Rates ---
        krw_rate = yf.Ticker("KRW=X").info.get("currentPrice", 1)
        eur_rate = yf.Ticker("EURUSD=X").info.get("currentPrice", 1)

        # --- Korean Exchange Table ---
        korean_securities = [
            {"name": "Samsung Electronics", "ticker": "005930.KS"},
            {"name": "Samsung Electronics Pref", "ticker": "005935.KS"},
            {"name": "SK Hynix", "ticker": "000660.KS"},
        ]

        kr_rows = []
        for s in korean_securities:
            info = yf.Ticker(s["ticker"]).info
            price = info.get("currentPrice", 0)
            change = info.get("regularMarketChangePercent", 0)
            kr_rows.append({
                "Security": s["name"],
                "Price (KRW)": f"{price:,.0f}",
                "Daily Change %": f"{change:.2f}%"
            })

        st.subheader("Korean Exchange Prices")
        st.dataframe(pd.DataFrame(kr_rows), use_container_width=True)

        # --- ADR Table ---
        adr_securities = [
            {"name": "Samsung Electronics (USD)", "ticker": "SMSN.IL", "currency": "USD", "shares": 25, "kr_ticker": "005930.KS", "kr_price": float(kr_rows[0]["Price (KRW)"].replace(",", ""))},
            {"name": "Samsung Pref (USD)",         "ticker": "SMSD.IL", "currency": "USD", "shares": 25, "kr_ticker": "005935.KS", "kr_price": float(kr_rows[1]["Price (KRW)"].replace(",", ""))},
            {"name": "SK Hynix (EUR)",             "ticker": "HY9H.F",  "currency": "EUR", "shares": 1,  "kr_ticker": "000660.KS", "kr_price": float(kr_rows[2]["Price (KRW)"].replace(",", ""))},
        ]

        adr_rows = []
        for s in adr_securities:
            info = yf.Ticker(s["ticker"]).info
            price = info.get("currentPrice", 0)
            change = info.get("regularMarketChangePercent", 0)

            # Implied Korean price based on ADR
            if s["currency"] == "EUR":
                implied_krw = (price / s["shares"]) * eur_rate * krw_rate
            else:
                implied_krw = (price / s["shares"]) * krw_rate

            premium_pct = ((implied_krw / s["kr_price"]) - 1) * 100 if s["kr_price"] else 0

            adr_rows.append({
                "Security": s["name"],
                "ADR Price": f"{price:.2f}",
                "Daily Change %": f"{change:.2f}%",
                "Implied Korean Price (KRW)": f"{implied_krw:,.0f}",
                "Premium / Discount %": f"{premium_pct:.2f}%"
            })

        st.subheader("ADR Prices")
        st.dataframe(pd.DataFrame(adr_rows), use_container_width=True)

        # --- Exchange Rates Table ---
        st.subheader("Exchange Rates")
        fx_rows = [
            {"Pair": "USD / KRW", "Rate": f"{krw_rate:,.2f}"},
            {"Pair": "EUR / USD", "Rate": f"{eur_rate:.4f}"},
        ]
        st.dataframe(pd.DataFrame(fx_rows), use_container_width=True)
