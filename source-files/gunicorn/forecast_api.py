# Project     : Python Weather Project
# Author      : Amihai Ben-Arush
# Code review :
# Description : A Flask program which uses a weather and geocoding API to return the weather forecast
#             : of the next 7 days in a given location
# Addition 1  : AWS Part 1 - allows users to download an image from our S3 storage and save forecast entries
#             : into our DynamoDB
# Addition 2  : Prometheus Monitoring - Add a metrics endpoint for Prometheus to scrape data from
#             : and add metrics to the app, such as visits, image downloads and cities searched
# Addition 3  : ELK Stack - Enable logging in an Elastic-search compatible format for ELK stack's Filebeat to collect
#             : and send to the ELK Stack
# Addition 4  : Kubernetes part 2 - Added a history section that collect previous searches in json format and allow to
#             : view and download said files.
# Addition 5  : Added env. variables that can change the app's color and path
import os
import json
import glob
from flask import Flask, render_template, request, redirect, Response
import boto3
from botocore.exceptions import ClientError
from datetime import date, timedelta
import requests
import prometheus_client
from prometheus_client import Counter
# from prometheus_client import Gauge, Histogram, Summary
import logging
import ecs_logging

app = Flask(__name__)

record = {"status": 0,
          "title": "",
          "location": "",
          "country": "",
          "forecast": None
          }
if os.environ.get("APP_PATH") is None:
    app_path = "forecast-api"
else:
    app_path = os.environ.get("APP_PATH")
if os.environ.get("BG_COLOR") is None:
    bg_color = "primary"
else:
    bg_color = os.environ.get("BG_COLOR")

# Prometheus' metrics collected as a dictionary
graphs = {'count_visits': Counter('app_visit_operations_total', 'Number of times app has been visited'),
          'count_images': Counter('images_download_request_total', 'Number of image download requests'),
          'count_cities': Counter('cities_searched_total', 'Number of times each city has been searched', ['city']),
          }
# ELK Stack
# Create a logger object
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
# Add ECS formatter to the Handler
handler = logging.FileHandler("forecast_api_log.json")
handler.setFormatter(ecs_logging.StdlibFormatter())
# Add handler to the logger
logger.addHandler(handler)
# Add a log entry of type 'info'
logger.info("Weather forecast app started!")


def get_coordinates(input_location):
    """Get the location coordinates, as well as the country name and matched location"""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": input_location, "count": 1}
    # Get altitude, longitude coordinates, as well as the name of the location and its country
    data = requests.get(url, params)
    # If request was not successful or without results return none
    if data.status_code != 200 or "results" not in data.text:
        logger.error("Coordinates error, probably bad location", extra={"data.status_code": data.status_code,
                                                                        "input_location": input_location})
        record["status"] = 0
        record["location"] = ""
        record["country"] = ""
        return {-1, -1}

    logger.info("Forecast search completed successfully", extra={"data.status_code": data.status_code,
                                                                 "input_location": input_location})
    # JSONify the data and return the relevant data
    data = data.json()
    record["status"] = 1
    record["location"] = data['results'][0]['name']
    record["country"] = data['results'][0]['country']
    return [data["results"][0]['latitude'], data["results"][0]['longitude']]


def get_forecast(location_coord):
    """Get forecast from OpenMeteo API by coordinates"""
    url = "https://api.open-meteo.com/v1/forecast"
    today = date.today()
    params = {"latitude": location_coord[0],
              "longitude": location_coord[1],
              "daily": ["temperature_2m_max", "temperature_2m_min"],
              "timezone": "auto",
              "temperature_unit": "celsius",
              "start_date": today,
              "end_date": today + timedelta(7)
              }
    # Return the daily part of the forecast JSONified along with a formatted date
    record["forecast"] = requests.get(url, params).json()['daily']


@app.route('/', methods=['GET', 'POST'])
def index():
    """Load web app and show results of forecast queries"""
    # When the website is first visited and no location search was done yet
    if request.method == 'GET':
        # Prometheus metric to track the number of times the web app has been visited
        graphs['count_visits'].inc()
        record["status"] = -1
        return render_template("index.html", record=record, BG_COLOR=bg_color, APP_PATH=app_path)
    elif request.method == 'POST':
        coordinates = get_coordinates(request.form['location'])
        if record["status"] == 1:
            get_forecast(coordinates)
            record["title"] = record["location"] + ', ' + record["country"] + \
                ' | ' + date.today().strftime("%A, %-d/%-m")
            with open(f"history/{record['location']}-{date.today()}.json", "a") as h:
                json_format = json.dumps(record)
                h.write(json_format)
            # Prometheus metric to track the number of times each city has been searched
            graphs['count_cities'].labels(record["location"]).inc()
        else:
            record["title"] = ""
            record["forecast"] = None
        # ELK Stack logging
        logger.info(f"Forecast request received", extra={"location": record["location"], "date": record["title"]})
        return render_template("index.html", record=record, BG_COLOR=bg_color, APP_PATH=app_path)


@app.route('/download', methods=['GET'])
def download_file():
    """Download an image stored in AWS S3"""
    # Prometheus metric to track the number of times an image has been attempted to be downloaded
    graphs['count_images'].inc()
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
        return redirect(url)
    except ClientError as e:
        # Log and error if the bucket couldn't be reached
        logging.error(e)
        return None


@app.route('/dynamodb', methods=['GET'])
def insert_to_db():
    """Insert a forecast entry into AWS DynamoDB"""
    global record
    dynamodb = boto3.resource('dynamodb',)
    table = dynamodb.Table('forecast_api-entries')
    table.put_item(
        Item={
            'Location': str(record["location"]),
            'Date': str(record["time_now"]),
            'Forecast': str(record["forecast"])
        }
    )
    # Return the same page with the current forecast
    return render_template("index.html", record=record, BG_COLOR=bg_color, APP_PATH=app_path)


# Metrics endpoint for Prometheus to collect data from
@app.route('/metrics')
def metrics():
    res = []
    for k, v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")


@app.route('/history')
def history():
    file_names = [file.split('/')[-1].split('.')[0] for file in glob.glob("history/*.json")]
    return render_template("history.html", file_names=file_names, BG_COLOR=bg_color, APP_PATH=app_path)


if __name__ == "__main__":
    app.run(debug=True)
