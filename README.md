# MN NIBRS Data explorer
--- 
## Description
The National Incident-Based Reporting System is an incident-based reporting system used by law enforcement agencies in the United States for collecting and reporting data on crimes. The following reporting tool is generated from data available at the [FBI Crime Data Explorer](https://cde.ucr.cjis.gov).  This tool allows the user to explore Minnesota NIBRS data from 2018-2022 to look at the details of incidents, offenses, and offenders.

The web applet was developed using Streamlit.io to create an interactive data exploration experience.  Streamlit offers a variety of interactive tools to explore the immense NIBRS data set.  I will continue to develop the web applet as I explore the data.  If there are features you would like to see, please let me know.

**Timeline of development**
- [x] 1/20/2024 - Gather MN 2018-2022 data locally for analysis.  Explore with Pg4admin POSTGRE SQL workbench
- [x] 1/29/2024 - Generate basic streamlit application to show annual offense trends 
- [x] 2/4/2024 - Exploratory Analysis with jupyter style notebook for ease of use
- [ ] 2/13/2024 - Documentation/Readme
- [ ] 

**Work in Progress**
- [ ] Explore machine learning capabilities
- [ ] Add "ORI"/"County" search features
- [ ] Add Mapping tools to Streamlit
  - [ ] Show hotspots based on ORI
  


---
## Streamlit App
[Streamlit App](https://mn-nibrs.streamlit.app/)

UPDATE - 2/13/2024 : Streamlit cloud is a bit finicky with syntax when running applets.  Small changes in the Github repo to the *NIBRS_DB_Explorer.py* have been crashing the cloud version, but seem to run fine locally.  Work in progress to minimize the cloud version uptime.

---
## Exploratory Analysis
*Analysis/Exploratory Analysis.ipynb*

Use this jupyter-stle notebook to test out exploratory analysis before deploying via streamlit.  Because the data is cumbersome, I run a local version of the MN 2018-2022 data as a PostGRE SQL database. 

### Concatenated data
Unlike the streamlit app, the EA notebook includes queries that combine 2018-2022 data. This data gives us a better understanding of long term trends in offenses.  In addition to the raw data, I use a 30-day rolling average to smooth the day to day noise. Graphs can include both noisy and smoothed data as needed.  Using the rolling average we can compare different offense in a much cleaner way as shown below.

![Motor Vehicle Theft](/SupportingDocs/motor%20vehicle%20theft.png)

![Top Ten Offense](SupportingDocs/top%2010%20offenses.png)



