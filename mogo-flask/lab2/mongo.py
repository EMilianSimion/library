import sys

import jsonify as jsonify
import pymongo

def connectMongoWorker (mConfigData):
    dbclient = None
    try:
        dbclient = pymongo.MongoClient(host = mConfigData['dbhost'],
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

#main
dbclient = None
mConfigDataOwner = {'dbhost':'localhost', 'dbport':27017, 'dbuser':'dbOwner', 'dbpasswd':'dbOwnerPass', 'dbname':'admin'}
mConfigDataReadWrite = {'dbhost':'localhost', 'dbport':27017, 'dbuser':'readWrite', 'dbpasswd':'readWritePass', 'dbname':'admin'}

dbclient = connectMongoWorker(mConfigDataOwner)
mydb = dbclient["biblioteca"]
mycol = mydb ["cartiPreferate"]
cartiPreferate = [
    {"_id": 1, "nume":"John Peter"},
    {"_id": 2, "nume": "FIICE PERFECTE"},
    {"_id": 3, "nume": "CELE 5 LIMBAJE ALE SCUZELOR"}
]
cartiAsteptate = [
    {"_id": 4, "nume":"Hobbitul"},
    {"_id": 5, "nume":"Stapanul Inelelor"},
    {"_id": 6, "nume":"Piratii din caraibe"}
]
x = mycol.insert_many(cartiAsteptate)
docs = {"nume":"ana are mere"}
# y = mycol.insert_many(cartiAsteptate)
# print(str(x)+ "\n" + str(y))
# doc = []
# query = {"sql_id":1}
# # docc = mycol.find(query)
# # for x in docc:
# #     print(x)
# for x in mycol.find() :
#     if x['sql_id'] == 1:
#         x['nume'] = 'EMinou'
#     print(x)
for x in mycol.find() :
    print(x)
#_id