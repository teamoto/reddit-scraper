import pymongo
import datetime


# connect a mongo db
def connect_mongodb(dbhost, dbport, dbname, dbuser, dbpass):
    con = pymongo.MongoClient(dbhost, dbport, retryWrites=False)
    db = con[dbname]
    try:
        db.authenticate(dbuser, dbpass)
        return db
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def insert_document(collection, data):
    try:
        collection.insert_one(data)
        return True
    except Exception as e:
        print("An exception occurred ::", e)
        return False


def check_post(collection, url):
    # if the same url is NOT found, return true
    if not collection.find_one({'url': url}):
        return True
    return False
