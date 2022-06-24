"""This is the app for introduction to Flask"""
import os

import pandas as pd
from flask import Flask
from flask_restx import Resource, Api, fields
from werkzeug.middleware.proxy_fix import ProxyFix

from app import logging_config
from app.config import Config


def create_app(test_config=None):
    logging_config.logging_setup()  # create and configure the app
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    api = Api(version='1.0', default='Cities', default_label='Cities API', title='World Cities AP',
              description='A simple API for World Cities',
              )

    app.config.from_mapping(
        SECRET_KEY='dev',
        debug=True
    )
    api.init_app(app)

    ns = api.namespace('cities', description='City Operations')

    city = api.model('City', {
        'id': fields.Integer(readonly=True, description='The Unique City Identifier'),
        'city': fields.String(required=True, description='The City Name')
    })

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    class CitiesDAO(object):
        def __init__(self):
            self.counter = 0
            self.cities = []

        def get(self, id):
            for city in self.cities:
                if city['id'] == id:
                    return city
            api.abort(400, "Cities {} doesn't exist".format(id))

        def create(self, data):
            city = data
            city['id'] = self.counter = self.counter + 1
            self.cities.append(city)
            return city

        def update(self, id, data):
            city = self.get(id)
            city.update(data)
            return city

        def delete(self, id):
            city = self.get(id)
            self.cities.remove(city)

    cities_dao = CitiesDAO()

    df = pd.read_csv(os.path.join(Config.BASE_DIR, '..', 'data', 'worldcities.csv'), nrows=5)
    for index, row in df.iterrows():
        cities_dao.create({'city': row['city_ascii']})

    # a simple page that lists cities
    @api.route('/cities')
    @ns.doc('cities api')
    class Cities(Resource):
        """Shows a list of all cities, and lets you POST to add new tasks"""

        @ns.marshal_list_with(city)
        def get(self):
            """List all cities"""
            return cities_dao.cities

        @ns.doc('create_city')
        @ns.expect(city)
        @ns.marshal_with(city, code=201)
        def post(self):
            """Create a new city"""
            return cities_dao.create(api.payload), 200

        @ns.route('/<int:id>')
        @ns.response(404, 'City not found')
        @ns.param('id', 'The city identifier')
        class City(Resource):
            """Show a single city item and lets you delete them"""

            @ns.doc('get_city')
            @ns.marshal_with(city)
            def get(self, id):
                """Fetch a given resource"""
                return cities_dao.get(id)

            @ns.doc('delete_city')
            @ns.response(204, 'City deleted')
            def delete(self, id):
                """Delete a task given its identifier"""
                cities_dao.delete(id)
                return '', 200

            @ns.expect(city)
            @ns.marshal_with(city)
            def put(self, id):
                """Update a task given its identifier"""
                return cities_dao.update(id, api.payload)

    return app
