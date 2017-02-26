import pymysql

print('Preparing connection')
db = pymysql.connect(host="127.0.0.1",
                     user="root",
                     password="rootroot",
                     database="tp")

print('Connection estalished')
with db.cursor() as cursor:
    sql = "DROP TABLE IF EXISTS issues, articles, mark_21"
    cursor.execute(sql)

print('done')
