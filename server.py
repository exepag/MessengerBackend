from flask import Flask,jsonify,request, Response
from flask import render_template
from store.config import PORT_SERVICE
from store import nasabah
from store.models import ResponseTemplate
app = Flask(__name__)




@app.route("/")
def hello():
        return "Backend Messenger"





@app.route("/api/login",methods=["POST"])
def api_login():
    responseHttp = ResponseTemplate()
    try:

        user = request.json['email']
        password = request.json['password']
        responseHttp = user.user_login(user, password)


    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data =[]

    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')






@app.route("/api/logout",methods=["POST"])
def api_logout():
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']

        if (nasabah.cek_nasabah_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = nasabah.nasabah_logout(token)
    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data =[]

    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# list_nasabah
@app.route("/api/nasabah/list",methods=["GET"])
def list_nasabah():
    responseHttp = ResponseTemplate()
    try:
        if 'token' not in request.headers:
            print('halo')
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            responseHttp.data = []
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')
        token = request.headers['token']
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)
        search = request.args.get('search', default='', type=str)

        if (nasabah.cek_nasabah_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            responseHttp.data = []
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = nasabah.list_nasabah(page, limit, search)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# view_nasabah
@app.route("/api/nasabah/<id>", methods=["GET"])
def view_nasabah(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']

        if (nasabah.cek_nasabah_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = nasabah.view_nasabah(id)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')








# create_nasabah
@app.route("/api/nasabah",methods=["POST"])
def create_nasabah():
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']
        email = request.json['email']
        nama = request.json['nama']
        alamat = request.json['alamat']


        if (nasabah.cek_nasabah_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = nasabah.create_nasabah(nama, email, alamat)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = {}
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# delete_nasabah
@app.route("/api/nasabah/<id>", methods=["DELETE"])
def delete_nasabah(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']

        if (nasabah.cek_nasabah_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = nasabah.delete_nasabah(id)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')






# update_nasabah
@app.route("/api/nasabah/<id>",methods=["PUT"])
def update_nasabah(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']
        email = request.json['email']
        nama = request.json['nama']
        alamat = request.json['alamat']
        #saldo = request.json['saldo']

        if (nasabah.cek_nasabah_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')
        responseHttp = nasabah.update_nasabah(id, nama, email, alamat)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')




if __name__ == "__main__":
    app.run("0.0.0.0", port=PORT_SERVICE, debug=True)
