import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Find a School that Best Fits YOU")

@st.cache
def loadData():
    data=pd.read_excel("Student_Admissions_Dashboard_Rd1.xlsx")
    return data

schoolData = loadData()

# Cleaning Data
#Keeping only totals
#mask = schoolData["school_group"].isnull()
#??schoolData = schoolData[mask]

## Interface

st.sidebar.title("Which Program is Right for You?")

visualization=st.sidebar.radio("Select a category to narrow your path for college!",
                 options=["Cost & Earnings", "Admissions", "Locations", "Student Life", ])


sizeRange=st.sidebar.slider("Select the size of the schools:",
                            min_value=int(schoolData["UGDS"].min()),
                            max_value=int(schoolData["UGDS"].max()),
                            value=(int(schoolData["UGDS"].min()), int(schoolData["UGDS"].max())))

#FilterDataSet
mask=schoolData["UGDS"].between(sizeRange[0], sizeRange[1])
schoolData=schoolData[mask]

## Select States
schoolData = schoolData.sort_values("STABBR")
selectedSchools=st.sidebar.multiselect("Select the states to be included:",
                                       options=schoolData["STABBR"].unique(),
                                       default=schoolData["STABBR"].unique())

mask=schoolData["STABBR"].isin(selectedSchools)
schoolData=schoolData[mask]

#Finance
if visualization=="Cost & Earnings":
    st.header("Cost & Earnings")
    #schoolData['DEBT_N'] = schoolData['schoolData'].str.replace('PrivacySuppressed', "0")
    schoolData = schoolData.rename(columns={"COSTT4_A":"Cost", "MD_EARN_WNE_INC1_P6":"Earnings", "DEBT_N":"Debt"})
    fig = px.scatter(schoolData, x="Cost", y="Debt", color="Earnings", hover_name="INSTNM")
    st.plotly_chart(fig)

#Visualization "Student Life"
if visualization=="Student Life":
    st.header("Student Life")

#Race/Ethnicity Pie Chart
#st.header("Race and Ethnicity in Schools")


if visualization=="Student Life":
    schoolData = schoolData.sort_values("INSTNM")
    selectedSchools=st.selectbox("Select One School",
    options=schoolData["INSTNM"].unique())
    mask=schoolData["INSTNM"]==selectedSchools
    schoolData=schoolData[mask]

    schoolData_population = schoolData.melt(
        id_vars=["INSTNM"],  # column that uniquely identifies a row (can be multiple_
        value_vars=["UGDS_WHITE", "UGDS_BLACK", "UGDS_HISP", "UGDS_ASIAN", "UGDS_AIAN", "UGDS_NHPI"],
        var_name="race_ethnicity",  # name for the new column created by melting
        value_name="population"  # name for new column containing values from melted columns
    )

    schoolData_population["race_ethnicity"] = schoolData_population["race_ethnicity"].replace("UGDS_WHITE", "White")
    schoolData_population["race_ethnicity"] = schoolData_population["race_ethnicity"].replace("UGDS_BLACK",
                                                                                              "African American")
    schoolData_population["race_ethnicity"] = schoolData_population["race_ethnicity"].replace("UGDS_HISP", "Hispanic")
    schoolData_population["race_ethnicity"] = schoolData_population["race_ethnicity"].replace("UGDS_ASIAN", "Asian")
    schoolData_population["race_ethnicity"] = schoolData_population["race_ethnicity"].replace("UGDS_AIAN",
                                                                                              "Native American")
    schoolData_population["race_ethnicity"] = schoolData_population["race_ethnicity"].replace("UGDS_NHPI",
                                                                                              "American Pacific Islander")
    fig = px.pie(schoolData_population, values="population", names="race_ethnicity",
                 title="Population Percentage per Race")
    st.plotly_chart(fig)

#Histogram Race & Ethnicity vs Earnings

    #schoolData = px.data.tips()
    #fig = px.histogram(schoolData, x="MD_EARN_WNE_INC1_P6", color="race_ethnicity")
    #fig.show()

    #fig = px.histogram(schoolData, x="UGDS_WHITE", color="MD_EARN_WNE_INC1_P6", marginal="rug",
                       #title="Earnings White")
    #fig.update_layout(barmode="overlay")
    #fig.update_traces(opacity=0.75)
    #st.plotly_chart(fig)

    # population_summary = schoolData_population.groupby("race_ethnicity").sum()

    # percentage = str(round(x*100)) + '%' print(percentage)

    #col1, col2 = st.columns(2)

    #with col1:
        #fig = px.pie(SchoolData_population, values="population", names="race_ethnicity", title="Population Percentage per Race")
    #st.plotly_chart(fig)
    #st.write(population_summary)

    #with col2:
        #fig2 = px.bar(population_summary, x=population_summary.index, y="population")
    #st.plotly_chart(fig2)

#Map of School Location



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

if visualization == "Locations":
    st.header("Compare cities and states!")
    # Map
    fig = go.Figure(data=go.Scattergeo(
        lon=schoolData['LONGITUDE'],
        lat=schoolData['LATITUDE'],
        text=schoolData['INSTNM'],
        mode='markers',
        marker_color=schoolData['LOCALE2'],

    ))

    fig.update_layout(
        title='School Location',
        geo_scope='usa',
    )
    st.plotly_chart(fig)









