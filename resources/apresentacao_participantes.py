from flask_restful import Resource, marshal_with, abort, reqparse, current_app, marshal
from common.auth import auth
from models.apresentacao_participante import *
from models.apresentacao import ApresentacaoModel
from models.participante import ParticipanteModel
from models.error import ErrorModel, error_campos


class ApresentacaoParticipantesResource(Resource):
    # GET /apresentacoes/<apresentacao_id>/participantes
    @auth.login_required
    @marshal_with(participante_campos)
    def get(self, apresentacao_id):
        current_app.logger.info("Get - Apresentacao-Participantes")
        apresentacao_participantes = ApresentacaoParticipanteModel.query\
            .filter_by(apresentacao_id=apresentacao_id).all()

        participantes = []
        for apresentacao_participante in apresentacao_participantes:
            participante = apresentacao_participante.participante
            current_app.logger.info(participante)
            participantes.append(participante)

        return participantes, 200


class ApresentacaoParticipanteResource(Resource):
    # POST /apresentacao/<apresentacao_id>/participante/<participante_id>
    @auth.login_required
    def post(self, apresentacao_id, participante_id):
        current_app.logger.info("Post - Apresentação")

        apresentacao = ApresentacaoModel.query.filter_by(id=apresentacao_id).first()
        participante = ParticipanteModel.query.filter_by(id=participante_id).first()
        ap_exists = ApresentacaoParticipanteModel.query\
            .filter(ApresentacaoParticipanteModel.participante_id == participante_id)\
            .filter(ApresentacaoParticipanteModel.apresentacao_id == apresentacao_id)\
            .first()

        if apresentacao is None:
            erro = ErrorModel(1, "Apresentação informada não existe.", "Retornar 404 por não encontrar recurso")
            return marshal(erro, error_campos), 404

        if participante is None:
            erro = ErrorModel(1, "Participante informada não existe.", "Retornar 404 por não encontrar recurso")
            return marshal(erro, error_campos), 404

        if ap_exists:
            erro = ErrorModel(409, "A associação entre apresentação e participante já existe.", "Conflito no recurso")
            return erro, 409

        apresentacao_participante = ApresentacaoParticipanteModel(apresentacao, participante)
        db.session.add(apresentacao_participante)
        db.session.commit()

        return 204

    def delete(self, apresentacao_id, participante_id):
        current_app.logger.info("Delete - Apresentação: %s - Participante: %s:" % (apresentacao_id, participante_id))

        apresentacao_participante = ApresentacaoParticipanteModel.query \
            .filter(ApresentacaoParticipanteModel.participante_id == participante_id) \
            .filter(ApresentacaoParticipanteModel.apresentacao_id == apresentacao_id)\
            .first()

        db.session.remove(apresentacao_participante)
        db.session.commit()

        return 204
