import io
from tkinter import *
import tkinter as tk

import mysql.connector
from PIL import ImageTk, Image
from tkinter import font
import webbrowser
import pandas as pd
import requests

connection = mysql.connector.connect(
    host="relational.fit.cvut.cz",
    database="ErgastF1",
    user="guest",
    password="relational",
    port="3306"
)
def main():
    get_driver_fastests_laps(connection)

# Get drivers ID
def get_driver_id (driver_name, connection):
    query_drivers_names = "SELECT * FROM drivers WHERE CONCAT(forename, ' ', surname) = '{0}'".format(driver_name)
    df_mysql = pd.read_sql(query_drivers_names, con=connection)
    driver_id = df_mysql['driverId'][0]
    return driver_id

# Get the first five fastests the driver has made
def get_driver_fastests_laps(connection):
    global str
    driver_id = get_driver_id('Lewis Hamilton', connection)
    query_drivers_results = "SELECT * FROM results WHERE driverId = {0}".format(driver_id)
    df_mysql = pd.read_sql(query_drivers_results, con=connection)
    # Drop any NA rows
    df_mysql = df_mysql.dropna()

    # Sort by the top five fastests laps
    df_first_five_laps = df_mysql.sort_values(by=['fastestLapTime']).head(5)
    pd.set_option('display.max_columns', None)

    print(df_first_five_laps)
    print(df_first_five_laps[['fastestLapTime', 'fastestLapSpeed']])

    str = ','.join(["'" + str(x) + "'" for x in df_first_five_laps['raceId'].tolist()])

    print(str)

if __name__ == '__main__':
    main()