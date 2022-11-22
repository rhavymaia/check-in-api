from flask_restful import Resource, marshal_with, reqparse, current_app, marshal
from common.auth import auth
from common.database import db
from sqlalchemy import exc
from models.trilha import TrilhaModel, trilha_campos
from models.error import ErrorModel, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)

'''
    Recursos de Trilha.
'''
# GET /trilhas
class TrilhasResource(Resource):
    @auth.login_required
    @marshal_with(trilha_campos)
    def get(self):
        current_app.logger.info("Get - Trilhas")
        trilhas = TrilhaModel.query\
            .filter_by(is_deleted=False)\
            .all()
        return trilhas, 200

    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Trilhas")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            # Trilha
            trilha = TrilhaModel(nome)
            # Criação da Trilha.
            db.session.add(trilha)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = ErrorModel(1,
                              "Erro ao adicionar no banco de dados, consulte o adminstrador",
                              err.__cause__())
            return marshal(erro, error_campos), 500


        return 204


class TrilhaResource(Resource):
    # Trilha/<id>
    @auth.login_required
    @marshal_with(trilha_campos)
    def get(self, trilha_id):
        current_app.logger.info("Get - Trilha por id")
        trilha = TrilhaModel.query.filter_by(id=trilha_id).first()
        return trilha, 200

    # trilha/<id>
    @auth.login_required
    def put(self, trilha_id):
        current_app.logger.info("Put - Trilha")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Trilha: %s:" % args)

            # Dados para atualização.
            nome = args['nome']

            TrilhaModel.query\
                .filter_by(id=trilha_id)\
                .update(dict(nome=nome))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204

    @auth.login_required
    def delete(self, trilha_id):
        current_app.logger.info("Delete - Cronograma: %s:" % trilha_id)
        try:
            TrilhaModel.query\
                .filter_by(id=trilha_id)\
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204


class BuscaTrilhasNomeResource(Resource):
    @auth.login_required
    @marshal_with(trilha_campos)
    def get(self, trilha_nome):
        current_app.logger.info("Get - Trilhas por nome")
        trilhas = TrilhaModel.query.filter(TrilhaModel.nome.ilike('%'+trilha_nome+'%')).all()
        return trilhas, 200
