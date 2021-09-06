from flask import Flask, jsonify, make_response, request, Response
import pymysql

db = pymysql.connect("localhost", "editor", "editor", "library")
app = Flask(__name__)

p_key = dict()
p_key["carti"] = "carte_id"
p_key["autori"] = "autor_id"


@app.errorhandler(404)
def not_found_response(err):
    response = dict()
    response["error"] = "resource not found"
    response["initial_data"] = str(err)
    return (jsonify(response), 404)


@app.route('/api/library', methods=['GET'])
def showTables():
    cursor = db.cursor()
    sql = "show tables"
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        return make_response(jsonify(result), 200)
    else:
        response = dict()
        response['err_msg'] = "Tables not found"
        return make_response(jsonify(response), 404)


@app.route('/api/library/<tabel>', methods=['Get'])
def showTable(tabel: str):
    cursor = db.cursor()
    try:
        sql = "select * from {}".format(tabel)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            return make_response(jsonify(result), 200)
    except:
        response = dict()
        response['err_msg'] = "Table not found"
        return make_response(jsonify(response), 404)


@app.route('/api/library/autori/nume/<nume>', methods=['GET'])
def gedIdAuthorByName(nume: str):
    response = dict()
    try:
        cursor = db.cursor()
        sql = "select autor_id from autori where nume = '{}'".format(nume)
        cursor.execute(sql)
        id = cursor.fetchall()[0][0]
        response["id"] = id
        return make_response(jsonify(response), 200)
    except:
        response["id"] = "Not found"
        return make_response(jsonify(response), 200)


@app.route('/api/library/cartiAutori/<id>', methods=['GET'])
def showAutorsBybooks(id: str):
    try:
        autori = []
        response = dict()
        cursor = db.cursor()
        sql = 'select autor_id from cartiAutori where carte_id = {}'.format(int(id))
        cursor.execute(sql)
        rez = cursor.fetchall()
        for r in rez:
            autori.append(r)
        response['message'] = "OK"
        response['autor_id'] = autori
        return make_response(jsonify(response), 200)
    except:
        response = dict()
        response['message'] = "Not found"
        return make_response(jsonify(response), 404)


@app.route('/api/library/<tabel>/<id>', methods=['GET'])
def showRowTable(tabel: str, id: str):
    try:
        cursor = db.cursor()
        sql = "select * from {} where {} = {}".format(tabel, int(id), p_key[tabel])
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            return make_response(jsonify(result), 200)
    except:
        response = dict()
        response['err_msg'] = "Not found"
        return make_response(jsonify(response), 404)


@app.route('/api/library/<tabel>', methods=['POST'])
def insertIntoTable(tabel: str):
    try:
        cursor = db.cursor()
        response = dict()
        headers = dict()

        if tabel == "cartiAutori":
            sql = "insert into cartiAutori (autor_id, carte_id) values ({}, {})".format(int(request.args['autor']),
                                                                                        int(request.args['carte']))
            cursor.execute(sql)
        elif tabel == "carti":
            sql = "insert into {} (nume, gen, an_aparitie, rezumat, editor) values('{}', '{}', {}, '{}', '{}')". \
                format(tabel, request.args['nume'], request.args['gen'], int(request.args['an_aparitie']),
                       request.args['rezumat'], request.args['editor'])
            cursor.execute(sql)

        elif tabel == "autori":
            sql = "insert into autori (nume, an_nastere) values ('{}', {})". \
                format(request.args['nume'], int(request.args['an_nastere']))
            cursor.execute(sql)

        if tabel != "cartiAutori":
            sql = "select {} from {} where nume = '{}'".format(p_key[tabel], tabel, request.args['nume'])
            cursor.execute(sql)
            id = cursor.fetchone()[0]

            response['id'] = id
            headers['location'] = '/api/library/{}/{}'.format(tabel, id)
            response["headers"] = headers
            print(id)
        response['status_code'] = 201
        response['message'] = "Created"
        return make_response(jsonify(response), 201)
    except:
        print("una 2 3 ")
        response = dict()
        response['err_msg'] = "Table not found"
        return make_response(jsonify(response), 404)


@app.route('/api/library/<tabel>/<id>', methods=['PUT'])
def updateIntoTable(tabel: str, id: str):
    try:
        response = Response()

        cursor = db.cursor()
        sql = "update {} set {} = '{}' where {} = {}".format(tabel, request.args['coloana'], request.args['nume'],
                                                             p_key[tabel], int(id))
        cursor.execute(sql)
        response.headers['location'] = "/api/library/{}/{}".format(tabel, id)

        return make_response(response, 200)
    except:
        response = dict()
        response['err_msg'] = "Table not found"
        return make_response(jsonify(response), 404)


@app.route('/api/library/<tabel>/<id>', methods=['DELETE'])
def delteRowInTable(tabel: str, id: str):
    try:
        cursor = db.cursor()
        sql = "delete from {} where {} = {}".format(tabel, p_key[tabel], int(id))
        cursor.execute(sql)
        return make_response(jsonify("No content"), 204)
    except:
        response = dict()
        response['err_msg'] = "Table not found"
        return make_response(jsonify(response), 404)


app.run(port=5013)
