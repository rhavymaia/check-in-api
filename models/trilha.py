from common.database import db
from flask_restful import fields


trilha_campos = {
    'id': fields.Integer(attribute='id'),
    'nome': fields.String(attribute='nome'),
    'is_deleted': fields.Boolean(attribute='is_deleted')
}


'''
    Classe Trilha.
'''
class TrilhaModel(db.Model):
    __tablename__ = 'trilha'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    is_deleted = db.Column(db.Boolean, default=False)

    # Eventos
    eventos = db.relationship('EventoTrilhaModel', back_populates='trilha',
                              lazy='dynamic',
                              primaryjoin="TrilhaModel.id==EventoTrilhaModel.trilha_id")

    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return '<Trilha %r>' % (self.nome)