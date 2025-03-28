import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="NotTheSame Ads Optimizer", layout="wide")
st.title("📊 NotTheSame Ads Optimizer — Meta Real-Time & CSV Analysis")

# Έλεγχος για Meta Token
token = st.secrets.get("META_ACCESS_TOKEN", None)
if not token:
    st.error("❌ Δεν βρέθηκε META_ACCESS_TOKEN. Βάλ' το στο Streamlit Secrets panel.")
    st.stop()

st.success("🔗 Meta Access Token ενεργό!")
st.markdown("---")

# 📁 CSV Upload Module
st.header("📁 Upload Meta Ads CSV για Ανάλυση")

uploaded_file = st.file_uploader("Επέλεξε CSV αρχείο εξαγωγής από Meta Ads Reporting", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Το αρχείο ανέβηκε επιτυχώς!")

        st.subheader("🔍 Προεπισκόπηση Δεδομένων")
        st.dataframe(df.head())

        # Εμφάνιση όλων των στηλών που υπάρχουν
        st.caption("🧠 Εντοπισμένες στήλες στο αρχείο:")
        st.write(list(df.columns))

        # Normalize function για αντιστοίχιση
        def normalize(col):
            return re.sub(r'[^a-z]', '', col.lower())

        normalized_cols = {normalize(col): col for col in df.columns}

        column_mapping = {
            'Campaign Name': ['campaignname', 'campaign'],
            'Amount Spent': ['amountspent', 'spend'],
            'Purchases': ['purchases', 'αγορες'],
            'Purchase ROAS': ['purchaseroas', 'roas', 'returnonadspend']
        }

        rename_dict = {}
        for target_col, patterns in column_mapping.items():
            for pattern in patterns:
                if pattern in normalized_cols:
                    rename_dict[normalized_cols[pattern]] = target_col
                    break

        df = df.rename(columns=rename_dict)

        # Έλεγχος τελικών στηλών
        required_columns = ['Campaign Name', 'Amount Spent', 'Purchases', 'Purchase ROAS']
        if all(col in df.columns for col in required_columns):
            df['Amount Spent'] = pd.to_numeric(df['Amount Spent'], errors='coerce')
            df['Purchases'] = pd.to_numeric(df['Purchases'], errors='coerce')
            df['Purchase ROAS'] = pd.to_numeric(df['Purchase ROAS'], errors='coerce')
            df['CPA'] = df['Amount Spent'] / df['Purchases']
            
            st.subheader("📈 KPIs Ανάλυση")
            st.dataframe(df[['Campaign Name', 'Amount Spent', 'Purchases', 'Purchase ROAS', 'CPA']])

            st.subheader("🤖 Προτεινόμενες Ενέργειες")
            def suggest_action(row):
                if row['Purchase ROAS'] < 1.5:
                    return "⛔ Χαμηλό ROAS – Επανεξέταση ή Pause"
                elif row['CPA'] > 20:
                    return "⚠️ Υψηλό CPA – Προτείνεται Scaling με caution"
                else:
                    return "✅ Καλή Απόδοση – Προτείνεται Scale"

            df['Πρόταση'] = df.apply(suggest_action, axis=1)
            st.dataframe(df[['Campaign Name', 'Purchase ROAS', 'CPA', 'Πρόταση']])
        else:
            st.warning(f"⚠️ Το αρχείο δεν περιέχει τις απαιτούμενες στήλες: {required_columns}")
    except Exception as e:
        st.error(f"❌ Σφάλμα κατά την ανάγνωση του αρχείου: {e}")
else:
    st.info("📤 Ανέβασε ένα CSV για να ξεκινήσει η ανάλυση.")