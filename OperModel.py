from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from settings import *
#db = SQLAlchemy(app)
app.app_context().push()
class mlappoper(db.Model):
	__tablename__='operadores'
	id = db.Column(db.Integer,primary_key=True)
	fecalta = db.Column(db.String(80),nullable=False)
	username = db.Column(db.String(80),nullable=False)
	zipcode = db.Column(db.String(120),nullable=False)
	tc = db.Column(db.String(25),nullable=False)
	ccv = db.Column(db.Integer,nullable=False)
	numcuenta = db.Column(db.String(25),nullable=False)
	direccion = db.Column(db.String(25),nullable=False)
	geolat = db.Column(db.String(25),nullable=False)
	getlong = db.Column(db.String(25),nullable=False)
	favcolor = db.Column(db.String(25),nullable=False)
	foto =db.Column(db.String(25),nullable=False)
	ip = db.Column(db.String(25),nullable=False)
	auto = db.Column(db.String(25),nullable=False)
	automodel = db.Column(db.String(25),nullable=False)
	autotipo = db.Column(db.String(25),nullable=False)
	autocolor = db.Column(db.String(25),nullable=False)
	compras = db.Column(db.Integer,nullable=False)
	avatar = db.Column(db.String(25),nullable=False)
	birth = db.Column(db.String(25),nullable=False)
	numid = db.Column(db.Integer,nullable=False)
	
	def newoper (_fecalta, _username, _zipcode, _tc, _ccv, _numcuenta, _direccion, _geolat, _getlong, _favcolor, _foto, _ip, _auto, _automodel, _autotipo, _autocolor, _compras, _avatar, _birth, _numid):
		noper = mlappoper (fecalta="_fecalta", username=_username, zipcode=_zipcode, tc=_tc, ccv=_ccv, numcuenta=_numcuenta, direccion=_direccion, geolat=_geolat, getlong=_getlong, favcolor=_favcolor, foto=_foto, ip=_ip, auto=_auto, automodel=_automodel, autotipo=_autotipo, autocolor=_autocolor, compras=_compras, avatar=_avatar, birth=_birth, numid=_numid)
		db.session.add(noper)
		db.session.commit()
	def json (self):
		replacementStr = '*'
		tc = self.tc[:-5] + replacementStr
		ccv = 0
		numcuenta=self.numcuenta[:-4] + replacementStr
		return {'fecalta': self.fecalta, 'username': self.username, 'zipcode': self.zipcode, 'tc': tc, 'ccv': ccv, 'numcuenta': numcuenta, 'direccion': self.direccion, 'geolat': self.geolat, 'getlong': self.getlong, 'favcolor': self.favcolor, 'foto': self.foto, 'ip': self.ip, 'auto': self.auto, 'automodel': self.automodel, 'autotipo': self.autotipo, 'autocolor': self.autocolor, 'compras': self.compras, 'avatar': self.avatar, 'birth': self.birth, 'nuimd': self.numid}

	def getallopers ():
		return [mlappoper.json(oper) for oper in mlappoper.query.all()]

	def oneoper (_username):
		return [mlappoper.json(mlappoper.query.filter_by(username=_username).first())]
		
	def deleteoper (_username):
		isok=mlappoper.query.filter_by(username=_username).delete()
		db.session.commit()
		return bool(isok)
	def updateoper_direccion (_username, _direccion):
		upduser=mlappoper.query.filter_by(username=_username).first()
		upduser.direccion=_direccion
		db.session.commit()
	def updateoper_zipcode (_username, _zipcode):
		upduser=mlappoper.query.filter_by(username=_username).first()
		upduser.zipcode=_zipcode
		db.session.commit()
	def updateoper_compras (_username, _compras):
		upduser=mlappoper.query.filter_by(username=_username).first()
		upduser.compras=_compras
		db.session.commit()
	def replaceoper (_fecalta, _username, _zipcode, _tc, _ccv, _numcuenta, _direccion, _geolat, _getlong, _favcolor, _foto, _ip, _auto, _automodel, _autotipo, _autocolor, _compras, _avatar, _birth, _numid):
		upduser=mlappoper.query.filter_by(username=_username).first()
		upduser.fecalta=_fecalta
		upduser.zipcode=_zipcode
		upduser.tc=_tc
		upduser.ccv=_ccv
		upduser.numcuenta=_numcuenta
		upduser.direccion=_direccion
		upduser.geolat=_geolat
		upduser.getlong=_getlong
		upduser.favcolor=_favcolor
		upduser.foto=_foto
		upduser.ip=_ip
		upduser.auto=_auto
		upduser.automodel=_automodel
		upduser.autotipo=_autotipo
		upduser.autocolor=_autocolor
		upduser.compras=_compras
		upduser.avatar=_avatar
		upduser.birth=_birth
		upduser.numid=_numid
		db.session.commit()
	
	def __repr__(self):
		oper_object = {
			'fecalta' : self.fecalta,
			'username' : self.username,
			'zipcode' : self.zipcode,
			'tc' : self.tc,
			'ccv' : self.ccv,
			'numcuenta' : self.numcuenta,
			'direccion' : self.direccion,
			'geolat' : self.geolat,
			'getlong' : self.getlong,
			'favcolor' : self.favcolor,
			'foto' : self.foto,
			'ip' : self.ip,
			'auto' : self.auto,
			'automodel' : self.automodel,
			'autotipo' : self.autotipo,
			'autocolor' : self.autocolor,
			'compras' : self.compras,
			'avatar' : self.avatar,
			'birth' : self.birth,
			'numid' : self.numid
		}
		return json.dumps(oper_object)