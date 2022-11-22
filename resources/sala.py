from flask_restful import Resource, marshal_with, reqparse, current_app, abort, marshal
from common.auth import auth
from common.database import db
from sqlalchemy import exc
from models.sala import SalaModel, sala_campos
from models.predio import PredioModel, predio_campos
from models.error import ErrorModel, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('descricao', required=True)
parser.add_argument('cor', required=True)
parser.add_argument('capacidade', required=True)
parser.add_argument('predio', type=dict)

class SalasResource(Resource):
    # GET /salas
    @auth.login_required
    @marshal_with(sala_campos)
    def get(self):
        current_app.logger.info("Get - Salas")
        eventos = SalaModel.query\
            .order_by(SalaModel.nome)\
            .filter_by(is_deleted=False)\
            .order_by(SalaModel.predio_id, SalaModel.nome)\
            .all()
        return eventos, 200

    # POST /salas
    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Sala")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Sala: %s:" % (args))

            # args
            nome = args['nome']
            descricao = args['descricao']
            cor = args['cor']
            capacidade = args['capacidade']
            predio_id = args['predio']['id']

            # Recovering existing resources
            predio = PredioModel.query.filter_by(id=predio_id).first()

            sala = SalaModel(
                nome=nome,
                descricao=descricao, 
                predio=predio, 
                cor=cor, 
                capacidade=capacidade
            )

            # Criação do Evento.
            db.session.add(sala)
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204

# GET /salas/<id>
class SalaResource(Resource):
    @auth.login_required
    @marshal_with(sala_campos)
    def get(self, sala_id):
        current_app.logger.info("Get - Sala: %s" % sala_id)
        sala = SalaModel.query.filter_by(id=sala_id).first()
        if sala is None:
            abort(404, message='Sala {} nao existe'.format(sala_id))

        return sala, 200

    @auth.login_required
    def put(self, sala_id):
        current_app.logger.info("Put - sala: %s:" % sala_id)
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Sala: %s:" % (args))

            # args
            nome = args['nome']
            descricao = args['descricao']
            cor = args['cor']
            capacidade = args['capacidade']
            predio_id = args['predio']['id']

            predio = PredioModel.query.filter_by(id=predio_id)
            if predio is None:
                erro = ErrorModel(1, "Predio informado não existe.", "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404

            SalaModel.query\
                .filter_by(id=sala_id)\
                .update(dict(nome=nome,
                             descricao=descricao,
                             cor=cor,
                             capacidade=capacidade,
                             predio_id=predio_id))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204

    @auth.login_required
    def delete(self, sala_id):
        current_app.logger.info("Delete - sala: %s:" % sala_id)
        try:
            SalaModel.query \
                .filter_by(id=sala_id) \
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204

class SalasNomeResource(Resource):
    @marshal_with(sala_campos)
    def get(self, nome):
        current_app.logger.info("Get - Salas por nome")
        salas = SalaModel.query\
            .filter(SalaModel.nome.ilike('%' + nome + '%')).all()
        return salas, 200