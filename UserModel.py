from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from settings import *
import json
import base64
#db = SQLAlchemy(app)

#db.init_app = SQLAlchemy(app)
app.app_context().push()

class mlappusers(db.Model):
	__tablename__='usuarios'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80),nullable=False)
	username = db.Column(db.String(120),nullable=False)
	secret = db.Column(db.String(120),nullable=False)
	role = db.Column(db.Integer,nullable=False)	

	
	def desofusca (bytes_string):
		b64bytesstr=bytes_string.encode("ascii")
		b64bytes= base64.b64decode(b64bytesstr)
		pwd_string = b64bytes.decode("ascii")
		return pwd_string

	def newuser (_name, _username, _secret, _role):
		pwd_string=_secret
		pwd_str = pwd_string.encode("ascii")
		b64 = base64.b64encode(pwd_str)
		b64string = b64.decode("ascii")
		nuser = mlappusers (name=_name, username=_username, secret=b64string, role=_role)
		db.session.add(nuser)
		db.session.commit()
	
	def json (self):
		
		password="*********"
		return {'name': self.name, 'username': self.username,'secret': password, 'role': self.role}

	def terminaljson (self):
		
		return {'name': self.name, 'username': self.username,'secret': self.secret, 'role': self.role}
	
	def getallusers ():
		return [mlappusers.json(usr) for usr in mlappusers.query.all()]

	def termgetallusers ():
		return [mlappusers.terminaljson(usr) for usr in mlappusers.query.all()]

	def oneuser (_username):
		return [mlappusers.json(mlappusers.query.filter_by(username=_username).first())]

	def termoneuser (_username):
		return [mlappusers.terminaljson(mlappusers.query.filter_by(username=_username).first())]

	def deleteuser (_username):
		mlappusers.query.filter_by(username=_username).delete()
		db.session.commit()
	def updateuser_name (_username, _name):
		upduser = mlappusers.query.filter_by(username=_username).first()
		upduser.name=_name
		db.session.commit()		 
	def updateuser_passwd (_username, _secret):
		pwd_string=_secret
		pwd_str = pwd_string.encode("ascii")
		b64 = base64.b64encode(pwd_str)
		b64string = b64.decode("ascii")
		upduser = mlappusers.query.filter_by(username=_username).first()
		upduser.secret=b64string
		db.session.commit()
	def updateuser_role (_username, _role):
		upduser = mlappusers.query.filter_by(username=_username).first()
		upduser.role=_role
		db.session.commit()
	def replaceuser (_username, _name, _secret, _role):
		upduser = mlappusers.query.filter_by(username=_username).first()
		pwd_string=_secret
		pwd_str = pwd_string.encode("ascii")
		b64 = base64.b64encode(pwd_str)
		b64string = b64.decode("ascii")
		upduser.name =_name
		upduser.secret =b64string
		upduser.role =_role
		db.session.commit()
	def pwdmatch (_username, _secret):
		pwd_string=_secret
		pwd_str = pwd_string.encode("ascii")
		b64 = base64.b64encode(pwd_str)
		b64string = b64.decode("ascii")
		pwdansw = mlappusers.query.filter_by(username=_username).filter_by(secret=b64string).first()
		if pwdansw is None:
			return False
		else:
			return True
	def __repr__(self):
		user_object = {
			'name': self.name,
			'username': self.username,
			'secret': self.secret,
			'role': self.role
		}
		return json.dumps(user_object)
