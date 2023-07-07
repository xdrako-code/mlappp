# import urllib library
from flask import Flask, jsonify, request, Response
from settings import *
from OperModel import mlappoper
import json
import requests
import base64
import sys
import getpass
from UserModel import mlappusers
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
	logging.info("GetallUsers:" + IPAddr + ' ' + mensaje)

def autentica():
	print ("Modulo de carga de clientes de la aplicacion mlapp, proporcione usuario y contraseña para iniciar")
	usuario=input("Username:")
	contrasena = getpass.getpass("Password:")
	match = mlappusers.pwdmatch(usuario, contrasena)
	if match:
		rol = mlappusers.oneuser(usuario)
		priv = str(rol[0]['role'])
		if priv=="10":
			totalrec=0
			escribelog("Autenticacion exitosa"+usuario)
			url = "https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios"
			response = requests.get(url)
			if response.status_code == 200:
				jsonData = json.loads(response.text)
				totalrec=len(jsonData)
				escribelog("Inicio de carga "+usuario)
				i=0
				while  i < totalrec:
					print ("fecha de alta", jsonData[i]["fec_alta"])
					print ("username", jsonData[i]["user_name"])
					print ("Zip code", jsonData[i]["codigo_zip"])
					print ("Tarjeta de Credito", jsonData[i]["credit_card_num"])
					print ("CCV", jsonData[i]["credit_card_ccv"])
					print ("Cuenta Numero", jsonData[i]["cuenta_numero"])
					print ("Direccion", jsonData[i]["direccion"])
					print ("Geolat", jsonData[i]["geo_latitud"])
					print ("Geolong", jsonData[i]["geo_longitud"])
					print ("color favorito", jsonData[i]["color_favorito"])
					print ("Foto", jsonData[i]["foto_dni"])
					print ("ip", jsonData[i]["ip"])
					print ("auto", jsonData[i]["auto"])
					print ("auto modelo", jsonData[i]["auto_modelo"])
					print ("auto tipo", jsonData[i]["auto_tipo"])
					print ("auto color", jsonData[i]["auto_color"])
					print ("compras", jsonData[i]["cantidad_compras_realizadas"])
					print ("avatar", jsonData[i]["avatar"])
					print ("birthday", jsonData[i]["fec_birthday"])
					print ("id", jsonData[i]["id"])
					#mlappoper.newoper (jsonData[i]["fec_alta"], jsonData[i]["user_name"], jsonData[i]["codigo_zip"], jsonData[i]["credit_card_num"], jsonData[i]["credit_card_ccv"], jsonData[i]["cuenta_numero"], jsonData[i]["direccion"], jsonData[i]["geo_latitud"], jsonData[i]["geo_longitud"], jsonData[i]["color_favorito"], jsonData[i]["foto_dni"], jsonData[i]["ip"], jsonData[i]["auto"], jsonData[i]["auto_modelo"], jsonData[i]["auto_tipo"], jsonData[i]["auto_color"], jsonData[i]["cantidad_compras_realizadas"], jsonData[i]["avatar"], jsonData[i]["fec_birthday"], jsonData[i]["id"])
					i += 1
			else:
				#print("Error retrieving data, status code: {response.status_code}")
				escribelog("Error retrieving data, status code: {response.status_code} "+ usuario)
			escribelog ("Numero de registros procesados "+ str(totalrec) + usuario)
		else:
			#print ("Usuario no autorizado para ejecutar el programa")
			escribelog ("Usuario no autorizado  "+ usuario)
		
	else:
		return escribelog ("Error al autenticar "+ usuario) 
		#print('Error al autenticar el usuario')

autentica()
