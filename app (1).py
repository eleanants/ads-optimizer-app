import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NotTheSame Ads Optimizer — Real-Time", layout="wide")
st.title("📡 NotTheSame Ads Optimizer — Meta Real-Time v1.5")

# Απόκτηση token από secrets
access_token = st.secrets.get("META_ACCESS_TOKEN")
if not access_token:
    st.error("❌ Δεν υπάρχει access token. Πρόσθεσέ το στο Secrets του Streamlit.")
    st.stop()

# 1. Ανάκτηση διαθέσιμων ad accounts
st.header("🔗 Σύνδεση με Meta")
accounts_url = f"https://graph.facebook.com/v18.0/me/adaccounts?access_token={access_token}"
accounts_res = requests.get(accounts_url)

if accounts_res.status_code != 200:
    st.error("⚠️ Σφάλμα κατά την ανάκτηση ad accounts.")
    st.stop()

accounts_data = accounts_res.json().get("data", [])
account_options = {acc["name"]: acc["id"] for acc in accounts_data}

if not account_options:
    st.warning("Δεν βρέθηκαν διαθέσιμοι λογαριασμοί.")
    st.stop()

selected_account_name = st.selectbox("🧾 Επίλεξε Ad Account", list(account_options.keys()))
selected_account_id = account_options[selected_account_name]

# 2. Ανάκτηση campaign insights
st.subheader(f"📊 Καμπάνιες για: {selected_account_name}")

params = {
    "fields": "name,objective,status,spend,actions,website_purchase_roas",
    "date_preset": "last_7d",
    "access_token": access_token
}
insights_url = f"https://graph.facebook.com/v18.0/act_{selected_account_id}/campaigns"
campaigns_res = requests.get(insights_url, params=params)

if campaigns_res.status_code != 200:
    st.error("❌ Αποτυχία λήψης campaign δεδομένων.")
    st.stop()

campaigns_data = campaigns_res.json().get("data", [])
campaign_list = []

# 3. Επεξεργασία καμπανιών
for camp in campaigns_data:
    name = camp.get("name", "Unnamed")
    objective = camp.get("objective", "-")
    status = camp.get("status", "-")
    spend = float(camp.get("spend", 0))
    roas = 0.0
    purchases = 0

    actions = camp.get("actions", [])
    for action in actions:
        if action["action_type"] == "offsite_conversion.purchase":
            purchases = int(float(action["value"]))
        if action["action_type"] == "omni_purchase":
            purchases = int(float(action["value"]))

    roas_data = camp.get("website_purchase_roas", [])
    if isinstance(roas_data, list) and roas_data:
        roas = float(roas_data[0].get("value", 0.0))

    cpa = round(spend / purchases, 2) if purchases else 0

    if roas < 1.5:
        recommendation = "⛔ Χαμηλό ROAS – Scale Down"
    elif cpa > 20:
        recommendation = "⚠️ Υψηλό CPA – Optimize"
    else:
        recommendation = "✅ Scale Up"

    campaign_list.append({
        "Campaign Name": name,
        "Objective": objective,
        "Status": status,
        "Spend (€)": round(spend, 2),
        "Purchases": purchases,
        "ROAS": roas,
        "CPA": cpa,
        "💬 Recommendation": recommendation
    })

# 4. Εμφάνιση αποτελεσμάτων
if campaign_list:
    df = pd.DataFrame(campaign_list)
    st.dataframe(df)
else:
    st.info("Δεν υπάρχουν ενεργές καμπάνιες με δεδομένα για τις τελευταίες 7 μέρες.")