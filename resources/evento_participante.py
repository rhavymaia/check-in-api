from flask_restful import Resource, marshal_with, abort, reqparse
from common.auth import auth
from models.evento import *
from models.participante import *
from models.participante_evento import *
from flask import g

parser = reqparse.RequestParser()
parser.add_argument('participante_id', required=True)


class EventoParticipantesResource(Resource):
    # GET /eventos/1/participantes/
    @auth.login_required
    @marshal_with(participante_evento_campos)
    def get(self, evento_id):
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        participantes = []
        for pe in evento.participantes:
            participantes.append(pe)
        return participantes, 200

    # POST /eventos/1/participantes/
    @auth.login_required
    def post(self, evento_id):
        args = parser.parse_args()
        # Evento
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        participante = ParticipanteModel.query.filter_by(
            id=args['participante_id']).first()
        if participante is None:
            abort(404, message='Participante {} nao existe'.format(evento_id))
        # Adicionando Participante ao Evento.
        participanteEvento = ParticipanteEventoModel(participante, evento)
        db.session.add(participanteEvento)
        db.session.commit()
        return 201

#TODO: Ajustar regra de negócio.
class EventoParticipanteResource(Resource):
    # PUT /eventos/1/participantes/<id>
    @auth.login_required
    def put(self, evento_id, participante_id):
        pe = ParticipanteEventoModel.query.filter_by(
            participante_id=participante_id, evento_id=evento_id).first()
        checkin = ParticipanteEventoCheckinModel.query.filter_by(
            participante_evento_id=pe.id).first()
        if checkin is None:
            checkin = ParticipanteEventoCheckinModel()
            checkin.participante_evento_id = pe.id
            checkin.entrada = db.func.now()
            checkin.usuario_id = g.usuario.id
            db.session.add(checkin)
            db.session.commit()
        return 204
