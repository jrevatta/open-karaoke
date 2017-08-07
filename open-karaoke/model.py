#!/usr/bin/env python
__author__ = 'Jorge Alvarado'
from google.appengine.ext import ndb

class Usuarios(ndb.Model):
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    fecha_registro = ndb.DateTimeProperty(auto_now=True)
    nombre_empresa = ndb.StringProperty(required=True)
    dni = ndb.StringProperty()
    ruc = ndb.StringProperty()
    telefono = ndb.StringProperty()
    direccion = ndb.StringProperty()


    def login(self, p_email,p_password):
        respuesta = None

        q = Usuarios.query(ndb.AND(Usuarios.email == p_email, Usuarios.password == p_password)).fetch()
        for e in q:
            respuesta = e

        return respuesta


    def user_exist(self, p_email):

        respuesta = None

        q = Usuarios.query(Usuarios.email == p_email).fetch()

        for e in q:
            respuesta = e

        return respuesta
