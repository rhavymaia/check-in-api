from common.database import db
from flask_restful import fields

modalidade_campos = {
    'id': fields.Integer(attribute='id'),
    'nome': fields.String(attribute='nome'),
    'is_deleted': fields.Boolean(attribute='is_deleted')
}

'''
    Classe Modalidade.
'''
class ModalidadeModel(db.Model):
    __tablename__ = 'modalidade'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    # FK
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'))
    # OCS
    ocs_modalidade_id = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)

    # Evento
    evento = db.relationship("EventoModel")

    def __init__(self, nome, evento, ocs_modalidade_id = 0):
        self.nome = nome
        self.evento = evento
        self.ocs_modalidade_id = ocs_modalidade_id

    def __repr__(self):
        return '<Modalidade id=%r, nome=%r, ocs_modalidade_id=%r>' % (self.id, self.nome, self.ocs_modalidade_id)
