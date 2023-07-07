from flask import Flask, jsonify, request, Response
from settings import *
from UserModel import mlappusers
from OperModel import mlappoper
import json
import requests
import base64
import jwt, datetime
import socket    
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("mlapp.log"),
        logging.StreamHandler()
    ]
)
def escribelog(mensaje):
	hostname = socket.gethostname()    
	IPAddr = socket.gethostbyname(hostname)    
	logging.info("mlapp:" + IPAddr + ' ' + mensaje)


#app = Flask(__name__)

#En esta seccion seran definidas la rutas de acceso los endpoints del api utilizados para consumir la data de operadores (clientes) 
app.config['SECRET_KEY'] = 'estalallavecodeencode'

@app.route('/login', methods=['POST'])
def gettoken():
	request_data = request.get_json()
	usuario =str(request_data['username'])
	contrasena=str(request_data['secret'])
	match = mlappusers.pwdmatch(usuario, contrasena)
	if match:
		rol = mlappusers.oneuser(usuario)
		priv = str(rol[0]['role'])
		expirationjwt = datetime.datetime.utcnow() + datetime.timedelta(seconds=600)
		#token=jwt.encode ({'exp': expirationjwt, 'aud': priv, 'sub': usuario}, key='estalallavecodeencode', algorithm='HS256')
		tokenall = {
			'exp': expirationjwt,
			'aud': priv,
			'sub': usuario		
		}
		#token=jwt.encode ({'exp': expirationjwt}, key='estalallavecodeencode', algorithm='HS256')
		token=jwt.encode (tokenall, key='estalallavecodeencode', algorithm='HS256')
		escribelog("Autenticacion exitosa " + usuario)
		return token
	else:
		escribelog("Error al autenticar " + usuario)
		return Response('', 401, mimetype='application/json')

@app.route('/clientes')
def get_oper():
		
		token = request.args.get('token')
		try:
			#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
			rol = jwt.decode(token, options={"verify_signature": False})

		except:
			escribelog("Token Invalido")
			return jsonify ({'error': 'Token Invalido'})	
			
		if (rol['aud'] == "1"):
			escribelog("GetOper " + rol['sub'])
			return jsonify ({'usuarios': mlappoper.getallopers()})
			
		else:
			escribelog("Usuario no autorizado " + rol['sub'])
			return Response('', 401, mimetype='application/json')
			

@app.route('/clientes/<string:username>')
def get_onlyoneoper(username):
		
		token = request.args.get('token')
		try:
			rol = jwt.decode(token, options={"verify_signature": False})
			#jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
		except:
			escribelog("Token Invalido")
			return jsonify ({'error': 'Token invalido'})

		if (rol['aud'] == "1" or rol['aud'] == "2" or rol['aud'] == "3"):
			escribelog("GetOnlyOneOper " + username + " " + rol['sub'])
			return jsonify (mlappoper.oneoper(username))
					
		else:
			escribelog("Usuario no autorizado " + rol['sub'])
			return Response('', 401, mimetype='application/json')

def validuser(userobject):
	if ("fecalta" in userobject and "username" in userobject and "zipcode" in userobject and "tc" in userobject and "ccv" in userobject and "numcuenta" in userobject and "direccion" in userobject  and "geolat" in userobject and "getlong" in userobject  and "favcolor" in userobject and "foto" in userobject  and "ip" in userobject and "auto" in userobject and "automodel" in userobject and "autotipo" in userobject and "autocolor" in userobject and "compras" in userobject and "avatar" in userobject and "birth" in userobject and "nuimd" in userobject):
		return True
	else:
		return False

@app.route('/clientes', methods=['POST'])
def add_oper():
	request_data = request.get_json()
	
	token = request.args.get('token')
	try:
		rol = jwt.decode(token, options={"verify_signature": False})
				#jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Token invalido'})	

	if rol['aud'] == "1":
				
		if (validuser(request_data)):
			mlappoper.newoper (request_data['fecalta'], request_data['username'], request_data['zipcode'], request_data['tc'], request_data['ccv'], request_data['numcuenta'], request_data['direccion'], request_data['geolat'], request_data['getlong'], request_data['favcolor'], request_data['foto'], request_data['ip'], request_data['auto'], request_data['automodel'], request_data['autotipo'], request_data['autocolor'], request_data['compras'], request_data['avatar'], request_data['birth'], request_data['nuimd'])
			respuesta = Response ("", 201, mimetype='application/json')
			respuesta.headers['Location'] =  "/clientes/" + str(request_data['username'])
			escribelog("AddOper " + request_data['username'] + " " + rol['sub'])
			return respuesta
		else:
			invalidUser = {
				"error": "Request invalido",
				"help": "Formato invalido o informacion incompleta "
			}
			respuesta = Response (json.dumps(invalidUser), 400, mimetype='application/json') 
			return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')
			
@app.route('/clientes/<string:username>', methods=['PUT'])
def update_oper(username):
	request_data = request.get_json()
	
	token = request.args.get('token')
	try:
		rol = jwt.decode(token, options={"verify_signature": False})
		#jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Token invalido'})	
	if (rol['aud'] == "1" or rol['aud'] == "2"):

		if (validuser(request_data)):
			mlappoper.replaceoper(request_data['fecalta'],username, request_data['zipcode'], request_data['tc'], request_data['ccv'], request_data['numcuenta'], request_data['direccion'], request_data['geolat'], request_data['getlong'], request_data['favcolor'], request_data['foto'], request_data['ip'], request_data['auto'], request_data['automodel'], request_data['autotipo'], request_data['autocolor'], request_data['compras'], request_data['avatar'], request_data['birth'], request_data['nuimd'])
			respuesta = Response("", status=204)
			escribelog("UpdateOper " + username + " " + rol['sub'])
			return respuesta
		else:
			invalidUser = {
				"error": "Request invalido",
				"help": "Formato invalido o informacion incompleta "
			}
			respuesta = Response (json.dumps(invalidUser), 400, mimetype='application/json') 
			return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')	
		

@app.route('/clientes/<string:username>', methods=['PATCH'])
def pupdate_oper(username):
	request_data = request.get_json()
	
	token = request.args.get('token')
	try:
		rol = jwt.decode(token, options={"verify_signature": False})
		#jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Token invalido'})	
	if (rol['aud'] == "1" or rol['aud'] == "2" or rol['aud'] == "3"):
		if ("direccion" in request_data):
			mlappoper.updateoper_direccion(username, request_data['direccion'])
			escribelog("UpdateOperDireccion " + username + " " + rol['sub'])
		if ("zipcode" in request_data):
			mlappoper.updateoper_zipcode(username, request_data['zipcode'])
			escribelog("UpdateOperZipCode " + username + " " + rol['sub'])

		if ("compras" in request_data):
			mlappoper.updateoper_compras(username, request_data['compras'])
			escribelog("UpdateOperCompras " + username + " " + rol['sub'])
		respuesta = Response("", status=204)
		respuesta.headers['Location'] =  "/usuarios/" + str(username)
		return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')	
		
			
@app.route ('/clientes/<string:username>', methods=['DELETE'])
def delete_oper(username):
	
	token = request.args.get('token')
	try:
		rol = jwt.decode(token, options={"verify_signature": False})
		#jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Token invalido'})	
	if rol['aud'] == "1":
		if (mlappoper.deleteoper(username)):
			respuesta = Response("", status=204)
			escribelog("DeleteOper " + username + " " + rol['sub'])
			return respuesta
		else:
			invalidUser = {
				"error": "Datos incorrectos",
				"help": "El usuario que proporciono no existe en la base de datos "
			}
			respuesta = Response(json.dumps(invalidUser), status=404, mimetype='application/json')
			return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')	
		
				
########################################
#En esta seccion seran definidas la rutas de acceso los endpoints del api utilizados para consumir la data de los usuarios
########################################


@app.route('/usuarios')
def get_user():
	token = request.args.get('token')
	try:
		#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
		rol = jwt.decode(token, options={"verify_signature": False})

	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Token Invalido'})	
			
	if rol['aud'] == "10":
		escribelog("GetAllUsers " + rol['sub'])
		return jsonify ({'usuarios': mlappusers.getallusers()})
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')

@app.route('/usuarios/<string:username>')
def get_onlyoneuser(username):
	token = request.args.get('token')
	try:
		#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
		rol = jwt.decode(token, options={"verify_signature": False})

	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Invalid token o token no proporcionado'})	
			
	if (rol['aud'] == "10"):
		return_value = mlappusers.oneuser(username)
		escribelog("GetOnlyOneUser " + username + " " + rol['sub'])
		return jsonify (return_value)

	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')
def validusers(userobject):
	
	if ("name" in userobject and "username" in userobject and "secret" in userobject and "role" in userobject):
		return True
	else:
		return False

@app.route('/usuarios', methods=['POST'])
def add_user():
	request_data = request.get_json()
	token = request.args.get('token')
	try:
		#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
		rol = jwt.decode(token, options={"verify_signature": False})

	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Invalid token o token no proporcionado'})	
			
	if (rol['aud'] == "10"):

		if (validusers(request_data)):
		
			mlappusers.newuser (request_data['name'], request_data['username'], request_data['secret'], request_data['role'])
			respuesta = Response ("", 201, mimetype='application/json')
			respuesta.headers['Location'] =  "/usuarios/" + str(request_data['username'])
			escribelog("AddUser " + request_data['username'] + " " + rol['sub'])
			return respuesta
		else:
			invalidUser = {
				"error": "Invalid request",
				"help": "Formato invalido o informacion incompleta "
			}
			respuesta = Response (json.dumps(invalidUser), 400, mimetype='application/json') 
			return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')

@app.route('/usuarios/<string:username>', methods=['PUT'])
def update_user(username):
	request_data = request.get_json()
	token = request.args.get('token')
	try:
		#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
		rol = jwt.decode(token, options={"verify_signature": False})

	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Invalid token o token no proporcionado'})	
			
	if (rol['aud'] == "10"):

		if (validusers(request_data)):
			mlappusers.replaceuser(username, request_data['name'], request_data['secret'], request_data['role'])
			respuesta = Response("", status=204)
			escribelog("UpdateUser " + username + " " + rol['sub'])
			return respuesta
		else:
			invalidUser = {
				"error": "Invalid request",
				"help": "Formato invalido o informacion incompleta "
			}
			respuesta = Response (json.dumps(invalidUser), 400, mimetype='application/json') 
			return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')

@app.route('/usuarios/<string:username>', methods=['PATCH'])
def pupdate_user(username):
	request_data = request.get_json()
	
	token = request.args.get('token')
	try:
		#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
		rol = jwt.decode(token, options={"verify_signature": False})

	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Invalid token o token no proporcionado'})	
			
	if (rol['aud'] == "10"):
		if ("name" in request_data):
			mlappusers.updateuser_name(username, request_data['name'])
			escribelog("UpdateUserName " + username + " " + rol['sub'])
		if ("secret" in request_data):
			mlappusers.updateuser_passwd(username, request_data['secret'])
			escribelog("UpdateUserSecret " + username + " " + rol['sub'])
		if ("role" in request_data):
			mlappusers.updateuser_role(username, request_data['role'])
			escribelog("UpdateUserRole " + username + " " + rol['sub'])
		respuesta = Response("", status=204)
		respuesta.headers['Location'] =  "/usuarios/" + str(username)
		return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')	
@app.route ('/usuarios/<string:username>', methods=['DELETE'])
def delete_user(username):
	
	token = request.args.get('token')
	try:
		#rol=jwt.decode(token, key='estalallavecodeencode', algorithms=["HS256"])
		rol = jwt.decode(token, options={"verify_signature": False})

	except:
		escribelog("Token Invalido")
		return jsonify ({'error': 'Invalid token o token no proporcionado'})	
			
	if (rol['aud'] == "10"):
		if (mlappusers.deleteuser(username)):
			respuesta = Response("", status=204)
			escribelog("DeleteUser " + username + " " + rol['sub'])
			return respuesta
		else:
			invalidUser = {
				"error": "Datos incorrectos",
				"help": "El usuario que proporciono no existe en la base de datos "
			}
			respuesta = Response(json.dumps(invalidUser), status=404, mimetype='application/json')
			return respuesta
	else:
		escribelog("Usuario no autorizado " + rol['sub'])
		return Response('', 401, mimetype='application/json')

#app.run(port=5000)
app.run('0.0.0.0', debug=False, port=8443, ssl_context=('server.crt', 'server.key'))