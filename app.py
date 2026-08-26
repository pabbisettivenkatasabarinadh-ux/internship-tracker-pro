import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

st.set_page_config(page_title="internship tracker pro",layout="wide")

# ---- GOOGLE LOGIN ----
if not st.user.is_logged_in:
    st.title("Internship Tracker PRO ")
    st.write("Google tho login avvu Chintu!")
    if st.button("Continue with Google"):
        st.login("google")
    st.stop()

# ---- LOGIN AYYAKA ----
st.sidebar.success(f"Hi {st.user.name}! ")
st.sidebar.write(st.user.email)
if st.sidebar.button("Logout"):
    st.logout()

st.title(f"Welcome {st.user.name}! ")
st.write("Nee internships ikkada track cheddam!")



st.set_page_config(page_title="Internship Tracker PRO", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #f8fafc; }
</style>
""", unsafe_allow_html=True)

st.title(" Internship Tracker PRO")
st.write("Google + Office Design")

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if data:
                    return pd.DataFrame(data)
        except:
            pass
    return pd.DataFrame(columns=["Company", "Role", "Status", "Date"])

def save_data(df):
    df.to_json(DATA_FILE, orient="records", indent=2)

df = load_data()

with st.form("add_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        company = st.text_input("Company")
    with col2:
        role = st.text_input("Role")
    with col3:
        status = st.selectbox("Status", ["Applied", "Interview", "Offer", "Rejected"])
    submitted = st.form_submit_button("Add Internship")
    if submitted and company:
        new_row = {"Company": company, "Role": role, "Status": status, "Date": pd.Timestamp.now().strftime("%Y-%m-%d")}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Added!")
        st.rerun()

if not df.empty:
    status_filter = st.multiselect("Filter by Status", options=df['status'].unique() if 'status' in df.columns else df['Status'].unique(), default=None)
    if status_filter:
        filtered_df = df[df['Status'].isin(status_filter)] if 'Status' in df.columns else df
    else:
        filtered_df = df

    st.dataframe(filtered_df, width="stretch")

    if not filtered_df.empty and 'Status' in filtered_df.columns:
        fig = px.pie(filtered_df, names='Status', title='Application Statistics')
        st.plotly_chart(fig, width="stretch")
else:
    st.info("No internships yet. Add one above!")