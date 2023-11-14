import io
from tkinter import *
import tkinter as tk

import mysql.connector
from PIL import ImageTk, Image
from tkinter import font
import webbrowser
import pandas as pd
import requests

import matplotlib.pyplot as plt
connections = None
# Get drivers ID
def get_driver_id (driver_name, connection):
    query_drivers_names = "SELECT * FROM drivers WHERE CONCAT(forename, ' ', surname) = '{0}'".format(driver_name)
    df_mysql = pd.read_sql(query_drivers_names, con=connection)
    driver_id = df_mysql['driverId'][0]
    return driver_id

# Get the first five fastests the driver has made
def get_driver_fastests_laps(connection,driver_name):
    connections = connection
    global str
    driver_id = get_driver_id(driver_name, connection)
    # Joining three tables results, races, circuits and select fastestLapTime, fastestLapSpeed, circuits.name, circuits.country
    query_drivers_results = "SELECT fastestLapTime, fastestLapSpeed, circuits.name, circuits.country, year FROM results INNER JOIN races on results.raceId = races.raceId INNER JOIN circuits on races.circuitId = circuits.circuitId WHERE driverId = {0}".format(driver_id)
    df_mysql = pd.read_sql(query_drivers_results, con=connection)

    # Sort by the top five fastests laps
    df_first_five_laps = df_mysql.sort_values(by=['fastestLapTime']).head(5)
    pd.set_option('display.max_columns', None)

    df_first_five_laps['year'] = df_first_five_laps['year'].map(str)

    circuits = df_first_five_laps['name'] + "-" + df_first_five_laps['country'] + " (" + df_first_five_laps['year'] + ")"

    fastestsTimes = df_first_five_laps['fastestLapTime']
    return circuits, fastestsTimes
    #
    # plt.bar(circuits, fastestsTimes, color = 'blue', width = 0.5)
    #
    # plt.xlabel("Fastest Lap Time")
    # plt.ylabel("Circuit names and countries")
    # plt.title("Top 5 Circuits with the fastest lap times")
    # plt.show()