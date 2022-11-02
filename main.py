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
    #schoolData['DEBT_N'] = schoolData['schoolData'].str.replace('PrivacySuppressed', "0")
    df = df.rename(columns={"COSTT4_A":"Cost", "MD_EARN_WNE_INC1_P6":"Earnings", "DEBT_N":"Debt"})
    fig = px.scatter(df, x="Cost", y="Earnings", color="Debt", hover_name="INSTNM")
    st.plotly_chart(fig)

#Visualization "Student Life"
if visualization=="Student Life":
    st.header("Student Life")

#Race/Ethnicity Pie Chart
#st.header("Race and Ethnicity in Schools")

#schoolData_population = schoolData.melt(
    #id_vars=["UGDS"], # column that uniquely identifies a row (can be multiple_
    #value_vars=["UGDS_WHITE", "UGDS_BLACK", "UGDS_HISP", "UGDS_ASIAN", "UGDS_AIAN", "UGDS_NHPI"],
    #var_name="race_ethnicity", # name for the new column created by melting
    #value_name="population" # name for new column containing values from melted columns
#)

#schoolData_population["race_ethnicity"]= schoolData_population["race_ethnicity"].replace("UGDS_WHITE", "White")
#schoolData_population["race_ethnicity"]= schoolData_population["race_ethnicity"].replace("UGDS_BLACK", "African American")
#schoolData_population["race_ethnicity"]= schoolData_population["race_ethnicity"].replace("UGDS_HISP", "Hispanic")
#schoolData_population["race_ethnicity"]= schoolData_population["race_ethnicity"].replace("UGDS_ASIAN", "Asian")
#schoolData_population["race_ethnicity"]= schoolData_population["race_ethnicity"].replace("UGDS_AIAN", "Native American")
#schoolData_population["race_ethnicity"]= schoolData_population["race_ethnicity"].replace("UGDS_NHPI", "American Pacific Islander")

#population_summary = schoolData_population.groupby("race_ethnicity").sum()

#percentage = str(round(x*100)) + '%' print(percentage)

#if visualization=="Student Life":
    #col1, col2 = st.columns(2)

    #with col1:
        #fig = px.pie(SchoolData_population, values="population", names="race_ethnicity", title="Population Percentage per Race")
    #st.plotly_chart(fig)
    #st.write(population_summary)

    #with col2:
        #fig2 = px.bar(population_summary, x=population_summary.index, y="population")
    #st.plotly_chart(fig2)

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
if visualization == "Admissions":
    st.header("Admissions")
    #st.header2("Please select up to 5 Universities for Comparison")
    # max selection not working , max_selections=5
    Top5Selection = st.multiselect('Please Select Your Top 5 School for Comparison:',
                                   options=schoolData["INSTNM"].unique())
    BasicInfo = schoolData[['INSTNM', 'CITY','INSTURL','ADM_RATE','SAT_AVG_ALL','ACTCMMID']]
    mask = BasicInfo['INSTNM'].isin(Top5Selection)
    st.write(BasicInfo[mask])
    fig = px.bar(schoolData[mask], x='INSTNM', y='SATVRMID')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='INSTNM', y='SATMTMID')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='INSTNM', y='SATWRMID')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='INSTNM', y='ACTENMID')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='INSTNM', y='ACTMTMID')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='INSTNM', y='ACTWRMID')
    st.plotly_chart(fig)












