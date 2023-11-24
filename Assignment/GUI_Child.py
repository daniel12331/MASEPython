from tkinter import *
import tkinter as tk

import self
from PIL import ImageTk
from tkinter import font, ttk
import webbrowser
import Driver_Profile
import Driver_Data_1
import Driver_Data_2
from Driver_Regression import Driver_Regression

import matplotlib.pyplot as plt
import matplotlib.pyplot as mlines
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AChild(tk.Toplevel):
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
        self.geometry('1915x1080')

        # MAC 13.3 RES
        # self.width = 1400
        # self.height = 800
        # self.geometry('1440x800')

        self.connections = None
        self.driver_name = None
        self.Regression_ChildObj = Driver_Regression(self)
        self.Regression_ChildObj.withdraw()

    def set_selected_driver(self, driver_name, connection):
        self.connections = connection
        self.driver_name = driver_name
        self.title(driver_name)
        driver_info = Driver_Profile.get_driver_url(driver_name, connection)

        # Buttons section
        self.buttonPanel = tk.Frame(self, background="black")
        self.buttonPanel.pack(side="left", fill="y")
        self._layoutButtons(self.buttonPanel, driver_info)

        # Canvas section
        self.canvasPanel = tk.Frame(self, background="black")
        self.canvasPanel.pack(side="right", fill="both", expand=True)
        self._layoutCanvas(self.canvasPanel, driver_info)

    def _layoutButtons(self, parent, driver_info):
        self.titleLabel = tk.Label(parent, text="Analyse", font=self.ComicF1)
        self.titleLabel.grid(row=0, column=0, sticky=N + S + E + W)

        self.web_link = tk.Button(parent, text="Info", command=lambda url=driver_info: self.open_link(url),
                                  font=self.ComicF2)
        self.web_link.grid(row=1, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.races_btn = tk.Button(parent, text="Races", command=self.loadRacesData1, font=self.ComicF2)
        self.races_btn.grid(row=2, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.racesv2_btn = tk.Button(parent, text="RacesV2", command=self.loadRacesData2, font=self.ComicF2)
        self.racesv2_btn.grid(row=3, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.compare_driver = tk.Button(parent, text="Compare", command=self.loadRacesData2, font=self.ComicF2)
        self.compare_driver.grid(row=4, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.regression_btn = tk.Button(parent, text="Regression", command=self.loadRegression, font=self.ComicF2)
        self.regression_btn.grid(row=5, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.close_Frame = tk.Button(parent, text="Go Back", command=self.hide, font=self.ComicF2)
        self.close_Frame.grid(row=6, column=0, sticky=N + S + E + W, padx=5, pady=5)

    def open_link(self, url):
        webbrowser.open(url)

    def _layoutCanvas(self, parent, driver_info):

        try:
            pil_image = Driver_Profile.get_driver_image(driver_info)
            self.image = ImageTk.PhotoImage(pil_image)

            self.canvas = tk.Canvas(parent, height=self.height, width=self.width)
            self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
            self.canvas.create_image(0, 1, anchor='nw', image=self.image)

        except Exception as e:
            self.loadDefaultImg(parent)

    def loadDefaultImg(self, parent):
        img_Path = 'images/no_image.png'
        self.image = ImageTk.PhotoImage(file=img_Path)

        self.canvas = tk.Canvas(parent, height=1080, width=1920)
        self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
        self.canvas.create_image(0, 1, anchor='nw', image=self.image)

    def loadRacesData1(self):
        # Get the drivers five fastest laps
        fastestsTimes = Driver_Data_1.get_driver_fastests_laps(self.connections, self.driver_name)

        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, dpi=70)

        ax1.bar(fastestsTimes['racetracks'], fastestsTimes['fastestLapTime'])
        ax1.set_ylabel('Fastests Lap times (seconds)')
        ax1.set_title('Top Five Fastest Lap Times')
        ax1.set_ylim(min(fastestsTimes['fastestLapTime']) - 0.5, max(fastestsTimes['fastestLapTime'] + 0.5))
        ax1.tick_params(axis='x', labelrotation=15)

        for patch in ax1.patches:
            x0, y0 = patch.get_xy()
            x0 += patch.get_width() / 2
            y0 += patch.get_height()
            color = patch.get_facecolor()
            ax1.text(x0, y0, str(y0), ha="center", va="bottom", color="white", clip_on=True,
                     bbox=dict(ec="black", fc=color))

        # Get the drivers total wins and loses
        driver_wins, driver_loses = Driver_Data_1.get_driver_wins_losses(self.connections, self.driver_name)
        labels = 'Wins', 'Loses'

        ax2.pie((driver_wins, driver_loses), labels=labels, autopct='% 1.1f %%'
                , shadow=True, startangle=90, explode=(0.05, 0.05), colors=['#5AF04B', '#DF3939'])
        ax2.axis('equal')
        ax2.set_title('Total Wins and Loses')

        # Get the drivers average pitstop time
        average_pitstop_duration = Driver_Data_1.get_driver_average_pitstop_lap(self.connections, self.driver_name)
        ax3.plot(average_pitstop_duration['raceId'], average_pitstop_duration['duration'], color='orange',
                 linewidth='2')
        ax3.set_xlabel('Total Races')
        ax3.set_ylabel('Average Pit stop duration (seconds)')
        ax3.set_title('Average Pit Stop Time For Each Race')

        fastestSpeeds = Driver_Data_1.get_driver_top_speed(self.connections, self.driver_name)

        s = ax4.barh(fastestSpeeds['name'], fastestSpeeds['fastestLapSpeed'], color='darkorchid')
        ax4.set_xlabel('Highest Speeds (km/h)')

        ax4.set_title('Top Five Fastest Speeds')
        high_limit = max(fastestSpeeds['fastestLapSpeed']) + 5
        low_limit = min(fastestSpeeds['fastestLapSpeed']) - 5
        ax4.set_xlim(low_limit, high_limit)

        ax4.tick_params(axis='y', labelrotation=50)
        ax4.bar_label(s, label_type="center", color='white')

        canvas = FigureCanvasTkAgg(fig, master=self.canvasPanel)
        canvas_widget = canvas.get_tk_widget()

        canvas_widget.grid(row=3, column=0, sticky=N + S + E + W)

        canvas.draw()

    def loadRacesData2(self):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, dpi=70)

        # Get the driver and constructors total points
        consPoints_driverPoints_relationship = Driver_Data_2.get_driver_constructor_points(self.connections,
                                                                                           self.driver_name)

        ax1.scatter(consPoints_driverPoints_relationship['constructor_points'],
                    consPoints_driverPoints_relationship['driver_points'], color='deepskyblue', marker='o')
        line = mlines.Line2D([0, 1], [0, 1], color='red')
        transform = ax1.transAxes
        line.set_transform(transform)
        ax1.add_line(line)

        ax1.set_xlabel('Constructor Points')
        ax1.set_ylabel('Driver Points')
        ax1.set_title('Relationship Constructor & Driver points (Top 15 wins)')
        ax1.grid(True, linestyle='--', alpha=0.7)

        # Get the drivers & constructor total wins and loses
        df_top_fifteen_wins_constructor = Driver_Data_2.get_driver_constructor_wins(self.connections, self.driver_name)

        bar_width = 0.4
        bar_positions = range(len(df_top_fifteen_wins_constructor))

        ax2.bar(bar_positions, df_top_fifteen_wins_constructor['constructor_wins'], color='yellowgreen',
                label='Constructor Wins', width=bar_width)
        ax2.bar([pos + bar_width for pos in bar_positions], df_top_fifteen_wins_constructor['driver_wins'],
                color='lightcoral', width=bar_width, label='Driver Wins')

        ax2.set_xticks([pos + bar_width / 2 for pos in bar_positions])
        ax2.set_xticklabels(f'Race {i + 1}' for i in bar_positions)
        ax2.set_xlabel('Races')
        ax2.set_ylabel('Number of wins')
        ax2.set_title('Constructor Wins and driver win contribution')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend()

        # Get drivers status
        df_driver_status = Driver_Data_2.get_driver_status_races(self.connections, self.driver_name)

        ax3.barh(df_driver_status['status'], df_driver_status['count'], color='salmon')
        ax3.set_xlabel('Count of statuses')
        ax3.set_ylabel('Status Type')
        ax3.set_title('Different Statuses for races')

        fastestSpeeds = Driver_Data_2.get_driver_fastestlap_count(self.connections, self.driver_name)
        theBins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
        counts, bins, bars = ax4.hist(fastestSpeeds['fastestLap'], bins=theBins, edgecolor='black', color='gainsboro')
        ax4.plot(bins[:-1] + 1.5 / 2, counts, color='red')
        mean = fastestSpeeds['fastestLap'].mean()
        mode = fastestSpeeds['fastestLap'].mode().values[0]

        ax4.axvline(mean, color='green', linestyle='--', label="Mean")
        ax4.axvline(mode, color='blue', linestyle='--', label="Mode")

        ax4.set_xlabel('0 - 80 Lap (bins)')
        ax4.set_ylabel('Count of Fastest Lap')
        ax4.set_title('Frequency Distribution for Lap No.')
        ax4.legend()

        # ax4.tick_params(axis='y', labelrotation=50)
        # ax4.bar_label(s, label_type="center", color='white')

        canvas = FigureCanvasTkAgg(fig, master=self.canvasPanel)
        canvas_widget = canvas.get_tk_widget()

        canvas_widget.grid(row=3, column=0, sticky=N + S + E + W)

        canvas.draw()

    def loadRegression(self):
        self.Regression_ChildObj.show()
        # s = self.Regression_ChildObj.set_selected_driver(self.driver_name, self.connections)

        self.wait_variable(self.Regression_ChildObj.s_var)
        print("hi")

        fig, (ax1) = plt.subplots(1, 1, dpi=70)
        # Get the driver and constructors total points
        consPoints_driverPoints_relationship = Driver_Data_2.get_driver_constructor_points(self.connections,
                                                                                           self.driver_name)

        ax1.scatter(consPoints_driverPoints_relationship['constructor_points'],
                    consPoints_driverPoints_relationship['driver_points'], color='deepskyblue', marker='o')
        line = mlines.Line2D([0, 1], [0, 1], color='red')
        transform = ax1.transAxes
        line.set_transform(transform)
        ax1.add_line(line)

        ax1.set_xlabel('Constructor Points')
        ax1.set_ylabel('Driver Points')
        ax1.set_title('Relationship Constructor & Driver points (Top 15 wins)')
        ax1.grid(True, linestyle='--', alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=self.canvasPanel)
        canvas_widget = canvas.get_tk_widget()

        canvas_widget.grid(row=3, column=0, sticky=N + S + E + W)

        canvas.draw()


    def show(self):
        self.update()  # Update the window
        self.deiconify()  # Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide()  # Hide the window

    def hide(self):
        self.withdraw()  # Removes the window from the screen, without destroying it.
        self.buttonPanel.destroy()
        self.canvasPanel.destroy()
        self.root.show()
