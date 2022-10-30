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


sizeRange=st.sidebar.slider("Select the size of the schools:",
                            min_value=int(schoolData["UGDS"].min()),
                            max_value=int(schoolData["UGDS"].max()),
                            value=(int(schoolData["UGDS"].min()), int(schoolData["UGDS"].max())))

#FilterDataSet
#mask=schoolData["STABBR"].between(sizeRange[0], sizeRange[1])
#schoolData=schoolData[mask]

## Select Schools
df = schoolData
df = df.sort_values("STABBR")
selectedSchools=st.sidebar.multiselect("Select the states to be included:",
                                       options=df["STABBR"].unique())


#Finance
if visualization=="Finance":
st.header("Finance")
df = df.rename(columns={"COSTT4_A":"Cost", "MD_EARN_WNE_INC1_P6":"Earnings", "DEBT_N":"Debt"})
fig = px.scatter(df, x="Cost", y="Earnings", color="Debt", hover_name="INSTNM")
fig.show()

#Visualization "Student Life"
if visualization=="Student Life":
    st.header("Student Life")

#Race/Ethnicity Pie Chart
#st.header("Race and Ethnicity in Schools)
#if visualization=="Race/Ethnicity":
    #df = px.data.gapminder().query("year == 2021").query("continent == 'Europe'")
    #df.loc[df['UGDS'] < 2.e6, 'country'] = 'Other countries'  # Represent only large countries
    #fig = px.pie(df, values='UGDS', names='INSTNM', title='Race and Ethnicity of Student Body')
    #fig.show()

#Map of School Location
#geo_df = gpd.read_excel("Student_Admissions_Dashboard_Rd1.xlsx")

#px.set_mapbox_access_token(open(".mapbox_token").read())
#fig = px.scatter_mapbox(geo_df,
                       #lat=LATITUDE.y,
                        #lon=LONGITUDE.x,
                        #hover_name="INSTNM",
                        #zoom=1)
#fig.show()

#Map
#px.set_mapbox_access_token(open(".mapbox_token").read())
#fig = px.scatter_mapbox(df, lat="LATITUDE", lon="LONGITUDE",  color="LOCALE2", size="UGDS")
                  #color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
#fig.show()

# Admission Requirement.
if visualization == "Admission":
    st.header("Admission")

st.header("Admission Requirement")
# max selection not working
# Top5Selection = st.multiselect('Please Select Your Top 5 School for Comparison:',
# options=schoolData["INSTNM"].unique(), max_selections=5)

