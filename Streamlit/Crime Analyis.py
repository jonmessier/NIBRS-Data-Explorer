import streamlit as st 
import pandas as pd 
import numpy as np 
import json
import requests
import plotly.express as px 
import datetime as datetime

#Mapping tools
import folium
from streamlit_folium import st_folium 

#FBI API
api_key = "aO1jZ8CtjeDFmfwhbT5Of9FZR0sSjRFpgwV4Yd2b"



def main():
    #Define Tabs
    arrests, agency_codes =st.tabs(["Arrests", "State Agency Codes"])


    states = states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", 
                       "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", 
                       "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", 
                       "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", 
                       "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]    

    #Define the Sidebar to filter the data  
    state = st.sidebar.selectbox("State Slection",states, index=None)

    category = st.sidebar.selectbox("Choose Category",("offense","offender","victim"))
    cat_type = st.sidebar.selectbox("Choose Type",('count', 'age', 'sex', 'race', 'ethnicity', 'relationship', 'location', 'linkedoffense', 'weapons'))
    offense = st.sidebar.selectbox("Choose Offense", ('all','violent crime', 'aggrevated assault', 'burglary','larceny','motor-vehicle-theft', 'homicide','rape','robbery','arson','property-crime'))
    ori = st.sidebar.text_input("Enter Organization ORI number")
    from_date, to_date = st.sidebar.slider("Select date range", 1985,2023,(1985,2023))

    #from_date = st.sidebar.date_input(label="From -- Year > X")
    #to_date = st.sidebar.date_input(label="To -- Year > X")


    #Agency Data Tab
    with agency_codes:
        st.header("State Agency Code Finder")
        st.markdown('''
                    Use this tab to find particular state agencies that are reporting to the FBI NIBRS system.
                    This tab requires the *State* field in the sidebar.
                    ''')
        url = "https://api.usa.gov/crime/fbi/cde/agency/byStateAbbr/" + state + "?API_KEY=" + api_key
        response = requests.get(url)
        jsonResponse = response.json()

        agencies = pd.DataFrame(jsonResponse)
        st.write("The table below can be sorted by clicking on the columns.  Use this tool to copy ""ORI"" values")
        st.dataframe(agencies)
        #st.write(agencies)
        #st.json(jsonResponse)


    #Arrests Tab
    with arrests:
        #Use the information in the sidebar to generate a historic plot of selected offenses
        st.header("Arrests")
        st.markdown('''
                    Use this tab to view monthly statistics on state Arrests/Offense/Categories
                    This tab requires the *State* and *Date Range* fields in the sidebar.
                    ''')

        url = f'https://api.usa.gov/crime/fbi/cde/arrest/state/{state}/monthly?from={from_date}&to={to_date}&API_KEY={api_key}'      
     
        
        response = requests.get(url)
        jsonResponse = response.json()
        arrests = pd.DataFrame(jsonResponse['data'])
        #st.dataframe(arrests)
        arrests['date'] = pd.to_datetime([f'{y}-{m}-01' for m, y, in zip(arrests['month_num'],arrests['data_year'])])
        arrest_types = arrests.columns[2:]
        select_offenses = st.multiselect("Select Offense", options=arrest_types)

        fig = px.line(
            data_frame=arrests,
            x="date",
            y=select_offenses
            # opacity=0.75
            # nbins = len(arrests["date"])
        )

        st.plotly_chart(fig, theme='streamlit', use_container_width=True)



    
    
    #NIBRS tab


if __name__ == "__main__":
    main()