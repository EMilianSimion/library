from config import connectMongoWorker
from flask import Flask, make_response, jsonify, request


mConfigDataReadWrite = {'dbhost':'localhost', 'dbport':27017, 'dbuser':'readWrite', 'dbpasswd':'readWritePass', 'dbname':'admin'}
db = connectMongoWorker(mConfigDataReadWrite)

app = Flask(__name__)

@app.errorhandler(404)
def not_found_resourse(err):
    response = dict()
    response['error'] = 'resource not found'
    response['initial_data'] = str(err)
    return(jsonify(response), 404)

@app.route('/api/biblioteca', methods = ['GET'])
def showCollections():
    collections_fetched = db["biblioteca"].list_collection_names()
    if collections_fetched:
        return make_response(jsonify(collections_fetched), 200)
    else:
        #No records are found
        result = dict()
        result['err_msg'] = "Collections not found"
        return make_response(jsonify(result), 404)
@app.route('/api/biblioteca/<colectie>', methods = ['GET'])
def showDocuments(colectie : str):
    if colectie in db["biblioteca"].list_collection_names():
        documents_fetched = db.biblioteca[colectie].find()
        doc = []
        for x in documents_fetched:
            doc.append(x['nume'])
        if doc:
            return make_response(jsonify(doc), 200)
    #No recors are found
    result = dict()
    result['err_msg'] = "Documents not found"
    return make_response(jsonify(result), 404)
@app.route('/api/biblioteca/<colectie>/<idDoc>', methods = ['GET'])
def showDocumentId(colectie : str, idDoc:str):
    if colectie in db["biblioteca"].list_collection_names():
        doc = db["biblioteca"][colectie].find({"_id":int(idDoc)}, {"_id": 0, "nume":1})
        list = []
        for elem in doc:
            list.append(elem)
        if list:
            return make_response(jsonify( list), 200)
    result = dict()
    result['err_msg'] = "Document not found"
    return make_response(jsonify(result), 404)

@app.route('/api/biblioteca/<colectie>', methods = ['POST'])
def addCollections(colectie:str):
    if colectie in db["biblioteca"].list_collection_names():
        doc ={"nume": request.args['numeCarte']}
        x = db["biblioteca"][colectie].insert_one(doc)
        return make_response(jsonify("Created"+str(x)), 201)
    result = dict()
    result['err_msg'] = 'Colection not found'
    return make_response(jsonify(result), 404) #not found

@app.route('/api/biblioteca/<colectie>/<doc_id>', methods = ['PUT'])
def updateCollections(colectie:str, doc_id:str):
    if colectie in db["biblioteca"].list_collection_names():
        for entry in db["biblioteca"][colectie].find():
            if entry['_id'] == int(doc_id):
                db["biblioteca"][colectie].delete_one(entry)
        doc = dict ()
        doc["_id"] = int(doc_id)
        doc["nume"] = request.args['numeCarte']
        db["biblioteca"][colectie].insert_one(doc)
        return make_response(jsonify("No Content"), 204)

    result = dict ()
    result['err_msg'] = 'data not found'
    return make_response(jsonify(result), 404)

@app.route('/api/biblioteca/<colectie>/<doc_id>', methods = ['DELETE'])
def deleteDocument(colectie : str, doc_id:str):
    if colectie in db["biblioteca"].list_collection_names():
        for entry in db["biblioteca"][colectie].find():
            if entry['_id'] == int(doc_id):
                db["biblioteca"][colectie].delete_one(entry)
        return make_response(jsonify("No Content"), 204)
    result = dict()
    result['err_msg'] = 'data not found'
    return make_response(jsonify(result), 404)


app.run(port = 5013)

