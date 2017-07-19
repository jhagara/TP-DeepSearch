import unittest
import os
import pymysql
import pytest
from semantic import Semantic
from helper import mysql_filler
from helper import mysql_init_tables
from helper import mysql_drop_tables


class TestDB(unittest.TestCase):
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_tables(self):
        db_name = 'test'
        mysql_drop_tables.drop_tables(db_name)
        mysql_init_tables.init_tables(db_name)

        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="root",
                             database=db_name)

        # print('Connection estalished')
        with db.cursor() as cursor:
            sql = "show tables"
            cursor.execute(sql)
            db.commit()
            row = cursor.fetchall()

        self.assertEqual(row[0][0], 'articles')
        self.assertEqual(row[1][0], 'issues')
        self.assertEqual(row[2][0], 'marc21')

        mysql_drop_tables.drop_tables(db_name)

        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="root",
                             database=db_name)

        # print('Connection estalished')
        with db.cursor() as cursor:
            sql = "show tables"
            cursor.execute(sql)
            db.commit()
            row = cursor.fetchall()

        self.assertEqual(len(row), 0)

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_filler(self):
        db_name = 'test'
        abs_path = os.path.dirname(os.path.abspath(__file__))
        header_conf_path = abs_path + "/page_header_conf_1941_1.json"
        xml_path = abs_path + "/slovak_1941_1_strana_1.xml"
        semantic = Semantic(xml=xml_path, header_config=header_conf_path)
        mysql_init_tables.init_tables(db_name)
        mysql_filler.Filler.fill_articles(semantic, 'Slovak_Test', db_name)
        mysql_filler.Filler.fill_marc21(semantic, 'Slovak_Test', db_name)

        db = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="root",
                             database=db_name)

        # print('Connection estalished')
        with db.cursor() as cursor:
            sql = "select * from articles"
            cursor.execute(sql)
            db.commit()
            row = cursor.fetchall()

        self.assertEqual(len(row), 7)
        self.assertEqual(len(row[0]), 5)
        self.assertEqual(len(row[2][1]), len(' Prielom slovenského vojska cez nepriate?ské opevnené línie'))
        self.assertEqual(row[2][1], ' Prielom slovenského vojska cez nepriate?ské opevnené línie')
        self.assertEqual(row[2][4], 0)