import streamlit as st
import pandas as pd
import plotly.express as px

# Set page style
st.set_page_config(layout="wide")

# Show the browser window scrollbar
import modules.scrollbar as scrollbar
scrollbar.show_scrollbar()

# Auto change St.metrics text from light to dark depending on mode
import streamlit as st

st.markdown(
    """
    <style>
    /* st.metric value */
    [data-testid="stMetricValue"] {
        color: #007BFF; !important;
    }

    /* st.metric label */
    [data-testid="stMetricLabel"] {
        color: var(--st-text-color) !important;
    }

    /* Optional: metric delta text */
    [data-testid="stMetricDelta"] {
        color: var(--st-text-color) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title('Ecomove Management Dashboard')
st.sidebar.title('Ecomove')
st.sidebar.divider()
# Add the Overall Metrics
st.subheader('Overall Metrics')

# Load data from ecomove.ipynb after cleaning
df=pd.read_excel("cleaned_ds.xlsx")

# Calculate the overall KPIs
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
kpi = {
        "Revenue": df_kpi['Ticket_Revenue_EUR'].sum(),
        "Delay": df_kpi['Average_Delay_Minutes'].mean(),
        "CO2": df_kpi['CO2_Saved_KG'].sum(),
        "Rating": df_kpi['Customer_Rating'].mean(),
        "Complaints": df_kpi['Accessibility_Complaints'].sum()
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

cols = st.columns([3, 2, 2, 3, 2])
cols[0].metric("Total Revenue (€)", f"{kpi['Revenue']:,.2f}")
cols[1].metric("Avg Delay (min)", f"{kpi['Delay']:.2f}")
cols[2].metric("Avg Rating", f"{kpi['Rating']:.2f}")
cols[3].metric("CO2 Saved (kg)", f"{kpi['CO2']:,.2f}")
cols[4].metric("Complaints", f"{kpi['Complaints']:.0f}")

st.divider()


# Map coordinates for each city in the data
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

# Add required filters to sidebar
st.sidebar.header("💼 Executive Filters")

# Filter 1: Fixed City
selection_1 = st.sidebar.selectbox("Select City", options=df['City'].unique())

# All available filter categories
filter_options = ['Transport_Mode', 'Route_Type', 'Weather', 'Event_Day', 'Country']

# Filter 2: User picks category and value
col_name_1 = st.sidebar.selectbox("Option 1", options=filter_options)
selection_2 = st.sidebar.selectbox(f"Select {col_name_1}", options=df[col_name_1].unique())

# Ensure selected categories cannot be selected again
remaining_options = [opt for opt in filter_options if opt != col_name_1]

# Show remaining filters
col_name_2 = st.sidebar.selectbox("Option 2", options=remaining_options)
selection_3 = st.sidebar.selectbox(f"Select {col_name_2}", options=df[col_name_2].unique())

# Filtering process
filtered_df = df[
    (df['City'] == selection_1) & 
    (df[col_name_1] == selection_2) & 
    (df[col_name_2] == selection_3)
]

# Calculate the KPIs
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

# Add the tabs for eaach visualisation
st.subheader(f"Transport Analytics: {selection_1}")

st.markdown('<p>The metrics based on Executive Filters are diplayed here. Choose tab to access further details for the selected city.</p>', 
            unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Key Metrics", "📉 Trend Analysis", "🗺️ Geo Map","🔗 Correlations","🎻Plots", "↔️Comparisons"])

with tab1:
    # Add the metrics
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
    # Show trends
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
    # Plot locations on the European Map
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
            opacity=0.1,
            zoom=10,
            hover_name="City",
            title=f"Location Analysis for {selection_1}"
        )

        
        fig_map.update_layout(
            map_style="open-street-map", 
            margin={"r":0,"t":40,"l":0,"b":0}
        )

        fig_map.update_layout(mapbox_center={"lat": filtered_df['lat'].mean(), 
                                             "lon": filtered_df['lon'].mean()}, mapbox_zoom=10)
        
        st.plotly_chart(fig_map, width='stretch')

with tab4:
    #Create the Correlation Heatmap
    st.subheader("Numerical Correlation Matrix")
    st.write("This map shows how strongly two metrics are related. 1.0 is a perfect positive correlation, -1.0 is a perfect negative correlation.")

    if filtered_df.empty:
        st.warning("No data available for correlation analysis.")
    else:
        numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])

        numeric_df = numeric_df.drop(columns=['lon', 'lat'])
        
        corr_matrix = numeric_df.corr()

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


with tab5:
    # Show the violin and Box plots for the selected data
    st.subheader("Metric Distributions - Violin and Box Plots")
    
    if filtered_df.empty:
        st.warning("No data matches these filters.")
    else:
        filtered_df =filtered_df.drop(columns=['Record_ID', 'lat','lon','Date','Country', 'Route_Type'])
        numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        all_cat_cols = [c for c in filtered_df.columns if c not in numeric_cols]
        
        # To prevent a plot with only one single bar (since City/Opt1/Opt2 are filtered),
        # we let the user pick a grouping column that isn't one of the fixed filters.
        fixed_filters = ['City', col_name_1, col_name_2]
        grouping_options = [c for c in all_cat_cols if c not in fixed_filters]
        
        # If no other categories exist, fallback to any categorical column
        category_col = st.selectbox("Group by:", options=grouping_options if grouping_options else all_cat_cols)

        # PREVENT "DOTS": Force category to string for Plotly
        plot_df = filtered_df.copy()
        plot_df[category_col] = plot_df[category_col].astype(str)

        for metric in numeric_cols:
            st.write(f"### {metric}")
            col1, col2 = st.columns(2)
            
            with col1:
                fig_violin = px.violin(
                    plot_df,
                    x=category_col,
                    y=metric,
                    color=category_col,
                    box=True,
                    points="all",
                    template="plotly_white"
                )
                fig_violin.update_xaxes(type='category') # FORCES categorical layout
                fig_violin.update_layout(showlegend=False, margin=dict(t=30, b=0))
                st.plotly_chart(fig_violin, width='stretch')
            
            with col2:
                fig_box = px.box(
                    plot_df,
                    x=category_col,
                    y=metric,
                    color=category_col,
                    points="outliers",
                    template="plotly_white"
                )
                fig_box.update_xaxes(type='category') # FORCES categorical layout
                fig_box.update_layout(showlegend=False, margin=dict(t=30, b=0))
                st.plotly_chart(fig_box, width='stretch')
            
            st.divider()
with tab6:
    # Add a visualisation to compare the selected city in the sidebar 
    # and the city select in the select box. The code should remove the 
    # city selected in the sidebar from the select box dynamically

    st.subheader('Compare City Key Metrics')
    


    if filtered_df.empty:
        st.warning("No data available for comparison.")
    else:
        available_cities = (
            df.loc[df["City"] != selection_1, "City"]
            .dropna()
            .unique()
            .tolist()
        )

        if not available_cities:
            st.warning("No other cities are available for comparison.")
        else:
            city_to_compare = st.selectbox(
                "Choose City:",
                options=available_cities
            )

            metric_options = [
                "Ticket_Revenue_EUR",
                "Average_Delay_Minutes",
                "CO2_Saved_KG",
                "Customer_Rating",
                "Accessibility_Complaints",
            ]

            selected_metrics = st.multiselect(
                "Choose Metrics to Compare:",
                options=metric_options,
                default=metric_options
            )

            if not selected_metrics:
                st.info(
                    "Select at least one metric to create the bar chart."
                )
            else:
                selected_cities = [
                    selection_1,
                    city_to_compare
                ]

                # Use only the selected cities and metrics
                comparison_df = df.loc[
                    df["City"].isin(selected_cities),
                    ["City"] + selected_metrics
                ].copy()

                # Convert selected metrics to numeric
                comparison_df[selected_metrics] = comparison_df[
                    selected_metrics
                ].apply(pd.to_numeric, errors="coerce")

                # Calculate average values by city
                grouped_df = (
                    comparison_df
                    .groupby("City", as_index=False)[selected_metrics]
                    .mean()
                )

                # Reshape data for Plotly
                chart_df = grouped_df.melt(
                    id_vars="City",
                    value_vars=selected_metrics,
                    var_name="Metric",
                    value_name="Value"
                ).dropna(subset=["Value"])

                if chart_df.empty:
                    st.warning(
                        "No data is available for the selected cities "
                        "and metrics."
                    )
                else:
                    fig = px.bar(
                        chart_df,
                        x="Metric",
                        y="Value",
                        color="City",
                        barmode="group",
                        text_auto=".2f",
                        title=(
                            f"Metric Comparison: "
                            f"{selection_1} vs {city_to_compare}"
                        ),
                        category_orders={
                            "City": selected_cities,
                            "Metric": selected_metrics
                        },
                        color_discrete_sequence=(
                            px.colors.qualitative.Set2
                        )
                    )

                    fig.update_layout(
                        xaxis_title="Metric",
                        yaxis_title="Average Value",
                        legend_title="City",
                        height=600,
                        hovermode="x unified"
                    )

                    fig.update_traces(
                        textposition="outside"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )
st.sidebar.divider()
st.sidebar.markdown("<h4 style='text-align: center;'>Dashboard Created by: 25119947 for COM7021</h4>", unsafe_allow_html=True)