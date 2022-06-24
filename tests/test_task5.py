""" Write your test for the task here"""
import json


# pylint: disable=redefined-outer-name, unused-argument


def test_task5(client):
    """Task 5 - Test that a city is deleted"""
    # first make sure that there are 5 cities
    response = client.get("/cities")
    cities = json.loads(response.data)
    assert len(cities) == 5
    assert response.status_code == 200
    # setup the headers for the request
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    # get the last city in the list
    get_last_city_added = cities[-1]
    # get the id
    city_id = get_last_city_added["id"]
    # create the url
    url = f"/cities/{city_id}"
    # make the request
    response = client.delete(url, headers=headers)
    # check the status code
    assert response.status_code == 204
    # make another request to check how many cities are there now
    response = client.get("/cities")
    city = json.loads(response.data)
    # check the number of results
    assert len(city) == 4
