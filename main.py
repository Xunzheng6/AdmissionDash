import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Find a School that Best Fits YOU")

schoolData = pd.read_csv("Cohorts/Most-Recent-Cohorts-Institution.csv")

# Cleaning Data
#Keeping only totals
mask = schoolData["school_group"].isnull()
#??schoolData = schoolData[mask]

## Interface

st.sidebar.title("Which Program is Right for You?")

visualization=st.sidebar.radio("Select a category to narrow your path for college!",
                 options=["School Information", "Admissions", "Student Life", "Finance"])


sizeRange=st.sidebar.slider("Select the size of the schools:",
                            min_value=int(schoolData["tot"].min()),
                            max_value=int(schoolData["tot"].max()),
                            value=(int(schoolData["tot"].min()), int(schoolData["tot"].max())))

st.write(schoolData)