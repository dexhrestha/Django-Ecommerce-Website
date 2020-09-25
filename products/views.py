from .models import Item
from .forms import CreateItem, EditItem
from flask import render_template,url_for,redirect
import sys
import os
sys.path.insert(0,'products/template')


def createItem(req):
	form = CreateItem()
	if req.method == 'GET':
		
		return render_template('add_item.html',form=form)
	if req.method == 'POST':
		title = form.title.data 
		price = form.price.data
		description = form.description.data
		if form.validate_on_submit():
			Item.create(title=title,price=price,description=description)	
			return redirect(url_for("list_item"))
		print(form.errors)

		return render_template("add_item.html",form=form)
	

def listItem(req,index=False): 
	qs = Item.select()
	content = {'items_':qs}
	if index:
		return content
	else :
		return render_template("list_item.html",content=content)


def detailItem(req,id):
	qs = Item.select().where(Item.id==id)
	for item in qs:
		content = {'item':item}
	return render_template("product_page.html",content=content)

def editItem(req,id):
	form = CreateItem()
	item = Item.select().where(Item.id==id)
	for i in item:
		item = i
	if req.method == "GET":
		form.id = item.id
		form.title.data = item.title
		form.price.data = item.price
		form.description.data = item.description

		return render_template('edit_item.html',form=form)

	if req.method == 'POST':
		if form.validate_on_submit():
			item.title = form.title.data 
			item.price = float(form.price.data)
			item.description = form.description.data

			item.save()
			return redirect(url_for("list_item"))
		print(form.errors)
		return render_template("edit_item.html",form=form)	

def deleteItem(req,id):
	dq = Item.delete().where(Item.id == id)
	dq.execute()
	return redirect(url_for('list_item'))
