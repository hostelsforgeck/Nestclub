import os
from datetime import datetime

from pymongo import errors
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

from flask import jsonify



uri = os.environ.get('MONGODB_URI')

# IF YOU CHANGE THIS VAR CHANGE THE NUMBER SPECIFIED IN "success.html" [elif == -2 { VAR DAYS } ] 
NO_OF_REQUESTS_PER_DAY = 5  # no of requests a person can make in a day.     


def save_user_request(document):
    client = None
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client['db1']
        collection = db['user_db']

        # Check if the user has already made 5 requests for the given day
        num_requests_today = collection.count_documents({
            "user_ph": document["user_ph"],
            "requested_date": document["requested_date"],
        })

        if num_requests_today >= NO_OF_REQUESTS_PER_DAY:
            return -2  # User has exceeded the limit of 5 requests per day

        # Check if the document already exists for the same phone number and hostel_id on the same day
        existing_doc = collection.find_one({
            "user_ph": document["user_ph"],
            "hostel_id": document["hostel_id"],
            "requested_date": document["requested_date"],
        })

        if existing_doc:
            return -1  # Document already exists

        # Insert the new document
        collection.insert_one(document)
        return 1

    except PyMongoError as e:
        print(f"PyMongo error occurred: {e}")
        return 0  # Return 0 to indicate failure due to PyMongo error

    except Exception as e:
        print(f"Error occurred: {e}")
        return 0  # Return 0 to indicate general failure

    finally:
        if client:
            client.close()














