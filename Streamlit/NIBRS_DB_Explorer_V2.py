import streamlit as st 
import pandas as pd 
import numpy as np 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime as datetime

def loaddata():
    filename = f'./Data/MN{st.session_state.year} NIBRS Report data.csv'
    st.session_state.df = pd.read_csv(filename)


tab_annual, tab_trend, tab_map = st.tabs(['Annual','Trend', 'Map'])

#Use this tab to explore annual trends for specific incident types.
#Show demographic, time of day, weapon use, etc
with tab_annual:
    #Get the year of interest
    if "year" not in st.session_state:
        st.session_state.year = 2022
    st.selectbox(label="Choose Year", options=(2022,2021,2020,2019,2018),index=0, key="year", on_change=loaddata())

    #Load the annual data into a dataframe
    if "annual" not in st.session_state:
        st.session_state.annual = pd.DataFrame()
        
        filename = f"./Data/MN{st.session_state.year} NIBRS Report data.csv"
        st.session_state.annual = pd.read_csv(filename)

    #Get the list of offense_names
    offenses = {}
    with open("offenses.txt", "r") as file:
        for line in file:
            offense, code = line.strip().split(": ")
            offenses[offense] = code

    #BEGIN REPORT
    st.title(f"MN NIBRS data for {st.session_state.year}")
    st.write("""
             The National Incident-Based Reporting System is an incident-based reporting system used by law enforcement agencies in the United States for collecting and reporting data on crimes. The following reporting tool is generated from data available at the [FBI Crime Data Explorer](https://cde.ucr.cjis.gov).  This tool allows the user to explore Minnesota NIBRS data from 2018-2022 to look at the details of incidents, offenses, and offenders. 
             
             **Use the side menu** to select the year to explore. In this version of the applet, no database is needed as the DB queries are written to '.csv' files.  If you would like to more/other information, please feel free to fork this repository on my github and/or reach out for customization.
             """)
    st.write('''
             # Choose the Offense type to explore
             NIBRS incident data can be grouped by offense type.  Use the drop down menu below to select an offense type.  The plot below shows the number of incidents citing a particular offense code for the given year, and the mean.
             ''')
    
    # Displaying the offense descriptions in a selectbox
    selected_offense = st.selectbox("Select Offense", [f"{offense} ({code})" for offense, code in offenses.items()])
    # Extracting the selected offense description and code
    selected_offense_desc, selected_offense_code = selected_offense.split(" (", 1)

    #filter the data to show only the selected offense. 
    #On startup select 
    filter = st.session_state.df[st.session_state.df["type"]==str(selected_offense_code[:-1])] 

    #Calculate the number of incidents per day
    #---------------->CHECK MATH ON THIS!!!<-------------------
    trend = st.session_state.df[st.session_state.df["type"]==str(selected_offense_code[:-1])].groupby("date")["incident"].count()
    daily_mean = trend.mean()
    incident_count = filter["incident"].count()

    #Agency with most recorded incidents
    agencies = filter.groupby("agency_name")["incident"].count().nlargest(1)

    st.write(f"**{selected_offense_desc}** occured **{incident_count}** times in {st.session_state.year}.  The daily *mean* occurances was **{daily_mean:.1f}**.",
            f'The highest rate of incidents were reported by **{agencies.index[0]}** with a total of **{agencies[0]}** incidents.' )

    #OFFENSE OCCURANCE PLOT
    #plot the trend line
    fig = px.line(data_frame=trend, labels={"Date", "Count"}, title=f"{selected_offense_desc}")
    #add the mean of the trend
    fig.add_hline(y = trend.mean(), 
                line_color="black",
                line_dash="dash",
                annotation_text = f"{selected_offense_desc} mean = {trend.mean():.1f}",
                annotation_position="bottom right",
                annotation_font_size=16,
                annotation_font_color="black",
                name = f"Mean = {trend.mean():.1f}")
    fig.update_layout(showlegend=False,
                      xaxis_title="Date",
                      yaxis_title = "Count")
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    #WHAT ARE INCIDENT OFFENDER DEMOGRAPHICS?
    #Pie chart of age-sex-race
    st.write('''
            # What are the demographics of the incident offenders?
            The NIBRS system allows for 1 incident to have multiple offenses assigned to it.  It also tracks offenders. Offenders can commit multiple offenses, and multiple offenders can commit 1 incident. Therefore, when analyzing the offender demographics we are dealing with a dataset larger than the actual incidents.  
            ''')  
    age_summary = filter['age'].value_counts()
    sex_summary = filter['sex'].value_counts()
    race_summary =filter['race'].value_counts()

    fig2 = make_subplots(rows=1, cols=3, subplot_titles=("Age","Sex","Race"), specs=[[{"type": "histogram"}, {"type": "pie"}, {"type": "pie"}]])
    age_trace = go.Histogram(x=filter['age'], y=filter['incident'], histfunc='count', legendgroup='1')
    sex_trace = go.Pie(labels=filter['sex'].unique(), values=sex_summary.values[:], legendgroup='2')
    race_trace = go.Pie(labels=filter['race'].unique(), values=race_summary.values[:], legendgroup='3')
    fig2.append_trace(age_trace, 1,1)
    fig2.append_trace(sex_trace,1,2)
    fig2.append_trace(race_trace,1,3)
    #-------------------->FIX THE LEGEND LOCATION<------------------
    fig2.update_layout(legend=dict(orientation="h",y=-0.5),
                    legend_tracegroupgap=150
                    )
    st.plotly_chart(fig2,theme='streamlit', use_container_width=True)

    #WHEN DO INCIDENTS OCCUR?
    #histogram of weekday and hourly occurances
    st.write(f'''
            # When do {selected_offense_desc}s occur?
            The NIBRS reporting includes the date hour of occurance.  We can use this data to determine:
            1. Is the incident more likely on weekdays or weekends?
            2. Is there a particular time when the incident is more likely to occur?
            3. Are there correlations between the time of day and different incidents?
            ''')
    fig3 = make_subplots(rows=1, cols=2, subplot_titles=("Weekday","24H Occurance"))
    wkd_trace = go.Histogram(x=filter["weekday"], y=filter["incident"], histfunc='count', nbinsx=7, name="Weekday")
    hr_trace = go.Histogram(x=filter["hour"], y=filter["incident"],  histfunc='count', nbinsx=24, name="Hour")
    fig3.append_trace(wkd_trace, 1,1)
    fig3.append_trace(hr_trace,1,2)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3,theme='streamlit', use_container_width=True)

    st.write(f'''
            # Were Weapons involved in {selected_offense_desc}s?   
            ''')
    fig4 = px.pie(data_frame=filter[["incident","weapon"]], names='weapon', values='incident' )
    st.plotly_chart(fig4, theme='streamlit',use_container_width=True)

#Use a 30-day rolling average to explore multi-year trends for offenses
with tab_trend:
    st.write(f'''
               Use this section of the report to review and compare longer term trends of incidents.  The data presented here uses a 30-day rolling average to smooth out the daily noise in the count of incidents.  The data is for the entire state of Minnesota.  As with any analysis, care must be taken when interpretting the results especially when the data has been filtered/manipulated.  
             ''')
    #Load the trend data
    if "trends" not in st.session_state:
        trends = pd.DataFrame()
        filename = f'./Data/MN NIBRS Offense Trend.csv'
        st.session_state.trends = pd.read_csv(filename)
        st.session_state.trends.set_index("incident_date", inplace=True)

        
    #Multiselect offenses    
    #selected_offenses = st.multiselect(label="Select Offenses to compare", options=[f"{offense} ({code})" for offense, code in offenses.items()])
    #selected_offense_desc, selected_offense_code = selected_offenses.split(" (", 1)
    selected_offenses = st.multiselect(label="Select Offenses to compare", options=st.session_state.trends.columns)
    
    #OFFENSES TREND PLOT(S)
    #plot the trend line  
    df = st.session_state.trends[selected_offenses]
    
    fig = px.line(data_frame=df, y=selected_offenses, title="30-day Rolling Average", )
    fig.update_layout(showlegend=True,
                      xaxis_title="Date",
                      yaxis_title = "Count"
                      )
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
    st.write('''
             ---
             Let's take a look at the Minimum and Maximum values for each of the selected columns.  Do you see a trend in the data?  Are incidents counts goin up or down?  
             ''')

    for col in df.columns:
        st.write(f'''
                 ### {col} \n
                 MINIMUM counts: {df[col].min():.2f} occured on {df[col].idxmin()}. \n 
                 MAXIMUM counts: {df[col].max():.2f} occured on {df[col].idxmax()}. \n
                 MIN / MAX delta: {df[col].max()/df[col].min()*100:.2f}% \n
        
            ''')
with tab_map:
    st.write("## Coming Soon!")
