import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Korea ADR Arbitrage Tracker", layout="wide")
st.title("Korea ADR Arbitrage Tracker")

if st.button("🔄 Refresh Prices"):
    with st.spinner("Fetching latest prices..."):

        # --- Exchange Rates ---
        krw_rate = yf.Ticker("KRW=X").history(period="5d")["Close"].iloc[-1]
        eur_rate = yf.Ticker("EURUSD=X").history(period="5d")["Close"].iloc[-1]

        # --- Helper to get price and % change ---
        def get_price_and_change(ticker):
            info = yf.Ticker(ticker).info
            price = info.get("currentPrice") or info.get("regularMarketPrice", 0)
            change = info.get("regularMarketChangePercent", 0)
            return price, change

        # --- Korean Exchange Prices ---
        sec_kr,   sec_kr_chg   = get_price_and_change("005930.KS")
        pref_kr,  pref_kr_chg  = get_price_and_change("005935.KS")
        hynix_kr, hynix_kr_chg = get_price_and_change("000660.KS")

        # --- ADR Prices ---
        sec_adr,   sec_adr_chg   = get_price_and_change("SMSN.IL")
        pref_adr,  pref_adr_chg  = get_price_and_change("SMSD.IL")
        hynix_adr, hynix_adr_chg = get_price_and_change("HY9H.F")

        # --- Implied KRW prices from ADRs ---
        sec_implied   = (sec_adr / 25) * krw_rate
        pref_implied  = (pref_adr / 25) * krw_rate
        hynix_implied = (hynix_adr / 1) * eur_rate * krw_rate

        # --- Premium / Discount % ---
        sec_prem   = ((sec_implied / sec_kr) - 1) * 100    if sec_kr   else 0
        pref_prem  = ((pref_implied / pref_kr) - 1) * 100  if pref_kr  else 0
        hynix_prem = ((hynix_implied / hynix_kr) - 1) * 100 if hynix_kr else 0

        # TABLE 1: Korean Exchange Prices
        st.subheader("Korean Exchange Prices")
        kr_df = pd.DataFrame([
            {"Security": "Samsung Electronics",      "Price (KRW)": f"{sec_kr:,.0f}",   "Daily Change %": f"{sec_kr_chg:.2f}%",   "ADR Implied (KRW)": f"{sec_implied:,.0f}",   "Premium / Discount %": f"{sec_prem:.2f}%"},
            {"Security": "Samsung Electronics Pref", "Price (KRW)": f"{pref_kr:,.0f}",  "Daily Change %": f"{pref_kr_chg:.2f}%",  "ADR Implied (KRW)": f"{pref_implied:,.0f}",  "Premium / Discount %": f"{pref_prem:.2f}%"},
            {"Security": "SK Hynix",                 "Price (KRW)": f"{hynix_kr:,.0f}", "Daily Change %": f"{hynix_kr_chg:.2f}%", "ADR Implied (KRW)": f"{hynix_implied:,.0f}", "Premium / Discount %": f"{hynix_prem:.2f}%"},
        ])
        st.dataframe(kr_df, hide_index=True, use_container_width=True)

        # TABLE 2: ADR Prices
        st.subheader("ADR Prices")
        adr_df = pd.DataFrame([
            {"Security": "Samsung Electronics (USD)", "ADR Price": f"{sec_adr:,.2f}",   "Daily Change %": f"{sec_adr_chg:.2f}%"},
            {"Security": "Samsung Pref (USD)",        "ADR Price": f"{pref_adr:,.2f}",  "Daily Change %": f"{pref_adr_chg:.2f}%"},
            {"Security": "SK Hynix (EUR)",            "ADR Price": f"{hynix_adr:,.2f}", "Daily Change %": f"{hynix_adr_chg:.2f}%"},
        ])
        st.dataframe(adr_df, hide_index=True, use_container_width=True)

        # TABLE 3: Exchange Rates
        st.subheader("Exchange Rates")
        fx_df = pd.DataFrame([
            {"Pair": "USD / KRW", "Rate": f"{krw_rate:,.2f}"},
            {"Pair": "EUR / USD", "Rate": f"{eur_rate:.4f}"},
        ])
        st.dataframe(fx_df, hide_index=True, use_container_width=True)
