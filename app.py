
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="NotTheSame Ads Optimizer — Meta Real-Time v1.5", layout="wide")

# ✅ Title
st.markdown("## 📡 NotTheSame Ads Optimizer — Meta Real-Time v1.5")

# ✅ Έλεγχος META_ACCESS_TOKEN από τα secrets
access_token = st.secrets.get("META_ACCESS_TOKEN", None)
if not access_token:
    st.error("❌ Δεν υπάρχει access token. Πρόσθεσέ το στο Secrets του Streamlit.")
    st.stop()
else:
    st.success("🔓 Token βρέθηκε - σύνδεση με Meta API επιτυχής!")

# ✅ Παράδειγμα accounts για επιλογή
accounts_data = {
    "Pharmacy Ads Account": "123456",
    "Account 789012": "789012",
    "Fashion Ads": "345678"
}

# ✅ Επιλογή λογαριασμού
account_name = st.selectbox("📑 Επέλεξε Ad Account για Ανάλυση", list(accounts_data.keys()))
account_id = accounts_data[account_name]
st.info(f"📊 Αναλύοντας account: {account_name}")

# ✅ Προσομοίωση δεδομένων
df = pd.DataFrame([
    {"Campaign Name": "Spring Launch", "Objective": "Conversions", "Spend (€)": 139.53, "Purchases": 15, "ROAS": 4.49, "Status": "Active"},
    {"Campaign Name": "Retargeting", "Objective": "Sales", "Spend (€)": 143.63, "Purchases": 7, "ROAS": 2.58, "Status": "Paused"},
    {"Campaign Name": "Awareness Boost", "Objective": "Traffic", "Spend (€)": 217.22, "Purchases": 0, "ROAS": 0.0, "Status": "Active"}
])

# ✅ Υπολογισμός CPA
df["CPA"] = df.apply(lambda row: round(row["Spend (€)"] / row["Purchases"], 2) if row["Purchases"] > 0 else 0, axis=1)

# ✅ Προτάσεις
def generate_recommendation(row):
    if row["ROAS"] == 0:
        return "🔴 Χαμηλό ROAS – Επανεξέταση"
    elif row["CPA"] > 15:
        return "⚠️ Υψηλό CPA – Δοκιμή βελτιστοποίησης"
    else:
        return "✅ Καλή Απόδοση – Συνέχισε"

df["Πρόταση"] = df.apply(generate_recommendation, axis=1)

# ✅ Εμφάνιση
st.markdown("### 📈 Real-Time Απόδοση Καμπανιών")
st.dataframe(df, use_container_width=True)
