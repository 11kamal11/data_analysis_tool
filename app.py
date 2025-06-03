import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="📊 Enhanced Data Analysis Tool", layout="wide")

st.title("📈 Enhanced Data Analysis Tool")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Show number of rows selector
    st.sidebar.header("Data Controls")
    num_rows = st.sidebar.slider("Number of rows to display", min_value=5, max_value=len(df), value=10)

    st.subheader("Preview of Data")
    st.dataframe(df.head(num_rows))

    st.subheader("Basic Statistics")
    st.write(df.describe())

    st.subheader("Column Info")
    st.write(df.dtypes)

    # Chart section
    st.subheader("📊 Visualizations")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    chart_type = st.selectbox("Choose Chart Type", [
        "Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot", "Pie Chart", "Correlation Heatmap"
    ])

    if chart_type in ["Line Chart", "Bar Chart", "Scatter Plot", "Histogram", "Box Plot"]:
        if numeric_cols:
            x_axis = st.selectbox("X-axis", options=numeric_cols)
            y_axis = st.selectbox("Y-axis", options=numeric_cols)

            if chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis)
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis)
            elif chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axis, y=y_axis)
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis)
            elif chart_type == "Box Plot":
                fig = px.box(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No numeric columns available for selected chart.")
    
    elif chart_type == "Pie Chart":
        if categorical_cols and numeric_cols:
            cat_col = st.selectbox("Category Column", options=categorical_cols)
            num_col = st.selectbox("Numeric Column", options=numeric_cols)
            pie_df = df.groupby(cat_col)[num_col].sum().reset_index()
            fig = px.pie(pie_df, names=cat_col, values=num_col, title=f"{num_col} by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least one categorical and one numeric column for pie chart.")

       elif chart_type == "Correlation Heatmap":
        st.write("Correlation between numeric columns")
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)


