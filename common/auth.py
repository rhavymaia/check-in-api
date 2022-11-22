from flask import g
from flask_httpauth import HTTPBasicAuth
from flask_restful import current_app
from models.usuario import UsuarioModel

auth = HTTPBasicAuth()


@auth.verify_password
def verificar_senha(login_or_token, senha):
    current_app.logger.info("Auth - Login ou Token: %s" % (login_or_token))
    # Verificar token para usuários já autenticados.
    usuario = UsuarioModel.verify_auth_token(login_or_token)
    if not usuario:
        # Autenticar com login/senha
        usuario = UsuarioModel.query.filter_by(login=login_or_token).first()
        if not usuario or not usuario.verificar_senha(senha):
            return False
    # Usuário autenticado
    g.user = usuario
    return True
