from common.database import db
from flask_restful import fields
from models.predio import PredioModel, predio_campos
from models.evento import EventoModel, evento_campos


predio_evento_campos = {
    'id': fields.Integer(attribute='id'),
    'predio': fields.Nested(predio_campos),
    'evento': fields.Nested(evento_campos)
}


'''
    Classe Prédio do Evento.
'''
class EventoPredioModel(db.Model):
    __tablename__ = 'predio_evento'

    id = db.Column(db.Integer, primary_key=True)

    evento_id = db.Column(db.Integer,
                          db.ForeignKey('evento.id'))

    predio_id = db.Column(db.Integer,
                          db.ForeignKey('predio.id'))
    # Evento
    evento = db.relationship("EventoModel", back_populates="predios")
    # Prédio
    predio = db.relationship("PredioModel", back_populates="eventos")

    def __init__(self, evento, predio):
        self.evento = evento
        self.predio = predio

    def __str__(self):
        return '<EventoPredioModel %d, %d>' % (self.evento_id, self.predio_id)