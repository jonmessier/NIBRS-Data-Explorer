# Install the Pyscopg Postgre SQL adaptor for Python
#Use the Streamlit Virtual environment for this install

#pip install psycopg2-binary
#Documentation can be found at  https://www.psycopg.org/docs/
#It is recomended to use psycopg2 for production packages
#--->UPDATE in next .V

#PostGRE SQL library
import pandas as pd
import psycopg2 as psg

#Query the NIBRS PostGRE db
#when changing the query be sure to change the column names of the resulting dataframe 
#2021/2022
"""
q = '''
    select ni.incident_date, ni.incident_hour, ni.incident_id, ni.agency_id, a.ncic_agency_name, no.offense_code, ne.ethnicity_name, rr.race_desc, nwt.weapon_name, noff.age_num, noff.sex_code
    from nibrs_incident ni
    Right join nibrs_offense no on ni.incident_id = no.incident_id
    left join nibrs_offender noff on no.incident_id = noff.incident_id
    join nibrs_ethnicity ne on noff.ethnicity_id = ne.ethnicity_id
    join ref_race rr on noff.race_id = rr.race_id
    join agencies a on ni.agency_id = a.agency_id
    left join nibrs_weapon nw on no.offense_id = nw.offense_id
    left join nibrs_weapon_type nwt on nw.weapon_id=nwt.weapon_id
    '''
"""
#2018-2020 - the offense_type_id stored differently
q='''select ni.incident_date, ni.incident_hour, ni.incident_id, ni.agency_id, a.ncic_agency_name, 
	  ot.offense_code, ne.ethnicity_name, rr.race_desc, nwt.weapon_name, noff.age_num, 
	  noff.sex_code
    from nibrs_incident ni
    Right join nibrs_offense no on ni.incident_id = no.incident_id
    left join nibrs_offender noff on no.incident_id = noff.incident_id
    join nibrs_ethnicity ne on noff.ethnicity_id = ne.ethnicity_id
    join ref_race rr on noff.race_id = rr.race_id
    join agencies a on ni.agency_id = a.agency_id
    left join nibrs_weapon nw on no.offense_id = nw.offense_id
    left join nibrs_weapon_type nwt on nw.weapon_id=nwt.weapon_id
	join nibrs_offense_type ot on no.offense_type_id = ot.offense_type_id
    '''
try:
    #establish conection to database
    conn = psg.connect(dbname="MN2018", user="postgres", password="1234", host='localhost', port=5432)

    # Open a cursor to perform database operations
    # cursor class allows interaction with the database
    cur = conn.cursor()
    print("PostgreSQL server information")
    print(conn.get_dsn_parameters(), "\n")

    # Execute a query
    cur.execute(q)

    
#Collect Errors
except Exception as error:
    print("Error while connecting to PostgreSQL", error)

#Close the Connection
finally:
    if (conn):
        # Retrieve query results
        df = pd.DataFrame(cur.fetchall())
        
        #name the columns, add the weekday column
        df.columns = ["date","hour","incident","agencyID", "agency_name","type", "ethnicity", "race","weapon",'age','sex'] #Match with query
        df['weekday'] = df["date"].dt.strftime("%A")

        #Write to csv
        df.to_csv("MN2018 NIBRS Report data.csv", encoding='utf-8', index=False)
        
        #close the cursor and connection to the database
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")
