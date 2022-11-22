from common.database import db
from flask_restful import fields
from models.participante import participante_campos

apresentacao_participante_campos = {
    'id': fields.Integer(attribute='id'),
    'participante': fields.Nested(participante_campos)
}

participantes_campos = {
    'participante': fields.Nested(participante_campos)
}

'''
    Classe Participantes da Apresentação.
'''
class ApresentacaoParticipanteModel(db.Model):
    __tablename__ = 'apresentacao_participante'

    id = db.Column(db.Integer, primary_key=True)
    # FK
    apresentacao_id = db.Column(db.Integer,
                                db.ForeignKey('apresentacao.id'))
    participante_id = db.Column(db.Integer,
                                db.ForeignKey('participante.id'))

    # Apresentação
    apresentacao = db.relationship("ApresentacaoModel",
                                   back_populates="participantes")
    # Participante
    participante = db.relationship("ParticipanteModel",
                                   back_populates="apresentacoes")

    def __init__(self, apresentacao, participante):
        self.apresentacao = apresentacao
        self.participante = participante

    def __repr__(self):
        return '<Apresentacao %s, %s>' % (self.apresentacao, self.participante)