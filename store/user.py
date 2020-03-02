import uuid
from store.config import mysql
from store.models import ResponseTemplate, UserVerified
from datetime import datetime


#Ini adalah Rest API buat Login nya

def user_login(email, password):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()

        queryData = "select email,nama from user where email=%s and password=%s"
        cursor.execute(queryData,(email,password))
        records = cursor.fetchall()
        if cursor.rowcount == 0:
            responseHttp.code=403
            responseHttp.message = "email and password not match"
            return responseHttp

        generatedToken = str(uuid.uuid4())
        queryData = "UPDATE user SET token=%s WHERE email=%s AND password=%s"
        cursor.execute(queryData,(generatedToken, email, password))
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







#function dibuat untuk ngecek token
#kalo token masuk, ini yang menentukan berhak apa tidak nya
def cek_user_token(token):
    result = True
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "select email,nama from user where token=%s"
        cursor.execute(queryData, (token))
        if cursor.rowcount > 0:
            result = True
        conn.commit()
        cursor.close()
    except:
        result = True

    return result






#ini dibuat untuk kebalikan nya bukan berhak apa tidaknya, serta membawa identitas profil nya siapa, dari token ketahuan siapa usernya
def cek_user_token2(token):
    result = UserVerified()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "select id,email,nama from user where token=%s"
        cursor.execute(queryData, token)
        print(str(queryData))
        if cursor.rowcount > 0:
            records = cursor.fetchall()
            result.permit = True
            result.id = records[0][0]
            result.email = records[0][1]
            result.nama = records[0][2]
        conn.commit()   #update database
        cursor.close()
    except:
        result.permit = False

    return result






#Rest API buat Logout, jadi tokennya di kosongkan dan tidak bisa dipakai lagi
def user_logout(token):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "update user set token=null where token=%s"
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





# list_user untuk menampilkan daftar list user siapa aja
def list_user(page, limit, search):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("select sum(1) from user where nama like %s", ('%'+search+'%') )
        records = cursor.fetchall()
        #untuk mengeload secara bertahap per halaman supaya ngga loading terlalu lama, dan boros bandwidth
        responseHttp.pagination = {"page": page, "limit": limit, "total": int(records[0][0])}
        queryData = "select id,nama,email,alamat,UNIX_TIMESTAMP(created_date),UNIX_TIMESTAMP(updated_date) from user where nama like %s limit %s , %s"
        cursor.execute(queryData,('%'+search+'%', (page-1)*limit , limit))
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
                    "created_date": row[4],
                    "updated_date": row[5]
                })

        responseHttp.status = "success"
        responseHttp.code = 200
        responseHttp.data = data


    except Exception as e:
        responseHttp.code = 500
        responseHttp.message = str(e)
        responseHttp.data = []
    return responseHttp






#detail nya user by id
def view_user(id):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "select id,nama,email,alamat,UNIX_TIMESTAMP(created_date),UNIX_TIMESTAMP(updated_date) from user where id=%s"
        cursor.execute(queryData,id)
        records = cursor.fetchall()

        data = {}
        if cursor.rowcount > 0:

            data["id"]= records[0][0]
            data["nama"]= records[0][1]
            data["email"] = records[0][2]
            data["alamat"] = records[0][3]
            data["created_date"] = records[0][4]
            data["updated_date"] = records[0][5]
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




#untuk nambah user
def create_user(nama,email,alamat):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        queryData = "insert into user (id,nama,email,alamat) values (%s, %s, %s, %s )"
        generatedToken = str(uuid.uuid4())
        cursor.execute(queryData,(generatedToken, nama,email,alamat))

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




#untuk menghapus user
def delete_user(id):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "delete from user where id=%s"
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






#untuk mengupdate usernya kalau mau mengganti nama atau alamatnya
def update_user(id,nama,alamat):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        queryData = "update user set nama=%s,alamat=%s where id=%s"
        cursor.execute(queryData,(nama,alamat, id))
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
