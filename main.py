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

## Interface
st.sidebar.title("Which Program is Right for You?")
visualization=st.sidebar.radio("Select a category to narrow your path for college!",
                 options=["Cost & Earnings", "Admissions", "Locations", "Student Life", ])
#School size range
sizeRange=st.sidebar.slider("Select the size of the schools:",
                            min_value=int(schoolData["UGDS"].min()),
                            max_value=int(schoolData["UGDS"].max()),
                            value=(int(schoolData["UGDS"].min()), int(schoolData["UGDS"].max())))
#school size filter
mask=schoolData["UGDS"].between(sizeRange[0], sizeRange[1])
schoolData=schoolData[mask]
## Select states
schoolData = schoolData.sort_values("STABBR")
selectedSchools=st.sidebar.multiselect("Select the states to be included:",
                                       options=schoolData["STABBR"].unique(),
                                       default=schoolData["STABBR"].unique())
#state filter
mask=schoolData["STABBR"].isin(selectedSchools)
schoolData=schoolData[mask]

#Finance
if visualization=="Cost & Earnings":
    st.header("Cost, Debt & Earnings")
    st.write('Note: Some of the data are not available for the schools')
    #schoolData['DEBT_N'] = schoolData['schoolData'].str.replace('PrivacySuppressed', "0")
    schoolData = schoolData.rename(columns={"COSTT4_A":"Cost", "MD_EARN_WNE_INC1_P6":"Earnings", "DEBT_N":"Debt"})
    fig = px.scatter(schoolData, x="Earnings", y="Debt", color = "Cost", hover_name="INSTNM")
    st.plotly_chart(fig)

#Visualization "Student Life"
if visualization=="Student Life":
    st.header("Student Life")
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
    st.write('Please select your top schools for comparison. '
             'Note that not every school has shared the data with us.')
    schoolData = schoolData.sort_values("INSTNM")
    Top5Selection = st.multiselect('Select Schools:',
                                   options=schoolData["INSTNM"].unique(),
                                   default=['CUNY Bernard M Baruch College', 'New York University',
                                            'CUNY Brooklyn College','Barnard College',
                                            'Adelphi University',
                                            'Columbia University in the City of New York'])
    schoolData = schoolData.rename(columns={"INSTNM": "University Name", "INSTURL": "University Website",
                                            "ADM_RATE": "Admission Rate","SAT_AVG_ALL": "SAT Average",
                                            "ACTCMMID": "ACT Average","SATVRMID": "SAT Verbal","SATMTMID": "SAT Math",
                                            "SATWRMID": "SAT Writing","ACTENMID": "ACT English","ACTMTMID": "ACT Math",
                                            "ACTWRMID": "ACT Writing","CITY": "City"})

    #schoolData['Admission Rate'].apply(lambda a:str(round(schoolData['Admission Rate'] * 100)) + '%')
    #schoolData['ACT Average'] = schoolData['Admission Rate'].apply(lambda schoolData: round(schoolData['ACT Average']))
    BasicInfo = schoolData[['University Name', 'City','University Website','Admission Rate',
                            'SAT Average','ACT Average']]
    mask = BasicInfo['University Name'].isin(Top5Selection)
    st.write(BasicInfo[mask])
    st.subheader('SAT Scores by Subjects & Schools')
    fig = px.bar(schoolData[mask], x='University Name', y='SAT Verbal',text_auto=True,
                 title='SAT Verbal Score Comparison')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='University Name', y='SAT Math',text_auto=True,
                 title='SAT Math Score Comparison')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='University Name', y='SAT Writing',text_auto=True,
                 title='SAT Writing Score Comparison')
    st.plotly_chart(fig)
    st.write('ACT Scores by Subject & Schools')
    fig = px.bar(schoolData[mask], x='University Name', y='ACT English',text_auto=True,
                 title='ACT English Score Comparison')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='University Name', y='ACT Math',text_auto=True,
                 title='ACT Math Score Comparison')
    st.plotly_chart(fig)
    fig = px.bar(schoolData[mask], x='University Name', y='ACT Writing',text_auto=True,
                 title='ACT Writing Score Comparison')
    st.plotly_chart(fig)

if visualization == "Locations":
    st.header("Compare cities and states!")
    st.write ("Purple and Blue Colored Locations are Urban Cities while Orange and Yellow Locations are Suburban Cities")

    # Map
    fig = go.Figure(data=go.Scattergeo(
        lon=schoolData['LONGITUDE'],
        lat=schoolData['LATITUDE'],
        text=schoolData['INSTNM'],
        mode='markers',
        marker_color=schoolData['LOCALE2']

    ))

    fig.update_layout(
        title='School Locations',
        geo_scope='usa',
    )
    st.plotly_chart(fig)









