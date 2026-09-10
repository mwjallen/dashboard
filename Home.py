import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Data Visualisation Dashboard", layout="wide")

# Show the browser window scrollbar
import modules.scrollbar as scrollbar
scrollbar.show_scrollbar()

st.sidebar.title("Ecomove")
st.sidebar.subheader("Data Dashboard")

df=pd.read_excel("cleaned_ds.xlsx")

# Drop the Record_Id
df_cols_filtered = df.columns.drop(["Record_ID"])

# Define the limit
MAX_ITEMS = 3
selected_filters = st.sidebar.multiselect("Select Filters (Max 3)", options=df_cols_filtered)

if len(selected_filters) > MAX_ITEMS:
    st.error(f"Please select a maximum of {MAX_ITEMS} filters.")
    # Stop the rest of the app from running to prevent incorrect KPI calculations
    st.stop() 

# If we reach this point, the selection is within the limit
if selected_filters:
    filtered_df = df[df['Date'].isin(selected_filters)]
else:
    filtered_df = df

df_kpi = df[
    [
        "Date",
        "Ticket_Revenue_EUR",
        "Average_Delay_Minutes",
        "Customer_Rating",
        "CO2_Saved_KG",
        "Accessibility_Complaints",
    ]
].copy()

df_kpi["Date"] = pd.to_datetime(df_kpi["Date"], errors="coerce")
df_kpi = df_kpi.dropna(subset=["Date"])

# KPI Metrics
st.title("Ecomove Management Dashboard")  
st.divider()
st.subheader("Key Performance Indicators (KPIs)") 

kpi = {
    "Total Revenue (€)": df_kpi["Ticket_Revenue_EUR"].sum(),
    "Avg Delay (min)": df_kpi["Average_Delay_Minutes"].mean(),
    "Avg Customer Rating": df_kpi["Customer_Rating"].mean(),
    "Total CO2 Saved (kg)": df_kpi["CO2_Saved_KG"].sum(),
    "Accessibility Complaints": df_kpi["Accessibility_Complaints"].sum(),
}

# Add CSS to center and turn metrics blue
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        text-align: left;
        color: #1E90FF; 
    }
    [data-testid="stMetricLabel"] {
        text-align: justify;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

cols = st.columns([3, 2, 2, 2, 2])

cols[0].metric("Total Revenue (€)", f"{kpi['Total Revenue (€)']:,.2f}")
cols[1].metric("Avg Delay (min)", f"{kpi['Avg Delay (min)']:.2f}")
cols[2].metric("Avg Customer Rating", f"{kpi['Avg Customer Rating']:.2f}")
cols[3].metric("Total CO2 Saved (kg)", f"{kpi['Total CO2 Saved (kg)']:.2f}")
cols[4].metric("Accessibility Complaints", f"{kpi['Accessibility Complaints']:.0f}")

st.divider()

tb_rating, tb_complaints = st.tabs(['Customer Rating', 'Customer Complaints'])