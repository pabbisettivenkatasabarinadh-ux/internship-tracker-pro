import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Internship Tracker Pro", layout="wide")

st.markdown("""
<style>
.stApp {
    background-image: linear-gradient(rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.90)), url("https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1920&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
div[data-testid="stMetric"], div[data-testid="stForm"], div[data-testid="stDataFrame"] {
    background-color: rgba(255, 255, 255, 0.96) !important;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.google-watermark {
    position: fixed;
    bottom: 20px;
    right: 20px;
    opacity: 0.08;
    z-index: 0;
    width: 180px;
}
</style>
<div class="google-watermark">
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" width="180">
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg", width=110)
with col2:
    st.title("My Internship Tracker - PRO")

st.write("Track your internships with Google Secure Login")
st.divider()

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

with st.sidebar:
    st.header("Add New")
    with st.form("add_form"):
        company = st.text_input("Company Name")
        role = st.text_input("Role / Position")
        status = st.selectbox("Status", ["applied", "interview", "offer", "rejected"])
        applied_date = st.date_input("Applied Date", value=date.today())
        link = st.text_input("Job Link")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Application")
        if submitted:
            if company:
                new_entry = {
                    "company": company,
                    "role": role,
                    "status": status,
                    "date": str(applied_date),
                    "link": link,
                    "notes": notes
                }
                data.append(new_entry)
                save_data(data)
                st.success(f"{company} added!")
                st.rerun()
            else:
                st.error("Company Name required!")

if len(data) == 0:
    st.info("No applications yet. Add from sidebar!")
else:
    df = pd.DataFrame(data)
    c1, c2, c3, c4 = st.columns(4)
    if 'status' in df.columns:
        c1.metric("Total Applied", len(df))
        c2.metric("Interviews", len(df[df['status'] == 'interview']))
        c3.metric("Offers", len(df[df['status'] == 'offer']))
        c4.metric("Rejected", len(df[df['status'] == 'rejected']))
    else:
        c1.metric("Total Applied", len(df))

    st.subheader("Filter")
    if 'status' in df.columns:
        status_filter = st.multiselect("Filter by Status", options=df['status'].unique(), default=list(df['status'].unique()))
        filtered_df = df[df['status'].isin(status_filter)] if status_filter else df
    else:
        filtered_df = df

    st.dataframe(filtered_df, use_container_width=True)

    if not filtered_df.empty and 'status' in filtered_df.columns:
        fig = px.pie(filtered_df, names='status', title='Application Statistics')
        st.plotly_chart(fig, use_container_width=True)
