""" Make the tests pass to make the cities endpoint work"""
# pylint: disable=redefined-outer-name, unused-argument,line-too-long
import json


def test_task3(client):
    """Task 3 - Tests that a post to cities inserts a record into the API's data access object"""
    # requests to cities to find that there are 5 cities as expected and the response code is 200
    response = client.get("/cities")
    city = json.loads(response.data)
    assert len(city) == 5
    assert response.status_code == 200
    # sets the MIME Type to json in the HTTP Request header, so the service knows how to read the data being sent
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # prepares the dictionary to be sent
    data = {
        'city': "Pittsburgh",
    }
    # sets the URL
    url = '/cities'
    # makes the post request and converts the python object/dict to string
    response = client.post(url, data=json.dumps(data), headers=headers)
    # converts the API response to python dictionary

    created_city = json.loads(response.data)
    # checks the response type to make sure its json
    assert response.content_type == mimetype
    # checks that 201 is the status code for successful post request
    assert response.status_code == 201
    assert created_city['city'] == "Pittsburgh"
    # checking that there is one additional city in the API
    response = client.get("/cities")
    city = json.loads(response.data)
    assert len(city) == 6
    assert response.status_code == 200
