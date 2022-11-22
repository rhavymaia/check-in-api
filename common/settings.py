import os

# Autenticação
secret_key = '123456'

# Conexões com os Bancos de dados.
usuario = os.environ.get('DB_USUARIO', 'db_senha')
senha = os.environ.get('DB_SENHA', 'db_senha')

# Depuração
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@localhost/{}?charset=utf8&use_unicode=1'.format(
    usuario,
    senha,
    'checkin'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_BINDS = {
    'ocs': 'mysql+mysqlconnector://{}:{}@localhost/{}?charset=utf8&use_unicode=1'.format(
        usuario,
        senha,
        'ocs'
    )
}
