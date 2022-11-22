from common.database import db
from flask_restful import fields
from models.predio import predio_campos
from sqlalchemy.ext.orderinglist import ordering_list


sala_campos = {
    'id': fields.Integer(attribute='id'),
    'nome': fields.String(attribute='nome'),
    'descricao': fields.String(attribute='descricao'),
    'cor': fields.String(attribute='cor'),
    'capacidade': fields.Integer(attribute='capacidade'),
    'predio': fields.Nested(predio_campos),
    'isDeleted': fields.Boolean(attribute='is_deleted')
}


'''
    Classe Sala.
'''
class SalaModel(db.Model):
    __tablename__ = 'sala'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    descricao = db.Column(db.Text)
    cor = db.Column(db.String(255))
    capacidade = db.Column(db.Integer)
    ocs_sala_id = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)
    # FK
    predio_id = db.Column(db.Integer, db.ForeignKey('predio.id'))

    # Predio
    predio = db.relationship("PredioModel", order_by="PredioModel.id",
                             collection_class=ordering_list('id'),
                             back_populates="salas")

    def __init__(self, nome, descricao, predio, cor = 'ffffff', capacidade = 0,
                 ocs_sala_id = 0):
        self.nome = nome
        self.descricao = descricao
        self.predio = predio
        self.cor = cor
        self.capacidade = capacidade
        self.ocs_sala_id = ocs_sala_id

    def __str__(self):
        return '<Sala %r>'%(self.nome)