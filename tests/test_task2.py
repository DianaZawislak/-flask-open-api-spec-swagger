""" Make the tests pass to make the cities endpoint work"""
# pylint: disable=redefined-outer-name, unused-argument, line-too-long
import json


def test_task_2(client):
    """Task 2 - Test that cities/<id> retrieves one city and that city is Tokyo and that the status code is 200 or a
    404 if not found """
    # requests the first city
    response = client.get("/cities/1")
    # loads the Json string to a python dict
    city = json.loads(response.data)
    # checks the name of th city
    assert city["city"] == 'Tokyo'
    # checks that the status code is 200 for a successful request
    assert response.status_code == 200

    # requests the first city
    response = client.get("/cities/9")
    # loads the Json string to a python dict
    city = json.loads(response.data)
    # checks the name of th city
    # checks that the status code is 404 not found
    assert response.status_code == 404
