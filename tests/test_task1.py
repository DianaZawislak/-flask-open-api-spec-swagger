""" Make the tests pass to make the cities endpoint work"""
# pylint: disable=redefined-outer-name, unused-argument, line-too-long)
import json


def test_task_1(client):
    """Task 1 - Test that the home page loads the swagger UI and the API returns 5 cities and the first city is Tokyo"""
    # homepage loading with the swagger UI info displayed
    response = client.get("/")
    assert response.status_code == 200
    assert b'World Cities API' in response.data
    # checks that cities' endpoint returns 5 cities

    response = client.get("/cities")
    # converts the json string to a dictionary
    response_dict = json.loads(response.data)
    assert len(response_dict) == 5

    # checks that the first city is tokyo
    city = response_dict[0]
    assert city["city"] == 'Tokyo'
