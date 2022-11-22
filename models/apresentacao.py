from common.database import db
from flask_restful import fields
from models.trilha import trilha_campos
from models.sala import sala_campos
from models.cronograma import cronograma_campos
from models.apresentacao_participante import participantes_campos
from models.autor import autor_campos


apresentacao_campos = {
    'id': fields.Integer(attribute='id'),
    'titulo': fields.String(attribute='titulo'),
    'horaInicio': fields.String(attribute='hora_inicio'),
    'horaFim': fields.String(attribute='hora_fim'),
    'isDeleted': fields.Boolean(attribute='is_deleted'),
    'trilha': fields.Nested(trilha_campos),
    'sala': fields.Nested(sala_campos),
    'cronograma': fields.Nested(cronograma_campos),
    'autores': fields.Nested(autor_campos)
}

apresentacao_participantes_campos = {
    'id': fields.Integer(attribute='id'),
    'titulo': fields.String(attribute='titulo'),
    'horaInicio': fields.String(attribute='hora_inicio'),
    'horaFim': fields.String(attribute='hora_fim'),
    'isDeleted': fields.Boolean(attribute='is_deleted'),
    'trilha': fields.Nested(trilha_campos),
    'sala': fields.Nested(sala_campos),
    'cronograma': fields.Nested(cronograma_campos),
    'participantes': fields.Nested(participantes_campos),
    'autores': fields.Nested(autor_campos)
}


'''
    Classe Apresentação.
'''
class ApresentacaoModel(db.Model):
    __tablename__ = 'apresentacao'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    hora_inicio = db.Column(db.Time)
    hora_fim = db.Column(db.Time)
    ocs_pub_id = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)

    cronograma_id = db.Column(db.Integer, db.ForeignKey('cronograma.id'))
    trilha_id = db.Column(db.Integer, db.ForeignKey('trilha.id'))
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'))

    # Cronograma
    cronograma = db.relationship("CronogramaModel")
    # Trilha
    trilha = db.relationship("TrilhaModel")
    # Sala
    sala = db.relationship("SalaModel")
    # Participantes da Apresentação
    participantes = db.relationship("ApresentacaoParticipanteModel",
                                    back_populates="apresentacao")
    # Autores
    autores = db.relationship("AutorModel", back_populates="apresentacao")

    def __init__(self, titulo, hora_inicio, hora_fim, cronograma, trilha, sala,
                 participantes = [], ocs_pub_id = 0):
        self.titulo = titulo
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.cronograma = cronograma
        self.trilha = trilha
        self.sala = sala
        self.participantes = participantes
        self.ocs_pub_id = ocs_pub_id

    def __repr__(self):
        return '<Apresentacao %d, %s, %s, %s, %s, %s, %s, %d>' % (self.id, self.titulo, self.hora_inicio, self.hora_fim,
                                                                  self.cronograma, self.trilha, self.sala, self.ocs_pub_id)
