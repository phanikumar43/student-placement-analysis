import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Placement Analysis", layout="wide")

st.title("📊 Student Placement Analysis")

# Load dataset (IMPORTANT: correct relative path)
df = pd.read_csv("data/student_data.csv")

st.subheader("Dataset Preview")
st.dataframe(df)

st.subheader("Basic Statistics")
st.write(df.describe())
