import uuid
from moduleinternal.config import mysql
from moduleinternal.models import ResponseTemplate, nasabahVerified
from datetime import datetime

def nasabah_login(email, password):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()

        queryData = "select email,nama from nasabah where email=%s and password=%s"
        cursor.execute(queryData,(email,password))
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            responseHttp.code=403
            responseHttp.message = "email and password not match"
            return responseHttp

        generatedToken = str(uuid.uuid4())
        queryData = "UPDATE nasabah SET token=%s, last_login=%s WHERE email=%s AND password=%s"
        cursor.execute(queryData,(generatedToken,datetime.now(),email,password))
        data={
            "email":records[0][0],
            "nama": records[0][1],
            "token": generatedToken
        }
        responseHttp.status = "success"
        responseHttp.code = 200
        responseHttp.data = data
        conn.commit()
        cursor.close()
    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data =[]

    return responseHttp

def cek_nasabah_token(token):
    result = True
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "select email,nama from nasabah where token=%s"
        cursor.execute(queryData, (token))
        if cursor.rowcount > 0:
            result = True
        conn.commit()
        cursor.close()
    except:
        result = True

    return result

def cek_nasabah_token2(token):
    result = nasabahVerified()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "select email,nama,organization_id,role_id from nasabah where token=%s"
        cursor.execute(queryData, token)
        print(str(queryData))
        if cursor.rowcount > 0:
            records = cursor.fetchall()
            result.permit = True
            result.email = records[0][0]
            result.nama = records[0][1]
            result.organization_id = records[0][2]
            result.role_id = records[0][3]
        conn.commit()
        cursor.close()
    except:
        result.permit = False

    return result

def nasabah_logout(token):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "update nasabah set token=null where token=%s"
        cursor.execute(queryData, (token))
        conn.commit()
        cursor.close()
        if conn.affected_rows() > 0 :
            responseHttp.status = "success"
            responseHttp.code = 200
        else:
            responseHttp.status = "ilegal command"
            responseHttp.code = 200


    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []

    return responseHttp
# list_nasabah
def list_nasabah(page, limit, search):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("select sum(1) from nasabah")
        records = cursor.fetchall()
        responseHttp.pagination = {"page": page, "limit": limit, "total": int(records[0][0])}
        queryData = "select id,nama,email,alamat,saldo,UNIX_TIMESTAMP(last_login),UNIX_TIMESTAMP(create_date),UNIX_TIMESTAMP(update_date) from nasabah where nama like %s limit %s , %s"
        cursor.execute(queryData,('%'+search+'%', (page-1), limit))
        records = cursor.fetchall()
        conn.commit()
        cursor.close()

        data = []
        if cursor.rowcount > 0:
            for row in records:
                data.append({
                    "id": row[0],
                    "nama": row[1],
                    "email": row[2],
                    "alamat": row[3],
                    "saldo": row[4],
                    "last_login": row[5],
                    "created_date": row[6],
                    "updated_date": row[7]
                })

        responseHttp.status = "success"
        responseHttp.code = 200
        responseHttp.data = data


    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return responseHttp

def view_nasabah(id):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "select id,nama,email,alamat,saldo,last_login,UNIX_TIMESTAMP(create_date),UNIX_TIMESTAMP(update_date) from nasabah where id=%s"
        cursor.execute(queryData,id)
        records = cursor.fetchall()

        data = {}
        if cursor.rowcount > 0:

            data["id"]= records[0][0]
            data["nama"]= records[0][1]
            data["email"] = records[0][2]
            data["alamat"] = records[0][3]
            data["saldo"] = records[0][4]
            data["last_login"] = str(records[0][5])
            data["created_date"] = records[0][6]
            data["updated_date"] = records[0][7]
            responseHttp.status = "success"
            responseHttp.code = 200
        else:
            responseHttp.status = "data not found"
            responseHttp.code = 200
        responseHttp.data = data

        cursor.close()

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return responseHttp

def create_nasabah(nama,email,alamat):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        queryData = "insert into nasabah (id,nama,email,alamat,saldo) values (%s, %s, %s, %s, %s )"
        generatedToken = str(uuid.uuid4())
        cursor.execute(queryData,(generatedToken, nama,email,alamat,0))

        responseHttp.status = "success"
        responseHttp.code = 200
        responseHttp.data = conn.affected_rows()
        conn.commit()
        cursor.close()

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return responseHttp

def delete_nasabah(id):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "delete from nasabah where id=%s"
        cursor.execute(queryData, id)

        conn.commit()
        cursor.close()

        if conn.affected_rows() > 0 :
            responseHttp.status = "success"
            responseHttp.code = 200
        else:
            responseHttp.status = "data already deleted or data not found"
            responseHttp.code = 200
        responseHttp.data = conn.affected_rows()

    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return responseHttp

def update_nasabah(id,nama,email,alamat):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        queryData = "update nasabah set nama=%s,email=%s,alamat=%s where id=%s"
        cursor.execute(queryData,(nama,email,alamat, id))
        conn.commit()
        cursor.close()

        if conn.affected_rows() > 0 :
            responseHttp.status = "success"
            responseHttp.code = 200
        else:
            responseHttp.status = "data already changed or data not found"
            responseHttp.code = 200
        responseHttp.data = conn.affected_rows()


    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return responseHttp
