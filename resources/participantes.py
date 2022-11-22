from flask_restful import Resource, reqparse, marshal_with, abort, current_app
from common.database import db
from sqlalchemy import exc
from common.auth import auth
from models.participante import ParticipanteModel, participante_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('cpf', required=True)
parser.add_argument('email', required=True)

# GET /participantes
# POST /participantes
class ParticipantesResource(Resource):
    @auth.login_required
    @marshal_with(participante_campos)
    def get(self):
        current_app.logger.info("Get - Participantes")
        participantes = ParticipanteModel.query\
            .filter_by(is_deleted=False)\
            .all()
        return participantes, 200

    @auth.login_required
    @marshal_with(participante_campos)
    def post(self):
        current_app.logger.info("Post - Participantes")
        try:
            args = parser.parse_args()
            nome = args['nome']
            cpf = args['cpf']
            email = args['email']
            participante = ParticipanteModel(nome, cpf, email)
            db.session.add(participante)
            db.session.commit()
        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return participante, 201


# GET /participantes/<id>
# PUT /participantes/<id>
class ParticipanteResource(Resource):
    @auth.login_required
    @marshal_with(participante_campos)
    def get(self, participante_id):
        participante = ParticipanteModel.query.filter_by(
            id=participante_id).first()
        if participante is None:
            abort(404, message="Participante {} não existe"
                  .format(participante_id))
        return participante, 200

    @auth.login_required
    def put(self, participante_id):
        current_app.logger.info("Put - Participante")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Participante: %s:" % args)

            # Dados para atualização.
            nome = args['nome']
            cpf = args['cpf']
            email = args['email']

            ParticipanteModel.query\
                .filter_by(id=participante_id)\
                .update(dict(nome=nome, cpf=cpf, email=email))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
        return 204

    @auth.login_required
    def delete(self, participante_id):
        current_app.logger.info("Delete - Participante: %s:" % participante_id)
        try:
            ParticipanteModel.query\
                .filter_by(id=participante_id)\
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204

class BuscaParticipantesNomeResource(Resource):
    @auth.login_required
    @marshal_with(participante_campos)
    def get(self, participante_nome):
        current_app.logger.info("Get - Participantes por nome")
        participantes = ParticipanteModel.query.filter(ParticipanteModel.nome.ilike('%'+participante_nome+'%')).all()
        return participantes, 200