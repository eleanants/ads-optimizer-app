
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NotTheSame Ads Optimizer — Meta Real-Time v1.5", layout="wide")

st.title("📡 NotTheSame Ads Optimizer — Meta Real-Time v1.5")

# ✅ Token από τα secrets
access_token = st.secrets.get("META_ACCESS_TOKEN", None)
if not access_token:
    st.error("❌ Δεν υπάρχει access token. Πρόσθεσέ το στο Secrets του Streamlit.")
    st.stop()

# ✅ Ανάκτηση διαθέσιμων ad accounts
st.markdown("### 🔗 Σύνδεση με Meta API — Ανάκτηση Ad Accounts...")
accounts_url = f"https://graph.facebook.com/v18.0/me/adaccounts?access_token={access_token}"
response = requests.get(accounts_url)

if response.status_code != 200:
    st.error("❌ Αποτυχία σύνδεσης με Meta API. Έλεγξε το token.")
    st.stop()

accounts_data = response.json().get("data", [])

# ✅ Δημιουργία επιλογών dropdown
account_options = {
    f"{acc.get('name', 'Χωρίς Όνομα')} ({acc.get('id')})": acc.get("id")
    for acc in accounts_data if "id" in acc
}

if not account_options:
    st.warning("⚠️ Δεν βρέθηκαν ad accounts στο token.")
    st.stop()

selected_label = st.selectbox("📑 Επίλεξε Ad Account", list(account_options.keys()))
selected_account_id = account_options[selected_label]

st.success(f"📊 Επιλέχθηκε account: {selected_label}")

# Εδώ θα μπουν τα calls για campaigns / insights ανά selected_account_id

st.markdown("🚧 Η ανάλυση καμπανιών θα ενεργοποιηθεί μόλις ολοκληρωθεί το επόμενο στάδιο.")
