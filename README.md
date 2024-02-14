# MN NIBRS Data explorer
--- 
## Description
The National Incident-Based Reporting System is an incident-based reporting system used by law enforcement agencies in the United States for collecting and reporting data on crimes. The following reporting tool is generated from data available at the [FBI Crime Data Explorer](https://cde.ucr.cjis.gov).  This tool allows the user to explore Minnesota NIBRS data from 2018-2022 to look at the details of incidents, offenses, and offenders.

The web applet was developed using Streamlit.io to create an interactive data exploration experience.  Streamlit offers a variety of interactive tools to explore the immense NIBRS data set.  I will continue to develop the web applet as I explore the data.  If there are features you would like to see, please let me know.

---
## Streamlit App
[Streamlit App](https://mn-nibrs.streamlit.app/)


---
## Exploratory Analysis
*Analysis/Exploratory Analysis.ipynb*

Use this jupyter-stle notebook to test out exploratory analysis before deploying via streamlit.  Because the data is cumbersome, I run a local version of the MN 2018-2022 data as a PostGRE SQL database. 

### Concatenated data
Unlike the streamlit app, the EA notebook includes queries that combine 2018-2022 data. This data gives us a better understanding of long term trends in offenses.  In addition to the raw data, I use a 30-day rolling average to smooth the day to day noise. Graphs can include both noisy and smoothed data as needed.  Using the rolling average we can compare different offense in a much cleaner way as shown below.

![Motor Vehicle Theft](/SupportingDocs/motor%20vehicle%20theft.png)

![Top Ten Offense](/SupportingDocs/top%20ten%20offenses.png)



