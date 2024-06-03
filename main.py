# If you want to run the code, please contact me to ask for the API Key. Email: profissional.drey@gmail.com or andrey.estevamseabra@richmond.edu

import datetime as dt
import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

base_url = "http://api.openweathermap.org/data/2.5/weather?"

def k_to_c_f(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit


def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    temp_kelvin, feels_like_kelvin, description, wind_speed, icon_url, city, country, temp_celsius, temp_fahrenheit, feels_like_celsius, feels_like_fahrenheit, wind_speed, humidity, sunrise_time, sunset_time = result
    location_label.configure(text=f"{city}, {country}")

    # Load the weather icon!
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temp_kelvin:.2f}K, {temp_celsius:.2f}ºC, {temp_fahrenheit:.2f}ºF")
    description_label.configure(text=f"Description: {description}")


def get_weather(city):
    api_key = "" # If you want to run the code, please contact me to ask for the API Key. Email: profissional.drey@gmail.com or andrey.estevamseabra@richmond.edu
    url = base_url + "q=" + city + "&APPID=" + api_key
    response = requests.get(url).json()
    
    if response['cod'] == '404':
        messagebox.showerror("Error", "City not found")
        return None
    
    temp_kelvin = response['main']['temp']
    feels_like_kelvin = response['main']['feels_like']
    description = response['weather'][0]['description']
    wind_speed = response['wind']['speed']
    icon_id = response['weather'][0]['icon']
    city = response['name']
    country = response['sys']['country']
    temp_celsius, temp_fahrenheit = k_to_c_f(temp_kelvin)
    feels_like_celsius, feels_like_fahrenheit = k_to_c_f(feels_like_kelvin)
    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])

    icon_url = "https://openweathermap.org/img/wn/" + icon_id + "@2x.png"
    return (temp_kelvin, feels_like_kelvin, description, wind_speed, icon_url, city, country, temp_celsius, temp_fahrenheit, feels_like_celsius, feels_like_fahrenheit, wind_speed, humidity, sunrise_time, sunset_time)






if __name__ == '__main__':
    root = ttkbootstrap.Window(themename="morph")
    root.title("Weather App")
    root.geometry("400x400")

    #City name
    city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
    city_entry.pack(pady=10)

    # Widgets below:

    # To search about the weather info!
    search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
    search_button.pack(pady=10)

    # To show the city/country
    location_label = tk.Label(root, font="Helvetica, 25")
    location_label.pack(pady=20)

    # Weather icon widget
    icon_label = tk.Label(root)
    icon_label.pack()

    # Temperature label widget!
    temperature_label = tk.Label(root, font="Helvetica, 20")
    temperature_label.pack()

    # Weather description widget!
    description_label = tk.Label(root, font="Helvetica, 20")
    description_label.pack()

    root.mainloop()
