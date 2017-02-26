import pymysql

print('Preparing connection')
db = pymysql.connect(host="127.0.0.1",
                     user="root",
                     password="rootroot",
                     database="tp")

print('Connection estalished')
with db.cursor() as cursor:

    query_create_issues = """
            CREATE TABLE IF NOT EXISTS issues (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name TEXT CHARACTER SET utf8
            );
            """

    query_create_articles = """
            CREATE TABLE IF NOT EXISTS articles (
            id INT NOT NULL AUTO_INCREMENT,
            heading TEXT CHARACTER SET utf8,
            ftext TEXT CHARACTER SET utf8,
            issue_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (issue_id) REFERENCES issues(id)
            );
            """

    query_create_mark21 = """
            CREATE TABLE IF NOT EXISTS mark_21 (
            id INT NOT NULL AUTO_INCREMENT,
            dict_key TEXT CHARACTER SET utf8,
            value TEXT CHARACTER SET utf8,
            issue_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (issue_id) REFERENCES issues(id)
            );
            """

    print('Execuring query #1')
    cursor.execute(query_create_issues)
    print('Execuring query #2')
    cursor.execute(query_create_articles)
    print('Execuring query #3')
    cursor.execute(query_create_mark21)

print('done')
