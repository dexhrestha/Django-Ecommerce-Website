from flask import Flask, render_template, url_for,redirect,session,flash,send_from_directory
from flask import request

from flask_wtf.csrf import CSRFProtect
from login.forms import SignupForm,LoginForm,EditInfoForm,ChangePassword
from login.models import User
from products.views import (
		createItem,
		listItem,
		detailItem,
		editItem,
		deleteItem
	)
from products.models import Item
import os
from datetime import timedelta

SECRET_KEY = os.urandom(32)

# from models import users
# from views import login

basedir = os.path.abspath(os.path.dirname(__file__))
csrf = CSRFProtect()
app = Flask(__name__,
	static_url_path='',
	static_folder='static'
)

app.config['SECRET_KEY'] = SECRET_KEY

app.config['PERMANENT_SESSION_LIFETIME']  = timedelta(minutes = 20)
csrf.init_app(app)


#STATIC JS
@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory('js',path)
#HOMEPAGE
@app.route('/')
@app.route('/index')
def home():
	content = listItem(request,index=True)

	return render_template('index.html',title="Homepage",content=content)
#Signup page
@app.route('/signup',methods=['GET','POST'])
def signup():
	if session.get('username'):
		print(session.get('username'))
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'GET':
		return render_template('signup.html',form = form)

	if request.method == 'POST':
		fname = form.fname.data.strip()
		lname = form.lname.data.strip()
		email = form.email.data.strip()
		password = form.password.data.strip()
		#validate form
		if form.validate_on_submit():
			User.create(fname=fname,lname=lname,email=email,password=password)
			return redirect(url_for('login'))
		print(form.errors)
		return render_template('signup.html',form=form)

#Login page
@app.route('/login',methods=['GET','POST'])
def login():
	if session.get('username'):
		return redirect(url_for('home'))


	form  = LoginForm()
	if request.method == 'GET':
		
		return render_template('login.html',form=form)

	if request.method == 'POST':
		email = form.email.data.strip()
		password = form.password.data.strip()
		
		if form.validate_on_submit():
			qs = User.select().where(User.email==email)
			if len(qs) > 0:
				qs = qs[0]
				if qs.password == password:
					
					session['username'] = qs.fname
					session['id'] = qs.id
					session.permanent = True
					return redirect(url_for('home'))
			
			return render_template('login.html',form=form,error="Wrong password or email")
		print(form.errors)
		return render_template('login.html',form=form,error="Wrong password or email")
#Logout
@app.route('/logout',methods=['GET',])
def logout():
	session.pop('username',None)
	return redirect(url_for('login'))
#Show users
@app.route('/show',methods=['GET'])
def list_users():
	qs = User.select()
	
	content = {'users':qs}
	return render_template("list_users.html",content=content)
#Edit Users
@app.route('/edit',methods=['GET','POST'])
def edit_user():
	form = EditInfoForm()
	if session.get('id'):
		id = session['id']
		if request.method == "GET":
			
			user = User.select().where(User.id==id)[0]
			form.fname.data = user.fname
			form.lname.data = user.lname
			form.email.data = user.email

			return render_template('edit_user.html',form=form,id=id)
		if request.method == "POST":

			if form.validate_on_submit():
				#edit in db codd\
				user = User.select().where(User.id==id)[0]
				user.fname = form.fname.data.strip()
				user.lname = form.lname.data.strip() 
				user.email = form.email.data.strip()

				user.save()
				flash("Edit successful")
				return redirect(url_for('list_users',))

			print(form.errors)
			return render_template('edit_user.html',form=form)
		return redirect(url_for('list_users',))
#Edit password
@app.route('/change_password',methods=['GET','POST'])
def change_password():

	form = ChangePassword()
	if request.method == 'GET':
		return render_template('change_password.html',form=form)
	if request.method == 'POST':
		id = session['id']	
		user = User.select().where(User.id==id)[0]
		if form.validate_on_submit():			
			old_password = form.old_password.data.strip()
			if user.password == old_password:
				user.password = form.password.data.strip()
				print(user.password)
				user.save()
				flash("Password changed sucessfully")
				return redirect(url_for('list_users'))
			flash("wrong old password")
			return redirect(url_for('list_users'))
		print(form.errors)
		return render_template('change_password.html',form=form)

#Deleteuser
@app.route('/delete',methods=['GET'])
def delete_user():
	#delete from db code
	if session.get('id'):
		id = session['id']
		dq = User.delete().where(User.id==id)
		dq.execute()

	return redirect(url_for('logout'))
#CreateItem
@app.route('/add_item',methods=['GET','POST'])
def add_item():
	#if session.get('id'):
	return createItem(request)
	#flash("You are not logged in as superuser.")
	#return redirect(url_for('home',))
#ListItem
@app.route('/list_item',methods=['GET'])
def list_item():
	return listItem(request)

@app.route('/item/<id>',methods=['GET'])
def  detail_item(id):
	return detailItem(request,id)

@app.route('/edit_item/<id>',methods=['GET','POST'])
def edit_item(id):
	return editItem(request,id)

@app.route('/delete_item/<id>',methods=['GET'])
def delete_item(id):
	return deleteItem(request,id)
	
@app.errorhandler(404)
def not_found(e):
	return render_template('404.html')

#Session management
@app.before_request
def make_session_permanent():
	session.permanent = True

if __name__== '__main__':
	app.run(debug=True)