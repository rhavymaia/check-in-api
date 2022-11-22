from common.database import db
from flask_restful import fields
from models.evento import evento_campos


predio_campos = {
    'id': fields.Integer(attribute='id'),
    'nome': fields.String(attribute='nome'),
    'descricao': fields.String(attribute='descricao'),
    'isDeleted': fields.Boolean(attribute='is_deleted'),
    'evento': fields.Nested(evento_campos)
}


class PredioModel(db.Model):
    __tablename__ = 'predio'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    ocs_predio_id = db.Column(db.Integer)

    # Salas
    salas = db.relationship("SalaModel", back_populates="predio")
    # Eventos
    eventos = db.relationship('EventoPredioModel', back_populates='predio',
                              lazy='dynamic',
                              primaryjoin="PredioModel.id==EventoPredioModel.predio_id")

    def __init__(self, nome, descricao, ocs_predio_id = 0):
        self.nome = nome
        self.descricao = descricao
        self.ocs_predio_id = ocs_predio_id

    def __str__(self):
        return '<PredioModel %d>' % (self.id)
