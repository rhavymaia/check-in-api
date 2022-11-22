from common.database import db
from flask_restful import fields


evento_campos = {
    'id': fields.Integer,
    'nome': fields.String,
    'isDeleted': fields.Boolean(attribute='is_deleted'),
    'inicio': fields.DateTime(attribute='data_inicio', dt_format='iso8601'),
    'fim': fields.DateTime(attribute='data_fim', dt_format='iso8601')
}

'''
    Classe Evento.
'''
class EventoModel(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    data_inicio = db.Column(db.DateTime)
    data_fim = db.Column(db.DateTime)
    ocs_conferencia_id = db.Column(db.Integer)
    ocs_evento_id = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)


    # Participantes do Evento
    participantes = db.relationship("ParticipanteEventoModel", back_populates="evento")
    # Trilhas do Evento
    trilhas = db.relationship('EventoTrilhaModel', back_populates='evento',
                              lazy='dynamic',
                              primaryjoin="EventoModel.id==EventoTrilhaModel.evento_id")
    # Cronogramas do Evento
    cronogramas = db.relationship('CronogramaModel', back_populates='evento')
    # Prédios do Evento
    predios =  db.relationship('EventoPredioModel', back_populates='evento')

    def __init__(self, nome, data_inicio, data_fim, ocs_conferencia_id = 0,
                 ocs_evento_id = 0, participantes = [], cronogramas = [], trilhas = [],
                 predios = [], is_delete = False):
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.ocs_conferencia_id = ocs_conferencia_id
        self.ocs_evento_id = ocs_evento_id
        self.participantes = participantes
        self.cronogramas = cronogramas
        self.trilhas = trilhas
        self.predios = predios
        self.is_deleted = is_delete

    def __repr__(self):
        return '<Evento %r>' % (self.nome)