from common.database import db
from flask_restful import fields

autor_campos = {
    'id': fields.Integer(attribute='id'),
    'nome': fields.String(attribute='nome'),
    'email': fields.String(attribute='email'),
    'is_deleted': fields.Boolean(attribute='is_deleted')
}

'''
    Classe Autor.
'''
class AutorModel(db.Model):
    __tablename__ = 'autor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    email = db.Column(db.String(90))
    # FK
    apresentacao_id = db.Column(db.Integer, db.ForeignKey('apresentacao.id'))
    #OCS
    ocs_autor_id = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)

    # Apresentação
    apresentacao = db.relationship("ApresentacaoModel")

    def __init__(self, nome, email, apresentacao, ocs_autor_id = 0):
        self.nome = nome
        self.email = email
        self.apresentacao = apresentacao
        self.ocs_autor_id = ocs_autor_id

    def __str__(self):
        return '<Autor %r, %r>' % (self.nome, self.email)
