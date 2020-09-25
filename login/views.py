from models import User

def create_user():
	User.create(id = 5 ,fname="fname",lname="lname",email="dexter.shrestha10@gamil.com",password='pass')
	# user.save()

def read_users():
	sq = User.select(User)
	for row in sq:
		print(row.fname)

def update_user():
	pass

def delete_user():
	pass

create_user()
read_users()