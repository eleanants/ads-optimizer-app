
import streamlit as st

# Mocked example for accounts_data (to be replaced with real API response)
accounts_data = [
    {"name": "Pharmacy Ads Account", "id": "123456"},
    {"id": "789012"},  # Missing name
    {"name": "Fashion Ads", "id": "345678"}
]

# Διόρθωση για ασφαλή ανάγνωση των πεδίων
account_options = {
    acc.get("name", f"Account {acc.get('id', 'unknown')}"): acc.get("id", "")
    for acc in accounts_data if "id" in acc
}

st.title("Διαχείριση Λογαριασμών Meta Ads")
st.write("Διαθέσιμοι Λογαριασμοί:")
st.json(account_options)
