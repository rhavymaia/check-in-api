from common.database import db
from flask_restful import fields
from models.evento import evento_campos

cronograma_campos = {
    'id': fields.Integer,
    'nome': fields.String,
    'dataRealizacao': fields.DateTime(attribute='data_realizacao', dt_format='iso8601'),
    'horaInicio': fields.String(attribute='hora_inicio'),
    'horaFim': fields.String(attribute='hora_fim'),
    'isDeleted': fields.Boolean(attribute='is_deleted'),
    'evento': fields.Nested(evento_campos)
}

'''
    Classe Cronograma.
'''
class CronogramaModel(db.Model):
    __tablename__ = 'cronograma'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    # Data de realização do Cronograma que deve está dentro do período de realização do Evento.
    data_realizacao = db.Column(db.DateTime)
    # Hora inicial e final de realização de atividades no Cronograma.
    hora_inicio = db.Column(db.Time)
    hora_fim = db.Column(db.Time)
    # Id-Evento
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'))
    is_deleted = db.Column(db.Boolean, default=False)

    # Evento
    evento = db.relationship("EventoModel", back_populates='cronogramas')

    def __init__(self, nome, data_realizacao, hora_inicio, hora_fim, evento):
        self.nome = nome
        self.data_realizacao = data_realizacao
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.evento = evento

    def __repr__(self):
        return '<Cronograma %r>' % (self.nome)