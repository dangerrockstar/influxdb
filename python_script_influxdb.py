import pandas as pd
from influxdb import DataFrameClient
#import argparse
import numpy as np
#First start your Influx database after that RUN this script 
#connection to Influxdb
host='localhost'
port=8086
user = 'your user name'
password = '*****'
dbname = 'test'
protocol = 'json'
client = DataFrameClient(host, port, user, password, dbname)

#create database into influxdb
print("Create database: " + dbname)
client.create_database(dbname)

#read csv file using pandas Lib and convert that data into pandas DataFamre
file=pd.read_csv(r'type your .csv file path here') #read file
file.info()
print (file.head(1)) #print frist 5 Line
file.tail() #print last 5 Line

#qucik way to create a datafame
print('\n **DataFrame Create**')
df = pd.DataFrame(data=list(range(30)),
                      index=pd.date_range(start='7/20/2017',
                                          periods=30, freq='H'))

#Influxdb first Index as a Timestamp
file['exchange_timestamp']=pd.to_datetime(file['exchange_timestamp'],
    infer_datetime_format=True) #exchange_timestamp is a timestamp

file.set_index('exchange_timestamp', drop= True, inplace=True)
print ('___________________________________\n **Timestamp index set**')

#write(push) data into influxdb 
client.write_points(file,'test', protocol=protocol)

print('____________________________________\n**DataFrame Successfully Saved**')
#write Influxdb qurey as a string and pass into Client
table=client.query("SELECT * FROM test ")
print(table)

#if you want to drop your influxdb enable blowdown line
#client.drop_database(dbname)
