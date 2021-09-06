from flask import Flask, jsonify, make_response, request, Response
from pip._vendor import requests

app = Flask(__name__)


@app.errorhandler(404)
def not_found_response(err):
    response = dict()
    response["error"] = "resource not found"
    response["initial_data"] = str(err)
    return (jsonify(response), 404)


@app.route('/api/bookcollection/book/<id>', methods=['Get'])
def infoBook(id):
    try:
        carte = ["id", "nume", "gen", "an", "rezumat", "editia"]
        response = dict()
        name_autori = []
        id_autor = requests.get("http://127.0.0.1:5013/api/library/cartiAutori/{}".format(int(id))).json()
        print(id_autor)
        for i in id_autor['autor_id']:
            name_autori.append(
                requests.get("http://127.0.0.1:5013/api/library/autori/{}".format(int(i[0]))).json()[0][1])
            print(name_autori)
        informatii = (requests.get("http://127.0.0.1:5013/api/library/carti/{}".format(int(id))).json())
        for i in range(0, len(carte) - 1):
            response[carte[i]] = informatii[0][i]
        response["lista autori"] = name_autori

        return make_response(jsonify(response), 200)
    except:
        response = dict()
        response['err_msg'] = "Table not found"
        return make_response(jsonify(response), 404)


@app.route('/api/bookcollection', methods=['POST'])
def addBook():
    try:
        id_carte = requests.post(
            "http://127.0.0.1:5013/api/library/carti?nume={}&gen={}&an_aparitie={}&rezumat={}&editor={}".
                format(request.args["nume"], request.args["gen"], request.args["an_aparitie"], request.args["rezumat"],
                       request.args["editor"])).json()
        print("carte " + str(id_carte['id']))
        # for i in range(0, len(request.args["autori"]) - 1):
        #     print(request.args["autori"][i])
        id_autor = requests.get("http://127.0.0.1:5013/api/library/autori/nume/{}".format(request.args["autori"])).json()
        print("autor " + str(id_autor["id"]))
        if id_autor["id"] == "Not found":
            id_autor = requests.post(
                "http://127.0.0.1:5013/api/library/autori?nume={}&an_nastere={}".format(request.args["autori"],
                                                                                        request.args["an_nastere"]
                                                                                        )).json()
            print("autor not found" + str(id_autor["id"]))
        print(requests.post("http://127.0.0.1:5013/api/library/cartiAutori?autor={}&carte={}".format(id_autor["id"],
                                                                                                     id_carte[
                                                                                                         "id"])).json())

        return make_response(jsonify("Created"), 201)
    except:
        return make_response(jsonify("Not found"), 404)


app.run(port=5014)
