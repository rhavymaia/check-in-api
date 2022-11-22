from common.database import db
from flask_restful import fields
from models.trilha import trilha_campos
from models.evento import evento_campos


trilha_evento_campos = {
    'id': fields.Integer(attribute='id'),
    'trilha': fields.Nested(trilha_campos),
    'evento': fields.Nested(evento_campos)
}


'''
    Classe Participante de Eventos.
'''
class EventoTrilhaModel(db.Model):
    __tablename__ = 'trilha_evento'

    id = db.Column(db.Integer, primary_key=True)

    evento_id = db.Column(db.Integer,
                          db.ForeignKey('evento.id'))

    trilha_id = db.Column(db.Integer,
                          db.ForeignKey('trilha.id'))
    # Evento
    evento = db.relationship("EventoModel", back_populates="trilhas")

    # Trilha
    trilha = db.relationship("TrilhaModel", back_populates="eventos")

    def __init__(self, evento, trilha):
        self.evento = evento
        self.trilha = trilha