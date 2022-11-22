from common.database import db
from flask_restful import fields


turno_campos = {
    'id': fields.Integer(attribute='id'),
    'nome': fields.String(attribute='nome')
}


'''
    Classe Turno.
'''
class TurnoModel(db.Model):
    __tablename__ = 'turno'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    hora_inicio = db.Column(db.Time)
    hora_fim = db.Column(db.Time)

    def __init__(self, nome, hora_inicio, hora_fim):
        self.nome = nome
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim