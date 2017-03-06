import os
import sys
import pymysql
from semantic import Semantic
from helper import mysql_filler
from helper import mysql_init_tables
from helper import mysql_drop_tables

print ('Issue name: ', str(sys.argv[1]))
print ('Path to XML file: ', str(sys.argv[2]))
print ('Path to JSON header conffile: ', str(sys.argv[3]))

db_name = 'text'
issue_name = str(sys.argv[1])
xml_path = str(sys.argv[2])
header_conf_path = str(sys.argv[3])

mysql_drop_tables.drop_tables(db_name)

mysql_init_tables.init_tables(db_name)

semantic = Semantic(xml=xml_path, header_config=header_conf_path)
mysql_filler.Filler.fill_articles(semantic, issue_name, db_name)
mysql_filler.Filler.fill_marc21(semantic, issue_name, db_name)
