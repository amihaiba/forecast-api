# Worksheet   : 
# Author      : Amihai Ben-Arush
# Description : Determine if the web app is up and running by sending a request and getting a 2xx status code
import pytest
import requests


def test_reachable():
    # response = requests.get('https://localhost', verify=False)
    response = requests.get('http://localhost')
    assert 200 <= response.status_code <= 299


if __name__ == '__main__':
    pass
