""" Make the tests pass to make the cities endpoint work"""
# pylint: disable=redefined-outer-name, unused-argument, line-too-long
import json


def test_task4(client):
    """Task 4 - Tests that a post to cities updates a city record"""
    # get a city to update
    response = client.get("/cities/1")
    city = json.loads(response.data)
    # make sure its tokyo
    assert city["city"] == 'Tokyo'
    # check the status code
    assert response.status_code == 200
    # set the mimetype for the update
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # setup the update data
    data = {
        'city': "Pittsburgh",
    }
    # setup the endpoint url for the put request
    url = '/cities/1'
    # make the put request
    response = client.put(url, data=json.dumps(data), headers=headers)
    # get the updated data and check that it updated record 1 to pittsburgh and returns the correct response code 200
    updated_city = json.loads(response.data)
    assert response.content_type == mimetype
    # check that the API returns the updated data and that it is corrrect
    assert updated_city['city'] == "Pittsburgh"
    # status code for a successful put request
    assert response.status_code == 200
    # check that we still have 5 cities and that we didn't accidently create a new record
    response = client.get("/cities")
    city = json.loads(response.data)
    assert len(city) == 5
    assert response.status_code == 200
