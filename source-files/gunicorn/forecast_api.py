# Worksheet   : Python Weather Project
# Author      : Amihai Ben-Arush
# Code review :
# Description : A Flask program which uses a weather and geocoding API to return the weather forecast
#             : of the next 7 days in a given location
from flask import Flask, render_template, request
from datetime import date, timedelta
import requests
app = Flask(__name__)
forecast_dict = {}


def get_coords(location):
    """Get the location coordinates, aswell as the country name and matched location"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location, "count": 1}
    data = requests.get(url, params)
    if data.status_code == 200 and "results" in data.text:
        data = data.json()
        return 1,\
            data['results'][0]['name'],\
            data['results'][0]['country'],\
            data["results"][0]['latitude'],\
            data["results"][0]['longitude']
    return 0, None, None, None, None


def get_forecast(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    time_now = date.today()
    params = {"latitude": lat,
              "longitude": lon,
              "daily": ["temperature_2m_max", "temperature_2m_min"],
              "timezone": "auto",
              "temperature_unit": "celsius",
              "start_date": time_now,
              "end_date": time_now + timedelta(7)
              }
    return time_now.strftime("%A, %-d/%-m"), requests.get(url, params).json()['daily']


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html", status=-1)
    elif request.method == 'POST':
        status, location, country, latitude, longitude = get_coords(request.form['location'])
        if status == 1:
            today, forecast = get_forecast(latitude, longitude)
            title = location + ', ' + country + ' | ' + today
        else:
            title = ""
            forecast = None
        return render_template("index.html",
                               status=status,
                               title=title,
                               forecast=forecast
                               )


if __name__ == "__main__":
    app.run(debug=True)

