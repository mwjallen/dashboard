import streamlit as st
import pandas as pd
import plotly_express as px

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(layout="wide")

# Show the browser window scrollbar
import modules.scrollbar as scrollbar
scrollbar.show_scrollbar()

st.title('Ecomove Management Dashboard')

st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        text-align: left;
        color: #007BFF; 
    }
    [data-testid="stMetricLabel"] {
        text-align: justify;
        color: #007BFF;
        font-size: 20px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING ---

df=pd.read_excel("cleaned_ds.xlsx")

# COORDINATE MAPPING: This adds Lat/Lon to your 'City' column so the map works.
# Replace these coordinates with your actual city locations.
city_coords = {
    'Paris': {'lat': 48.8566, 'lon': 2.3522},
    'Rotterdam':{'lat':51.9244, 'lon': 4.4777},
    'Lyon':{'lat':45.7578, 'lon': 4.8320},
    'Amsterdam':{'lat':52.3731, 'lon': 4.8925},
    'Vienna':{'lat':48.2083, 'lon': 16.3725},
    'Rome': {'lat': 41.9028, 'lon': 12.4964},
    'Milan':{'lat':45.4642, 'lon': 9.1896},
    'Munich':{'lat':48.1371, 'lon': 11.5754},
    'Hamburg': {'lat': 53.5502, 'lon': 10.0013},
    'Barcelona': {'lat': 41.3826, 'lon': 2.1770},
    'Berlin': {'lat': 52.5174, 'lon': 13.3951},
    'Madrid': {'lat': 40.4167, 'lon': -3.7035},
}

# Map the coordinates to the dataframe
df['lat'] = df['City'].map(lambda x: city_coords.get(x, {}).get('lat', 0))
df['lon'] = df['City'].map(lambda x: city_coords.get(x, {}).get('lon', 0))

# Ensure Date is datetime format and sorted
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# --- 3. SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")

# Filter 1: Fixed City
selection_1 = st.sidebar.selectbox("Select City", options=df['City'].unique())

# All available filter categories
filter_options = ['Transport_Mode', 'Route_Type', 'Weather', 'Event_Day', 'Country']

# Filter 2: User picks category and value
col_name_1 = st.sidebar.selectbox("Option 1", options=filter_options)
selection_2 = st.sidebar.selectbox(f"Select {col_name_1}", options=df[col_name_1].unique())

# --- THE FIX: Remove the chosen col_name_1 from the options for col_name_2 ---
remaining_options = [opt for opt in filter_options if opt != col_name_1]

# Filter 3: Now only shows options NOT chosen in Filter 1
col_name_2 = st.sidebar.selectbox("Option 2", options=remaining_options)
selection_3 = st.sidebar.selectbox(f"Select {col_name_2}", options=df[col_name_2].unique())

# --- 4. DYNAMIC FILTERING LOGIC ---
filtered_df = df[
    (df['City'] == selection_1) & 
    (df[col_name_1] == selection_2) & 
    (df[col_name_2] == selection_3)
]

# --- 5. KPI CALCULATIONS ---
if not filtered_df.empty:
    kpi = {
        "Revenue": filtered_df['Ticket_Revenue_EUR'].sum(),
        "Delay": filtered_df['Average_Delay_Minutes'].mean(),
        "CO2": filtered_df['CO2_Saved_KG'].sum(),
        "Rating": filtered_df['Customer_Rating'].mean(),
        "Complaints": filtered_df['Accessibility_Complaints'].sum()
    }
else:
    kpi = {"Revenue": 0, "Delay": 0, "CO2": 0, "Rating": 0, "Complaints": 0}

# --- 6. MAIN UI TABS ---
st.subheader(f"Transport Analytics: {selection_1}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Key Metrics", "📉 Trend Analysis", "🗺️ Geo Map","🔗 Correlations","🎻Plots"])

with tab1:
    if filtered_df.empty:
        st.warning(f"No data found for {selection_2} and {selection_3} in {selection_1}.")
    else:
        # Inline Metrics
        cols = st.columns([3, 2, 2, 2, 2])
        cols[0].metric("Total Revenue (€)", f"{kpi['Revenue']:,.2f}")
        cols[1].metric("Avg Delay (min)", f"{kpi['Delay']:.2f}")
        cols[2].metric("Avg Rating", f"{kpi['Rating']:.2f}")
        cols[3].metric("CO2 Saved (kg)", f"{kpi['CO2']:,.2f}")
        cols[4].metric("Complaints", f"{kpi['Complaints']:.0f}")
        
        st.divider()
        with st.expander("View Raw Filtered Data"):
            st.dataframe(filtered_df)

with tab2:
    if filtered_df.empty:
        st.warning("No data available for trend analysis.")
    else:
        st.subheader("Performance Trends Over Time")
        
        trend_metric = st.selectbox(
            "Select Metric to Visualize", 
            options=['Ticket_Revenue_EUR', 'Average_Delay_Minutes', 'CO2_Saved_KG', 'Customer_Rating']
        )
        
        # Aggregate for a clean line
        if "Average" in trend_metric or "Rating" in trend_metric:
            trend_data = filtered_df.groupby('Date')[trend_metric].mean().reset_index()
        else:
            trend_data = filtered_df.groupby('Date')[trend_metric].sum().reset_index()
            
        fig_trend = px.line(
            trend_data, x='Date', y=trend_metric, 
            title=f"{trend_metric} Trend for {selection_1}",
            markers=True
        )
        fig_trend.update_traces(line_color='#007BFF', line_width=3)
        fig_trend.update_layout(template="plotly_white", hovermode="x unified")
        st.plotly_chart(fig_trend, width='stretch')

with tab3:
    st.subheader("Geographic Distribution")
    
    if filtered_df.empty:
        st.warning("No data available to map.")
    else:
        # Create Mapbox Scatter
        fig_map = px.scatter_map(
            filtered_df, 
            lat="lat", 
            lon="lon", 
            size="Ticket_Revenue_EUR", 
            color="Customer_Rating", 
            color_continuous_scale=px.colors.sequential.Plotly3_r,
            size_max=35, 
            zoom=10,
            hover_name="City",
            title=f"Location Analysis for {selection_1}"
        )

        
        fig_map.update_layout(
            mapbox_style="open-street-map", 
            margin={"r":0,"t":40,"l":0,"b":0}
        )

        fig_map.update_layout(mapbox_center={"lat": filtered_df['lat'].mean(), 
                                             "lon": filtered_df['lon'].mean()}, mapbox_zoom=10)
        
        st.plotly_chart(fig_map, width='stretch')

with tab4:
    st.subheader("Numerical Correlation Matrix")
    st.write("This map shows how strongly two metrics are related. 1.0 is a perfect positive correlation, -1.0 is a perfect negative correlation.")

    if filtered_df.empty:
        st.warning("No data available for correlation analysis.")
    else:
        # 1. Select only numerical columns for correlation
        numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])

        numeric_df = numeric_df.drop(columns=['lon', 'lat'])
        
        # 2. Calculate the correlation matrix
        corr_matrix = numeric_df.corr()

        # 3. Create the Plotly Heatmap
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True, # This puts the actual numbers inside the squares
            aspect="auto",
            color_continuous_scale='RdBu_r', # Red-Blue scale: Red=Neg, Blue=Pos
            zmin=-1, zmax=1 # Force the scale to be exactly -1 to 1
        )
        
        fig_corr.update_layout(
            title="Metric Correlation Heatmap",
            xaxis_title="Metrics",
            yaxis_title="Metrics",
            template="plotly_white"
        )
        
        st.plotly_chart(fig_corr, width='stretch')
        