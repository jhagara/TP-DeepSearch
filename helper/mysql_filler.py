import pymysql

class Filler(object):

    def fill_articles(self, issue_name, db_name):

        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="rootroot",
                             database=db_name)

        print('Connection estalished')
        with db.cursor() as cursor:
            # Create a new record
            sql = "SELECT id FROM issues"
            cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db.commit()

            create_issue = True

            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                else row[1] is issue_name:
                    create_issue = False
                    issue_id = row[0]
                    print("%s" % row[0])

        if (create_issue):
            with db.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `issues` (`name`) VALUES (%s)"
                    cursor.execute(sql, (issue_name))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                try:
                    db.commit()
                    issue_id = cursor.lastrowid
                except:
                    db.rollback()

        with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `articles` (`heading`, `ftext`, 'issue_id') VALUES (%s, %s)"
                cursor.execute(sql, (heading, ftext, issue_id))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            try:
                db.commit()
            except:
                db.rollback()


    def fill_mark_21(self, issue_name, db_name):

        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="rootroot",
                             database=db_name)

        print('Connection estalished')
        with db.cursor() as cursor:
            # Create a new record
            sql = "SELECT id FROM issues"
            cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db.commit()

            create_issue = True

            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                else row[1] is issue_name:
                    create_issue = False
                    issue_id = row[0]
                    print("%s" % row[0])

        if (create_issue):
            with db.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO `issues` (`name`) VALUES (%s)"
                    cursor.execute(sql, (issue_name))

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                try:
                    db.commit()
                    issue_id = cursor.lastrowid
                except:
                    db.rollback()

        with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO 'mark_21` (`dict_key`, `value`) VALUES (%s, %s)"
                cursor.execute(sql, (dict_key, value))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            try:
                db.commit()
            except:
                db.rollback()
