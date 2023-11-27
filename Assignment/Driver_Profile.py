import io
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font
import webbrowser
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_driver_url(driver_name, connection):
    query_drivers_names = "SELECT * FROM drivers WHERE CONCAT(forename, ' ', surname) = '{0}'".format(driver_name)
    df_mysql = pd.read_sql(query_drivers_names, con=connection)
    print(driver_name)
    print(df_mysql)
    driver_info = df_mysql['url'][0]
    return driver_info


def get_driver_image(driver_info):
    response = requests.get(driver_info)
    # Getting html content of the page using beatifulsoup
    soup = BeautifulSoup(response.text, 'html.parser')

    infobox = soup.find("table", class_="infobox")

    # Find the image element within the infobox
    if infobox:
        image_element = infobox.find("img")

        if image_element:
            image_url = "https:" + image_element.get("src")

            try:
                # Download the image
                image_response = requests.get(image_url)

                # Create a PIL Image from the image data
                pil_image = Image.open(io.BytesIO(image_response.content))
                return pil_image

            except requests.exceptions.HTTPError:
                print("HTTP error when fetching the image.")


            except Exception as e:
                print("An error occurred while processing the image:", e)

        else:
            print("Image not found in the infobox.")

    else:
        print("Infobox not found on the page.")
