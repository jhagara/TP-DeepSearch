import pymysql

class Filler(object):

    def fill_articles(self, issue_name, db_name):

        heads = []
        fulltexts = []

        for element in semantic.articles:
            for elem in element:
                heading = ''
                fulltext = ''
                for group in elem:
                    if group.attrib['type'] == 'headings':
                        for par in group.xpath('par'):
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    heading = heading + ' ' + formatting.text
                    elif group.attrib['type'] == 'fulltexts':
                        for par in group.xpath('par'):
                            for line in par.xpath('line'):
                                for formatting in line.xpath('formatting'):
                                    fulltext = fulltext + ' ' + formatting.text
                heads.append(heading)
                ftexts.append(fulltext)

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

        for index in range(len(heads)):
            with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `articles` (`heading`, `ftext`, 'issue_id') VALUES (%s, %s, %s)"
                cursor.execute(sql, (heads[index], fulltexts[index], issue_id))

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
