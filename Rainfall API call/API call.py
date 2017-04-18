import requests
import pandas as pd

directory_to_store_files = 'C:\\Users\\matt.miller\\OneDrive - Agrimetrics\\'
#local directory to store obtained files from API call

uri = "http://environment.data.gov.uk/flood-monitoring/archive/readings-"
#URI for API calls

station_ref_uri = 'http://environment.data.gov.uk/flood-monitoring/id/stations?parameter=rainfall'
#get metadata associated with each observation station e.g. location. file returned is in json-ld

def get_rainfall_data(start_date,end_date):
    #Input start date and end date for rainfall data required, in the format yyyy-mm-dd. Each day will produce a separate csv file
    daterange = pd.date_range(start_date, end_date)
    for specificdate in daterange:
        specificdate = specificdate.strftime("%Y-%m-%d")
        r = requests.get(uri+specificdate+'.csv')
        with open(directory_to_store_files+specificdate+'.csv', "wb") as dataset:
            dataset.write(r.content)
            print("saving..."+specificdate+'.csv')


def get_station_reference_data():
    metadatarequest = requests.get(station_ref_uri)
    with open (directory_to_store_files+'station reference data.jsonld', "wb") as metadata:
        print("saving...station reference data.jsonld")
        metadata.write(metadatarequest.content)


get_rainfall_data('2017-01-01','2017-01-02')
get_station_reference_data()
