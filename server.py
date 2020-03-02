from flask import Flask,jsonify,request, Response
from flask import render_template
from store.config import PORT_SERVICE
from store import user, message
from store.models import ResponseTemplate
app = Flask(__name__)




@app.route("/")
def hello():
        return "Backend Messenger"





@app.route("/api/login",methods=["POST"])
def api_login():
    responseHttp = ResponseTemplate()
    try:

        email = request.json['email']
        password = request.json['password']
        responseHttp = user.user_login(email, password)


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

        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = user.user_logout(token)
    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data =[]

    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# list_user
@app.route("/api/user/list",methods=["GET"])
def list_user():
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

        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            responseHttp.data = []
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = user.list_user(page, limit, search)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# view_user
@app.route("/api/user/<id>", methods=["GET"])
def view_user(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']

        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = user.view_user(id)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')








# create_user
@app.route("/api/user",methods=["POST"])
def create_user():
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']
        email = request.json['email']
        nama = request.json['nama']
        alamat = request.json['alamat']


        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = user.create_user(nama, email, alamat)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = {}
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# delete_user
@app.route("/api/user/<id>", methods=["DELETE"])
def delete_user(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']

        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = user.delete_user(id)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')






# update_user
@app.route("/api/user/<id>",methods=["PUT"])
def update_user(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']
        email = request.json['email']
        nama = request.json['nama']
        alamat = request.json['alamat']

        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')
        responseHttp = user.update_user(id, nama, email, alamat)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')






#list_message
@app.route("/api/message/list",methods=["GET"])
def list_message():
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
        
        receiver = request.args.get('receiver', default='', type=str)
        userVerified = cek_user_token2('token')

        if (userVerified.permit == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            responseHttp.data = []
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        sender = userVerified.id
        
        responseHttp = message.list_message(page, limit, search, sender, receiver)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')



#create_message
@app.route("/api/message",methods=["POST"])
def create_message():
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']
        status = 1
        content = request.json['content']

        receiver = request.json['receiver']
        
        type = request.json['type']
        userVerified = cek_user_token2(token)

        if (userVerified.permit == False):
            responseHttp.code = 403
            responseHttp.message = "Forbidden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')
        
        sender = userVerified(id)
        
        responseHttp = message.create_message(status, content, type, sender, receiver)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = {}
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







# delete_message
@app.route("/api/message/<id>", methods=["DELETE"])
def delete_message(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']

        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbiden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')

        responseHttp = message.delete_message(id)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')






# update_message
@app.route("/api/message/<id>",methods=["PUT"])
def update_message(id):
    responseHttp = ResponseTemplate()
    try:
        token = request.headers['token']
        status = request.json['status']
        
        if (user.cek_user_token(token) == False):
            responseHttp.code = 403
            responseHttp.message = "Forbidden"
            return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')
        responseHttp = message.update_message(id, status)

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return Response(responseHttp.toJSON(), status=responseHttp.code, mimetype='application/json')







#menjalankan service nya backend, LISTEN di Port berapa, gerbang inputan siap menerima perintah
if __name__ == "__main__":
    app.run("0.0.0.0", port=PORT_SERVICE, debug=True)
