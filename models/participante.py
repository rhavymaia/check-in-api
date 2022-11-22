from common.database import db
from flask_restful import fields

participante_campos = {
    'id': fields.Integer,
    'nome': fields.String(attribute='nome'),
    'cpf': fields.String(attribute='cpf'),
    'email': fields.String(attribute='email'),
    'osParticipanteId': fields.String(attribute='ocs_participante_id '),
    'isDeleted': fields.Boolean(attribute='is_deleted'),
}


'''
    Classe Participante.
'''
class ParticipanteModel(db.Model):
    __tablename__ = 'participante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150))
    cpf = db.Column(db.String(11))
    email = db.Column(db.String(90))
    ocs_participante_id = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)

    # Eventos
    eventos = db.relationship("ParticipanteEventoModel",
                              back_populates="participante")
    # Apresentações
    apresentacoes = db.relationship('ApresentacaoParticipanteModel',
                                    back_populates='participante')

    def __init__(self, nome, cpf, email, ocs_participante_id = 0):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.ocs_participante_id = ocs_participante_id

    def __str__(self):
        return '<Participante %r>' % (self.nome)
