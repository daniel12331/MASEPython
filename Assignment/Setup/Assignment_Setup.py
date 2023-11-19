import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

import tkinter
from tkinter import messagebox

from sqlalchemy.exc import SQLAlchemyError

root = tkinter.Tk()
root.withdraw()


df_circuits = pd.read_csv('archive/circuits.csv')
df_constructor_results = pd.read_csv('archive/constructor_results.csv')
df_constructor_standings = pd.read_csv('archive/constructor_standings.csv')
df_constructors = pd.read_csv('archive/constructors.csv')
df_driver_standings = pd.read_csv('archive/driver_standings.csv')
df_drivers = pd.read_csv('archive/drivers.csv')
df_lap_times = pd.read_csv('archive/lap_times.csv')
df_pit_stops = pd.read_csv('archive/pit_stops.csv')
df_qualifying = pd.read_csv('archive/qualifying.csv')
df_races = pd.read_csv('archive/races.csv')
df_results = pd.read_csv('archive/results.csv')
df_seasons = pd.read_csv('archive/seasons.csv')
df_sprint_results = pd.read_csv('archive/sprint_results.csv')
df_status = pd.read_csv('archive/status.csv')


try:
    # engine = mysql.connector.connect(
    #     host="localhost",
    #     database="f1",
    #     user="root",
    #     password="root",
    #     port="3306"
    # )
    engine = create_engine("mysql+mysqlconnector://root:root@localhost/f1")
    df_circuits.to_sql(name='circuits', con=engine, if_exists='append', index=False)
    df_constructor_results.to_sql(name='constructor_results', con=engine, if_exists='append', index=False)
    df_constructor_standings.to_sql(name='constructor_standings', con=engine, if_exists='append', index=False)
    df_constructors.to_sql(name='constructors', con=engine, if_exists='append', index=False)
    df_driver_standings.to_sql(name='driver_standings', con=engine, if_exists='append', index=False)
    df_drivers.to_sql(name='drivers', con=engine, if_exists='append', index=False)
    df_lap_times.to_sql(name='lap_times', con=engine, if_exists='append', index=False)
    df_pit_stops.to_sql(name='pit_stops', con=engine, if_exists='append', index=False)
    df_qualifying.to_sql(name='qualifying', con=engine, if_exists='append', index=False)
    df_races.to_sql(name='races', con=engine, if_exists='append', index=False)
    df_results.to_sql(name='results', con=engine, if_exists='append', index=False)
    df_seasons.to_sql(name='seasons', con=engine, if_exists='append', index=False)
    df_sprint_results.to_sql(name='sprint_results', con=engine, if_exists='append', index=False)
    df_status.to_sql(name='status', con=engine, if_exists='append', index=False)
    messagebox.showinfo("Successful", "The database has been loaded and created successfully!")

except SQLAlchemyError:
    messagebox.showerror("ERROR", "The database hasnt been created properly")



