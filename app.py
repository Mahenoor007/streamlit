import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.set_page_config(page_title="Interactive Data Dashboard", layout="wide")
st.title("Interactive Data Dashboard")
st.write("Upload your CSV file, explore the data, and visualize it with interactive features.")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    # Read dataset
    data = pd.read_csv(uploaded_file)

    # Display dataset preview
    st.header("Dataset Preview")
    st.dataframe(data.head())

    # Display basic statistics
    st.header("Summary Statistics")
    st.write(data.describe())

    # Sidebar for interactive options
    st.sidebar.header("Visualization Options")

    # Column selection for visualization
    columns = data.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to visualize", columns)

    if selected_columns:
        # Plot type selection
        plot_type = st.sidebar.selectbox("Select a plot type", ["Line Chart", "Bar Chart", "Histogram"])

        # Visualization
        st.header("Data Visualization")
        if plot_type == "Line Chart":
            st.line_chart(data[selected_columns])
        elif plot_type == "Bar Chart":
            st.bar_chart(data[selected_columns])
        elif plot_type == "Histogram":
            for col in selected_columns:
                st.subheader(f"Histogram for {col}")
                fig, ax = plt.subplots()
                sns.histplot(data[col], kde=True, ax=ax)
                st.pyplot(fig)

    # Additional feature: Download button
    st.header("Download Processed Data")
    if st.button("Download Dataset"):
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )

    # Filters
    st.header("Filter Data")
    filter_col = st.selectbox("Select column to filter", columns)
    if filter_col:
        unique_values = data[filter_col].unique()
        selected_value = st.multiselect(f"Filter {filter_col} by value", unique_values)
        if selected_value:
            filtered_data = data[data[filter_col].isin(selected_value)]
            st.dataframe(filtered_data)
