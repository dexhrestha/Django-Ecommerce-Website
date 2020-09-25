from login.models import User,mysql_db
from products.models import Item
def create_tables():
	with mysql_db:
		mysql_db.create_tables([User,Item])

create_tables()
