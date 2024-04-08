# Reference
# https://open-meteo.com/en/docs
# https://anaconda.org/
# https://code.visualstudio.com/docs/python/environments 
# https://kanoki.org/python-plotting-latitude-and-longitude-from-csv-on-map-using-basemap-folium-geopandas-and-plotly 
# https://www.askpython.com/python/examples/gui-weather-app-in-python


# import required modules
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pytz
import requests,json
from functools import partial
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import *
import pandas as pd

# Initialize Window
root = Tk()
root.geometry("600x400+300+200")
root.resizable(False, False)
root.title("Weather App")

# Create geolocator instance
geolocator = Nominatim(user_agent="weather_app")

# Function to fetch weather data
def getWeather():
    city = textfield.get()
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I: %M %p")
    clock.config(text=current_time)
    name.config(text=f" WEATHER IN {city.upper()}")

    # API call to fetch weather data
    api = f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,soil_temperature_0cm,uv_index,is_day&daily=uv_index_max&timezone=auto"
    json_data = requests.get(api).json()

    # Extract current weather data
    temp = int(json_data['current']['temperature_2m'])
    condition = int(json_data['current']['apparent_temperature'])
    wind = int(json_data['current']['wind_speed_10m'])
    humidity = json_data['current']['relative_humidity_2m']
    precipitation = int(json_data['current']['precipitation'])
   # hourly_data = json_data.get('hourly', {}).get('temperature_2m', [])
    
    # Update GUI with current weather data
    t.config(text=f"{temp}°C")
    c.config(text=f"FEELS LIKE {condition}°C")
  #  ht.config(text=f"Hourly \n Temp in {city} :")
    w.config(text=(wind,"m/s"))
    h.config(text=(humidity,"%"))
    p.config(text=(precipitation,"%"))

    

# GUI setup
Search_image=PhotoImage(file="search.png")
myimage=Label (image=Search_image)
myimage.place (x=20, y=20)
textfield=tk.Entry(root, justify="center",width=17, font=("poppins", 25, "bold" ))
textfield.place(x=50,y=40)
textfield.focus()

Search_icon=PhotoImage(file="search_icon.png")
myimage_icon=Button (image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place (x=400,y=34)

# Logo
Logo_image=PhotoImage(file="logo.png")
logo=Label (image=Logo_image)
logo.place (x=260, y=130)

# Side box
Round_box=PhotoImage(file="SideBox.png")
Label(root,image=Round_box).place(x=20,y=240)

# Hourly temperature frame
#hourly_frame = Frame(root, width=100, height=680,  bg="#f7f6f6")
#hourly_frame.place(x=650, y=1)

# Time display
name=Label(root,font=("arial",15,"bold"))
name.place (x=30, y=100)
clock = Label(root,font=("Helvetica",20))
clock.place (x=30,y=130)

# Labels for weather information
label1=Label(root, text="WIND SPEED", font=("Helvetica", 10, 'bold'), fg="white" , bg="#00008B")
label1.place (x=25,y=250)

label2=Label(root, text="HUMIDITY", font=("Helvetica", 10, 'bold'), fg="white" , bg="#00008B")
label2.place(x=25,y=280)

label3=Label(root, text="PRECIPITATION", font=("Helvetica", 10, 'bold'), fg="white" , bg="#00008B")
label3.place(x=25,y=310)

# Labels for weather data
t=Label(font=("arial",40,"bold"),fg="#ee666d")
t.place(x=30, y=160)
c=Label(font=("arial",10,"bold"))
c.place(x=30, y=220)


w=Label(text="...",font=("arial",12,"bold"), fg="white" , bg="#00008B")
w.place (x=150, y=250)
h=Label(text="...",font=("arial",12,"bold"), fg="white" , bg="#00008B")
h.place (x=150, y=280)
p=Label(text="...",font=("arial",12,"bold"), fg="white" ,bg="#00008B")
p.place (x=150, y=310)

root.mainloop()
