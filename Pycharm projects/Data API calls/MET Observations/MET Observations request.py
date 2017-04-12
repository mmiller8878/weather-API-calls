import requests
from xml.etree import ElementTree as ET
import pandas as pd
from datetime import datetime as DT
import os

"""The pattern of the data request is: send a POST request containing the desired parameters. Within the html response 
there is a link, which is then used in a GET request. The response to this GET request is a csv file containing weather data """

directory_to_save =  'C:/Users/matt.miller/OneDrive - Agrimetrics/met office obs/2015/'

#URL for API calls
url = "https://weather.data.gov.uk/query"

#example parameters for the initial post request
params = {"Type": "Observation",
          "PredictionSiteID": "ALL",
          "ObservationSiteID": "ALL",
          "Date": "03/04/2017",
          "PredictionTime": "0300"}.

def post_request():

    try:
        post = requests.post(url, data = params)
        post.raise_for_status()
        return(post.text)
    except:
        raise


def parse_html_response():
    #the html response contains a link
    try:
        htmltree = ET.fromstring(post_request())
        findlink = htmltree.find("body/div/p/a")
        link = findlink.attrib
        return link['href']
    except:
        raise

def get_hourly_csv_file():
    try:
        '''function processes the get request, saves to specified directory and checks each item for number of lines'''
        #this first bit alters the format of that date so that it is in a form thet the website will accept
        date = DT.strptime(params["Date"], "%d/%m/%Y")
        date = date.strftime('%d-%m-%Y')
        date=str(date)
        time = DT.strptime(params["PredictionTime"], "%H%M")
        time = time.strftime("%H%M")
        time=str(time)
        #the actual get request
        get = requests.get(parse_html_response())
        with open(directory_to_save+'WeatherObs_'+date+"_"+time+".csv", "wb") as weatherobs:
            weatherobs.write(get.content)
            print("saved...WeatherObs_"+date+"_"+time+".csv")
        with open (directory_to_save+'WeatherObs_'+date+"_"+time+".csv", "r") as weather:
            num_lines = sum(1 for line in weather)
            if num_lines < 100:
                write_warnings_to_log(date,time,num_lines)
    except:
        raise



def generate_hourly_daterange(start_date,end_date):
    '''generates a range of datetimes at hourly intervals '''
    try:
        date_and_time=[]
    #converts datetime to the english format (dd/mm/yyyy hhmm)
        start_date = DT.strptime(start_date, "%d/%m/%Y-%H%M")
        end_date = DT.strptime(end_date, "%d/%m/%Y-%H%M")
        for datetime in pd.date_range(start_date,end_date, freq='1h').strftime("%d/%m/%Y %H%M"):
            datetime = datetime.split( )
            date_and_time.append(datetime)
        return date_and_time
    except (ValueError):
        raise




def get_measurements(daterange):
    '''this works but only for dates in 2016'''
    try:
        for i in daterange:
            try:
                params["Date"] = i[0]
                params["PredictionTime"] = i[1]
                get_hourly_csv_file()
            except requests.exceptions.MissingSchema:
                with open(directory_to_save + "warning log.txt", 'a+') as logfile:
                    logfile.write("Missing file: WeatherObs_%s_%s.csv does not exist\n" % (i[0], i[1]))
                print("Missing file: WeatherObs_%s_%s.csv does not exist, skipping..." % (i[0], i[1]))
                pass
            except (TimeoutError, requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
                with open(directory_to_save + "warning log.txt", 'a+') as logfile:
                    logfile.write("Handled Timeout error with WeatherObs_%s_%s.csv, host failed to respond\n" % (i[0], i[1]))
                print("Timeout Error with WeatherObs_%s_%s.csv - attempting reconnection...\n" % (i[0], i[1]))
                continue
    except:
        raise

def write_warnings_to_log(inputdate,inputtime,lines):
    with open (directory_to_save+"warning log.txt", 'a+') as logfile:
        logfile.write("file WeatherObs_%s_%s.csv only has %s lines\n" %(inputdate, inputtime, lines))




def main():
    d = generate_hourly_daterange('24/10/2015-1800', '31/12/2015-2300')
    get_measurements(d)
    if os.path.isfile(directory_to_save+"warning log.txt") == True:
        print('Completed, but there were warnings - please check warning log.txt')
    else:
        print('Completed without any warnings')


if __name__ == '__main__':
    main()

