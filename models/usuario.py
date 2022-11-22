from common.database import db
from common.settings import secret_key
from flask_restful import fields, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

usuario_campos = {
    'id': fields.Integer(attribute='id'),
    'login': fields.String(attribute='login')
}

login_campos = {
    'id': fields.Integer(attribute='id'),
    'token': fields.String(attribute='token')
}

class UsuarioModel(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(255))

    def __init__(self, login, senha, id = None, token = None ):
        self.login = login
        self.set_senha(senha)
        self.id = id
        self.token = token

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, value):
        return check_password_hash(self.senha, value)

    def generate_auth_token(self, expiration=None):
        s = Serializer(secret_key, expires_in=expiration)
        dumps = s.dumps({'id': self.id})
        self.token = dumps.decode('ascii')
        return dumps

    @staticmethod
    def verify_auth_token(token):
        current_app.logger.info("Token: %s" % (token))
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = UsuarioModel.query.get(data['id'])
        return user

    def __str__(self):
        return '<Usuario %r>' % (self.login)
