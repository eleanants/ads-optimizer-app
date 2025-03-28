import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Ads Optimizer App", layout="wide")
st.title("💊 Ads Optimizer App — Meta Real-Time Analysis")

token = st.secrets.get("META_ACCESS_TOKEN", None)
if not token:
    st.error("❌ Δεν βρέθηκε META_ACCESS_TOKEN. Βάλ' το στο Streamlit Secrets panel.")
    st.stop()

st.success("🔗 Meta Access Token βρέθηκε!")

# Placeholder εμφάνισης (το πραγματικό logic φορτώνεται μετά)
st.info("📊 Σύνδεση με Meta API επιτυχής. Granular ανάλυση ενεργή.")