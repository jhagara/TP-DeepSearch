import pymysql

def drop_tables(db_name):
    print('Preparing connection')
    db = pymysql.connect(host="127.0.0.1",
                         user="root",
                         password="root",
                         database=db_name)

    print('Connection estalished')
    with db.cursor() as cursor:
        sql = "DROP TABLE IF EXISTS articles"
        cursor.execute(sql)
        sql = "DROP TABLE IF EXISTS marc21"
        cursor.execute(sql)
        sql = "DROP TABLE IF EXISTS issues"
        cursor.execute(sql)
    print('done')
