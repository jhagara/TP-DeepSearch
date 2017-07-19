import pymysql


class Filler(object):

    def fill_articles(self, issue_name, db_name):

        heads = []
        ftexts = []
        issue_id = 9999
        is_ignored = False

        for element in self.articles:
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
                             password="root",
                             database=db_name,
                             charset='utf8')

        print('Connection estalished')
        with db.cursor() as cursor:
            # Create a new record
            sql = "SELECT * FROM issues"
            cursor.execute(sql)

            # connection is not autocommit by default. So you must commit
            # to save your changes.
            db.commit()

            create_issue = True

            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                elif row[1] is issue_name:
                    create_issue = False
                    issue_id = row[0]
                    print("%s" % row[0])

        if (create_issue):
            with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `issues` (`name`) VALUES (%s)"
                cursor.execute(sql, (issue_name))

                # connection is not autocommit by default. So you must commit
                # to save your changes.
                try:
                    db.commit()
                    issue_id = cursor.lastrowid
                except:
                    db.rollback()

        for index in range(len(heads)):
            with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `articles` (`heading`, `ftext`, `issue_id`, `is_ignored`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (heads[index], ftexts[index], issue_id, is_ignored))

                # connection is not autocommit by default. So you must commit
                # to save your changes.
                try:
                    db.commit()
                except:
                    db.rollback()
        print('done')
        print('issue_id: ', issue_id)

    def fill_marc21(self, issue_name, db_name):

        keys = []
        values = []

        for index in range(len(self.header['marc21'])):
            keys.append(self.header['marc21'][index]['key'])
            values.append(self.header['marc21'][index]['value'])

        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="root",
                             database=db_name,
                             charset='utf8')

        print('Connection estalished')
        with db.cursor() as cursor:
            # Create a new record
            sql = "SELECT * FROM issues"
            cursor.execute(sql)

            # connection is not autocommit by default. So you must commit
            # to save your changes.
            db.commit()

            create_issue = True

            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                elif row[1] is issue_name:
                    create_issue = False
                    issue_id = row[0]
                    print("%s" % row[0])

        if (create_issue):
            with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `issues` (`name`) VALUES (%s)"
                cursor.execute(sql, (issue_name))

                # connection is not autocommit by default. So you must commit
                # to save your changes.
                try:
                    db.commit()
                    issue_id = cursor.lastrowid
                except:
                    db.rollback()

        for index in range(len(keys)):
            with db.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `marc21` (`dict_key`, `value`, `issue_id`) VALUES (%s, %s, %s)"
                cursor.execute(sql, (keys[index], values[index], issue_id))

                # connection is not autocommit by default. So you must commit
                # to save your changes.
                try:
                    db.commit()
                except:
                    db.rollback()
        print('done')
