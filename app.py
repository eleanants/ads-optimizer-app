import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="NotTheSame Ads Optimizer", layout="wide")
st.title("📡 NotTheSame Ads Optimizer — Meta Real-Time Preview v1.4")

# Έλεγχος token
token = st.secrets.get("META_ACCESS_TOKEN", None)
if not token:
    st.error("❌ Δεν βρέθηκε META_ACCESS_TOKEN. Βάλ' το στο Streamlit Secrets panel.")
    st.stop()

st.success("🔐 Token βρέθηκε - σύνδεση με Meta API επιτυχής!")

# Προσομοιωμένοι λογαριασμοί για preview (σε τελική μορφή θα έρχονται από API)
accounts = {
    '1234567890': 'Pharmacy Ads Account',
    '0987654321': 'Sportswear Dynamic',
    '1122334455': 'Beauty Campaigns'
}

selected_account = st.selectbox("🧾 Επέλεξε Ad Account για Ανάλυση", options=list(accounts.keys()), format_func=lambda x: accounts[x])

st.info(f"📊 Αναλύοντας account: {accounts[selected_account]}")

# Mocked campaign performance data
data = [
    {
        "Campaign Name": "Spring Launch",
        "Objective": "Conversions",
        "Spend (€)": round(random.uniform(50, 300), 2),
        "Purchases": random.randint(5, 30),
        "ROAS": round(random.uniform(0.8, 4.5), 2),
        "Status": "Active"
    },
    {
        "Campaign Name": "Retargeting",
        "Objective": "Sales",
        "Spend (€)": round(random.uniform(80, 250), 2),
        "Purchases": random.randint(3, 25),
        "ROAS": round(random.uniform(0.5, 3.5), 2),
        "Status": "Paused"
    },
    {
        "Campaign Name": "Awareness Boost",
        "Objective": "Traffic",
        "Spend (€)": round(random.uniform(100, 400), 2),
        "Purchases": 0,
        "ROAS": 0.0,
        "Status": "Active"
    }
]

df = pd.DataFrame(data)
df['CPA'] = df.apply(lambda x: round(x['Spend (€)'] / x['Purchases'], 2) if x['Purchases'] > 0 else 0, axis=1)

# Προτεινόμενες ενέργειες
def suggest(row):
    if row["ROAS"] < 1.2:
        return "⛔ Χαμηλό ROAS – Επανεξέταση"
    elif row["CPA"] > 20:
        return "⚠️ Υψηλό CPA – Δοκιμή βελτιστοποίησης"
    else:
        return "✅ Καλή Απόδοση – Συνέχισε"

df["Πρόταση"] = df.apply(suggest, axis=1)

st.subheader("📈 Real-Time Απόδοση Καμπανιών")
st.dataframe(df)