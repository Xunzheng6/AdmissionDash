import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Find a School that Best Fits YOU")

schoolData = pd.read_excel("Student_Admissions_Dashboard_Rd1.xlsx")

# Cleaning Data
#Keeping only totals
#mask = schoolData["school_group"].isnull()
#??schoolData = schoolData[mask]

## Interface

st.sidebar.title("Which Program is Right for You?")

visualization=st.sidebar.radio("Select a category to narrow your path for college!",
                 options=["School Information", "Admissions", "Student Life", "Finance"])


#sizeRange=st.sidebar.slider("Select the size of the schools:",
                            #min_value=int(schoolData["tot"].min()),
                            #max_value=int(schoolData["tot"].max()),
                            #value=(int(schoolData["tot"].min()), int(schoolData["tot"].max())))

#FilterDataSet
#mask=schoolData["tot"].between(sizeRange[0], sizeRange[1])
#schoolData=schoolData[mask]

## Select Schools
selectedSchools=st.sidebar.multiselect("Select the states to be included:",
                                       options=schoolData["STABBR"].unique())

st.write(schoolData)

#Finance
st.header("Finance")
df = schoolData
df = df.rename(columns={"COSTT4_A":"Cost", "MD_EARN_WNE_INC1_P6":"Earnings", "DEBT_N":"Debt"})
fig = px.scatter(df, x="Cost", y="Earnings", color="Debt", hover_name="INSTNM")
fig.show()