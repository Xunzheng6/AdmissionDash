import streamlit as st
import pandas as pd

st.title("Admission Dashboard")

SchoolData = pd.read_excel('Student_Admissions_Dashboard_Rd1.xlsx')

st.sidebar.title('Controls')

