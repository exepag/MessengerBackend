import uuid
from store.config import mysql
from store.models import ResponseTemplate, UserVerified
from datetime import datetime











# list_message untuk menampilkan daftar list message siapa aja
def list_message(page, limit, search, sender, receiver):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute("select sum(1) from user where content like %s and sender like %s and receiver like %s", ('%'+search+'%', '%'+sender+'%', '%'+receiver+'%') )
        records = cursor.fetchall()
        responseHttp.pagination = {"page": page, "limit": limit, "total": int(records[0][0])}
        queryData = "select id, status, content, type, sender, receiver,UNIX_TIMESTAMP(created_date),UNIX_TIMESTAMP(updated_date) from message where content like %s and sender like %s and receiver like %s limit %s , %s"
        cursor.execute(queryData,('%'+search+'%', '%'+sender+'%', '%'+receiver+'%', (page-1)*limit , limit))
        records = cursor.fetchall()
        conn.commit()
        cursor.close()

        data = []
        if cursor.rowcount > 0:
            for row in records:
                data.append({
                    "id": row[0],
                    "status": row[1],
                    "content": row[2],
                    "type": row[3],
                    "sender": row[4],
                    "receiver": row[5],
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









#untuk nambah/membuat message
def create_message(status, content, type, sender, receiver):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        queryData = "insert into user (id, status, content, type, sender, receiver) values (%s, %s, %s, %s, %s, %s )"
        generatedToken = str(uuid.uuid4())
        cursor.execute(queryData,(generatedToken, status, content, type, sender, recreiver))

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




#untuk menghapus message
def delete_message(id):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        queryData = "delete from message where id=%s"
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






#untuk mengupdate messagenya secara keseluruhan
def update_message(id, status):
    responseHttp = ResponseTemplate()
    try:
        conn = mysql.connect()
        cursor =conn.cursor()
        queryData = "update message set status=%s where id=%s"
        cursor.execute(queryData,(status, id))
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
