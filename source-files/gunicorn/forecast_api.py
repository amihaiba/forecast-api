# Worksheet   : Python Weather Project
# Author      : Amihai Ben-Arush
# Code review :
# Description : A Flask program which uses a weather and geocoding API to return the weather forecast
#             : of the next 7 days in a given location
import logging
from flask import Flask, render_template, request, redirect
import boto3
from botocore.exceptions import ClientError
from datetime import date, timedelta
import requests
app = Flask(__name__)

time_now = None
status = 0
location = ""
country = ""
forecast = []


def get_coords(input_location):
    """Get the location coordinates, as well as the country name and matched location"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": input_location, "count": 1}
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
    global time_now
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
    global status, location, country, forecast
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


@app.route("/download", methods=['GET'])
def download_file():
    s3 = boto3.client('s3',
                      aws_access_key_id='AKIAUEZE5XNIEIYV36NK',
                      aws_secret_access_key='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'
                      )
    try:
        url = s3.generate_presigned_url(ClientMethod='get_object',
                                        Params={'Bucket': 'www.amihaiba-website.co.il',
                                                'Key': 'fluffy-cloud-clipart.jpeg',
                                                'ResponseContentDisposition': 'attachment'
                                                },
                                        ExpiresIn=60
                                        )
        print(url)
        return redirect(url)
    except ClientError as e:
        logging.error(e)
        return None


@app.route('/dynamodb', methods=['GET'])
def insert_to_db():
    global status, country, location, forecast, time_now
    dynamodb = boto3.resource('dynamodb',)
    table = dynamodb.Table('forecast_api-entries')
    table.put_item(
        Item={
            'Location': str(location),
            'Date': str(time_now),
            'Forecast': str(forecast)
        }
    )

    title = location + ', ' + country + ' | ' + time_now.strftime("%A, %-d/%-m")
    return render_template("index.html",
                           status=status,
                           title=title,
                           forecast=forecast
                           )


if __name__ == "__main__":
    app.run(debug=True)
