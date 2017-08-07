#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright Natural Computing EIRL.

import webapp2
import cgi
import jinja2

from google.appengine.api import mail
from types import *

from model import Usuarios
#from google.appengine.api import users


LEN_DETALLE = 8

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader('templates'))

class LoginHandler(webapp2.RequestHandler):
    def post(self):

        email = str(cgi.escape(self.request.get('email')))
        password = str(cgi.escape(self.request.get('password')))
        val_user = False

        #assert type(email) is StringType, "email is not a string: %r" % email

        template_name = 'ingreso2.html'

        if mail.is_email_valid(email):

            user_instance = Usuarios()

            user = user_instance.login(email, password)



            if user:

                val_user = True
                mensaje = 'Bienvenido ' + email
            else:
                mensaje = 'Lo sentimos no se encuentran datos para la informacion proporcionada'

        else:

            mensaje = 'El email es incorrecto'

        template_values = {
            'val_user': val_user,
            'mensaje': mensaje,
            'email': email
        }

        template = jinja_environment.get_template(template_name)
        self.response.out.write(template.render(template_values))


class EmailHandler(webapp2.RequestHandler):
    def post(self):
        email = cgi.escape(self.request.get('email'))

        assert type(email) is StringType, "email is not a string: %r" % email

        if mail.is_email_valid(email):
            message = mail.EmailMessage()
            message.sender = 'mail@open-karaoke-174505.appspotmail.com'
            message.to = email
            message.bcc = 'j.revatta@gmail.com'
            s = 'Bienvenido(a) ' + email + ' a Open Karaoke.' \
                                           '\nHemos enviado un correo a nuestros representantes.' \
                                           'Pronto recibiras un correo con informacion sobre nuestros servicios.' \
                                           '\n\t\t Muchas gracias por participar. ' \
                                           '\n\t\t ' \
                                           '\n\t\t Team Open Karaoke.'
            message.subject = 'Solicitud de información de servicios desde: ' + email
            message.body = s
            message.send()

        destino_informacion = 'form_respuesta.html'

        self.response.redirect(destino_informacion)

class RegistroHandler(webapp2.RequestHandler):
    def post(self):
        nombre = str(cgi.escape(self.request.get('nombre')))
        tipodoc = str(cgi.escape(self.request.get('tipodoc')))
        dni_ruc = str(cgi.escape(self.request.get('dni_ruc')))
        direccion = str(cgi.escape(self.request.get('direccion')))
        telefono = str(cgi.escape(self.request.get('telefono')))
        email = str(cgi.escape(self.request.get('email')))
        password = str(cgi.escape(self.request.get('clave1')))
        password2 = str(cgi.escape(self.request.get('clave2')))

        template_name = 'registro.html'
        user_exist = False

        if mail.is_email_valid(email):

            user_instance = Usuarios()

            user = user_instance.user_exist(email)

            if user:
                user_exist = True
                mensaje = 'Ya existe un registro con este correo. Si olvido su clave solicite una por el enlace correspondiente'

            else:

                user_instance.nombre_empresa = nombre
                if tipodoc == 'dni':
                    user_instance.dni = dni_ruc
                else:
                    user_instance.ruc = dni_ruc
                user_instance.direccion = direccion
                user_instance.email = email
                user_instance.telefono = telefono
                user_instance.password = password

                user_instance.put()

                mensaje = 'Gracias por registrarse en nuestro servicio'

                message = mail.EmailMessage()
                message.sender = 'mail@open-karaoke-174505.appspotmail.com'
                message.to = email
                message.bcc = 'j.revatta@gmail.com'
                s = 'Bienvenido(a) ' + email + ' a Open Karaoke.' \
                                               '\nHemos enviado un correo a nuestros representantes.' \
                                               'Pronto recibiras un correo con informacion sobre nuestros servicios.' \
                                               '\n\t\t Muchas gracias por participar. ' \
                                               '\n\t\t ' \
                                               '\n\t\t Team Open Karaoke.'
                message.subject = 'Registro en servicios de Open Karaoke desde: ' + email
                message.body = s
                message.send()


        else:
            mensaje = 'El email es incorrecto'

        template_values = {
            'user_exist': user_exist,
            'mensaje': mensaje,
            'email': email
        }

        template = jinja_environment.get_template(template_name)
        self.response.out.write(template.render(template_values))

class BatchHandler(webapp2.RequestHandler):

    def get(self):

        #esto para cargar informacion de inicio de sesion
        """
        """



app = webapp2.WSGIApplication([
    ('/login', LoginHandler),
    ('/batch', BatchHandler),
    ('/email', EmailHandler),
    ('/registro', RegistroHandler)
], debug=True)
