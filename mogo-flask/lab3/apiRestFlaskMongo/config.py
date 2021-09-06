"""This module is to configure app to connect with database."""

from pymongo import MongoClient
import sys

def connectMongoWorker (mConfigData):
    dbclient = None
    try:
        dbclient = MongoClient(host = mConfigData['dbhost'],
                               port = mConfigData['dbport'],
                               username = mConfigData['dbuser'],
                               password = mConfigData['dbpasswd'],
                               authSource = mConfigData['dbname']
                               )
        print('[MONGODB_CONNECT] Listing collections for user 0: {}: 1: "{}'.format(mConfigData['dbuser'],
                                str(dbclient[mConfigData['dbname']].list_collection_names())))
        return dbclient
    except AttributeError as attr_error:
        print(attr_error)
        sys.exit(1)
    except Exception as generic_error:
        print(generic_error)
        sys.exit(1)