import tkinter.messagebox

from tkinter import *
import tkinter as tk
from tkinter import font, ttk

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import Driver_Profile
from Assignment import Driver_Data_1


class Driver_Regression(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)  # Initialize superclass
        """Constructor"""
        self.root = master
        # Title for window and do not kill the window
        self.protocol('WM_DELETE_WINDOW', self.OverrideWindow)

        # Set up the fonts you want to use
        self.ComicF1 = font.Font(family="Calibri", size=16, weight="normal")
        self.ComicF2 = font.Font(family="Calibri", size=12, weight="normal")

        self.resizable(False, False)

        # Windows 1920x1080
        self.width = 1900
        self.height = 1080
        self.geometry('400x400')

        self.connections = None
        self.driver_name = None

        self.s_var = tk.StringVar()

    def set_selected_driver(self, driver_name, connection):
        self.connections = connection
        self.driver_name = driver_name
        self.title(driver_name)
        self.driver_id = Driver_Data_1.get_driver_id(driver_name, connection)

        # Buttons section
        self.buttonPanel = tk.Frame(self, background="black")
        self.buttonPanel.pack(fill="y")
        list_of_circuits = self.load_circuits(self.driver_id, connection)
        self._layoutButtons(self.buttonPanel, list_of_circuits)

    def load_circuits(self, driver_id, connection):
        query_drivers_names = "select name from results Inner join races on results.raceId = races.raceId where driverId = {0}".format(
            driver_id)
        df_mysql = pd.read_sql(query_drivers_names, con=connection)
        df_unique_circuits = df_mysql['name'].unique()
        return df_unique_circuits

    def _layoutButtons(self, parent, circuits):
        self.titleLabel = tk.Label(parent, text="Regression Analysis", font='Helvetica 18 bold')
        self.titleLabel.grid(row=0, column=0, sticky=N + S + E + W)

        self.titleLabel = tk.Label(parent, text="Choose a circuit: ", font=self.ComicF1)
        self.titleLabel.grid(row=1, column=0, sticky=N + S + E + W)
        self.clicked = StringVar()
        self.clicked.set("Choose a grand prix")
        list_circuits = list(circuits)
        self.drop_down = OptionMenu(parent, self.clicked, *list_circuits)
        self.drop_down.grid(row=2, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.titleLabel = tk.Label(parent, text="Enter a new fastest speed(km/hr): ", font=self.ComicF1)
        self.titleLabel.grid(row=3, column=0, sticky=N + S + E + W)
        self.lap_speed = StringVar()
        self.entry_name = tk.Entry(parent, textvariable=self.lap_speed)
        self.entry_name.grid(row=4, column=0, sticky=N + S + E + W, padx=5, pady=5, ipadx=10, ipady=5)

        self.regr_btn = tk.Button(parent, text="Perform Lap Time Prediction", command=self.regression_analysis,
                                  font=self.ComicF2)
        self.regr_btn.grid(row=5, column=0, sticky=N + S + E + W, padx=5, pady=5)

    def regression_analysis(self):

        try:
            lap_speed = float(self.lap_speed.get())
            choosen_circuit = self.clicked.get()
            if choosen_circuit == "Choose a grand prix":
                raise NameError

            query_drivers_names =("select fastestLapSpeed as 'Lap_Speed(km/hr)', fastestLapTime, name from results Inner join races on results.raceId = races.raceId where driverId = {0} and name = '{1}'"
                                  .format(self.driver_id, choosen_circuit))
            df_mysql = pd.read_sql(query_drivers_names, con=self.connections)
            # Converting fastestLapSpeed column to numeric
            df_mysql['Lap_Speed(km/hr)'] = pd.to_numeric(df_mysql['Lap_Speed(km/hr)'], errors='coerce')
            # Using regex to format the lap times into total seconds
            d = {'^(\d+\.\d+)$': r'00:00:\1', '^(\d+:\d+\.\d+)$': r'00:\1'}
            df_mysql['fastestLapTime'] = df_mysql['fastestLapTime'].replace(d, regex=True).apply(
                pd.to_timedelta).dt.total_seconds()

            # Splitting the data into training and testing data
            x_train, x_test, y_train, y_test = train_test_split(df_mysql[['Lap_Speed(km/hr)']], df_mysql[['fastestLapTime']],
                                                                test_size=0.33, random_state=42)
            linear_regr = LinearRegression()
            linear_regr.fit(x_train, y_train)
            regression_score = linear_regr.score(x_test,y_test)

            # Getting list of predictions
            y_pred = linear_regr.predict(x_test)

            # Formating user input into dataframe so prediction can be made
            data = [lap_speed]
            df_prediction = pd.DataFrame(data, columns=['Lap_Speed(km/hr)'])


            # Preform the prediction and get value from 2D array
            individual_prediction = linear_regr.predict(df_prediction)
            individual_prediction = round(individual_prediction[0][0], 3)
            self.hide()
            return individual_prediction,y_pred, regression_score, x_train,x_test,y_train,y_test, choosen_circuit, lap_speed

        except ValueError:
            tkinter.messagebox.showwarning("Invalid Lap Speed", "Please enter a valid speed")
        except NameError:
            tkinter.messagebox.showwarning("No circuit choosen", "Please select a circuit")



    def show(self):
        self.update()  # Update the window
        self.deiconify()  # Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide()  # Hide the window

    def hide(self):
        self.buttonPanel.destroy()
        self.s_var.set("close")
        self.withdraw()
