from flask_restful import Resource, marshal_with, reqparse, current_app, abort, marshal
from common.auth import auth
from common.database import db
from sqlalchemy import exc
from models.predio import PredioModel, predio_campos
from models.error import ErrorModel, error_campos
from models.evento import EventoModel
from models.sala import SalaModel, sala_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('descricao', required=True)

class PrediosResource(Resource):
    # GET /predios
    @auth.login_required
    @marshal_with(predio_campos)
    def get(self):
        current_app.logger.info("Get - Predio")
        predios = PredioModel.query\
            .order_by(PredioModel.nome)\
            .filter_by(is_deleted=False)\
            .all()
        return predios, 200

    # POST /predios
    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Predio")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Predio: %s:" % (args))

            # args
            nome = args['nome']
            descricao = args['descricao']

            predio = PredioModel(nome, descricao)

            # Criação do Evento.
            db.session.add(predio)
            db.session.commit()

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = ErrorModel(1,
                              "Erro ao adicionar no banco de dados, consulte o adminstrador",
                              err)

            return marshal(erro, error_campos), 500

        return 204


class PredioResource(Resource):
    # GET /predios/<id>
    @auth.login_required
    @marshal_with(predio_campos)
    def get(self, predio_id):
        current_app.logger.info("Get - predio: %s" % predio_id)
        predio = PredioModel.query.filter_by(id=predio_id).first()
        if predio is None:
            abort(404, message='Predio {} nao existe'.format(predio_id))

        return predio, 200

    # PUT /predios/<id>
    @auth.login_required
    def put(self, predio_id):
        current_app.logger.info("Put - predio: %s:" % predio_id)
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Predio: %s:" % (args))

            # args
            nome = args['nome']
            descricao = args['descricao']

            PredioModel.query\
                .filter_by(id=predio_id)\
                .update(dict(nome=nome, descricao=descricao))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204

    # DELETE /predios/<id>
    @auth.login_required
    def delete(self, predio_id):
        current_app.logger.info("Delete - predio: %s:" % predio_id)
        try:
            PredioModel.query \
                .filter_by(id=predio_id) \
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204

class PredioSalasResource(Resource):
    # GET /predios/<predio_id>/salas
    @auth.login_required
    @marshal_with(sala_campos)
    def get(self, predio_id):
        current_app.logger.info("Get - Predio - Salas")
        salas = SalaModel.query\
        .filter(SalaModel.predio_id==predio_id)\
        .all()
        
        return salas, 200


class PrediosNomeResource(Resource):
    # GET /predios/nome/<nome>
    @auth.login_required
    @marshal_with(predio_campos)
    def get(self, nome):
        current_app.logger.info("Get - Predios por nome")
        predios = PredioModel.query.filter(PredioModel.nome.ilike('%' + nome + '%')).all()
        return predios, 200