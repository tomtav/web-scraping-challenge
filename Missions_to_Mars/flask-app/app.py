# import dependencies
import os
import numpy as np
import pandas as pd
import pymongo
from datetime import datetime, timedelta
from scrape_mars import scrape

from flask import (
    Flask, flash, jsonify, render_template, send_from_directory, url_for
)


def create_app():

    # Connect to database
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Declare the database
    db = client.mars_db

    # Declare the collection
    collection = db.news

    app = Flask(__name__, instance_relative_config=True)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route('/', methods=['GET'])
    def home():
        """Home Page"""
        try:
            document = collection.find({}).sort(
                "modified", pymongo.DESCENDING).limit(1)[0]
        except:
            document = {}

        return render_template('index.html', data=document)

    @app.route('/scrape', methods=['GET'])
    def run_scrape():
        """Scrape Mars Data from the Internet"""
        document = scrape()
        collection.insert_one(document)
        del document["_id"]
        return document

    return app
