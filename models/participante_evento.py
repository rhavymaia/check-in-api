from common.database import db
from flask_restful import fields
from models.participante import participante_campos


participante_evento_checkin_campos = {
    'usuario_id': fields.Integer,
    'entrada': fields.DateTime
}


participante_evento_campos = {
    'participante': fields.Nested(participante_campos),
    'checkin': fields.Nested(participante_evento_checkin_campos)
}


'''
    Classe Participantes do Evento.
'''
class ParticipanteEventoModel(db.Model):
    __tablename__ = 'participante_evento'

    id = db.Column(db.Integer, primary_key=True)
    participante_id = db.Column(db.Integer,
                                db.ForeignKey('participante.id'))
    evento_id = db.Column(db.Integer,
                          db.ForeignKey('evento.id'))
    tipo_participante_evento_id = db.Column(db.Integer,
                                  db.ForeignKey('tipo_participante_evento.id'))
    # Evento
    evento = db.relationship("EventoModel", back_populates="participantes")

    # Participante
    participante = db.relationship("ParticipanteModel",
                                   back_populates="eventos")

    # Tipo do Participante do Evento.
    tipoParticipanteEvento = db.relationship("TipoParticipanteEventoModel")

    # Checkin
    checkin = db.relationship('ParticipanteEventoCheckinModel',
                              backref='participante_evento',
                              lazy='joined')

    def __init__(self, participante, evento, tipoParticipanteEvento = None):
        self.participante = participante
        self.evento = evento
        self.tipoParticipanteEvento = tipoParticipanteEvento


'''
    Classe Checkin do Participante.
'''
class ParticipanteEventoCheckinModel(db.Model):
    __tablename__ = 'participante_evento_checkin'

    participante_evento_id = db.Column(db.Integer,
                                       db.ForeignKey('participante_evento.id'),
                                       primary_key=True)
    usuario_id = db.Column(db.Integer,
                           db.ForeignKey('usuario.id'))
    entrada = db.Column(db.DateTime)


'''
    Tipo do Participante.
'''
class TipoParticipanteEventoModel(db.Model):
    __tablename__ = 'tipo_participante_evento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    ocs_tipo_participante_id = db.Column(db.Integer, default=0)
    evento_id = db.Column(db.Integer,
                          db.ForeignKey('evento.id'))

    def __init__(self, nome, evento_id, ocs_tipo_participante_id = 0):
        self.nome = nome
        self.evento_id = evento_id
        self.ocs_tipo_participante_id = ocs_tipo_participante_id

    def __str__(self):
        return "<TipoParticipanteEventoModel %d>" % (self.id)
