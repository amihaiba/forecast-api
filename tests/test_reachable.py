import pytest
import requests


def test_reachable():
    response = requests.get('https://localhost', verify=False)
    assert 200 <= response.status_code <= 299


if __name__ == '__main__':
    pass
