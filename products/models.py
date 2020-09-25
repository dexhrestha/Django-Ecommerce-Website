from peewee import *
import os
import sys
sys.path.insert(0,os.path.abspath('../ecom'))
from secrets.credentials import *
import pymysql
mysql_db = MySQLDatabase(dbname,
	user=username,
	password=password,
	host=hostname,
	port=port,
)

# mysql_db = pymysql.connect(
# 	host = 'localhost',
# 	user= 'root',
# 	password = 'root',
# 	db = 'ecom'
# 	)

class Item(Model):
	title = CharField(null=False,max_length=100)
	price  = FloatField(null=False)
	
	description = TextField()


	class Meta:
		database = mysql_db
		db_table = "items"
