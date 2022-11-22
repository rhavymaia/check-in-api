from flask_restful import Resource, marshal_with, reqparse, current_app, marshal
from common.auth import auth
from common.database import db
from sqlalchemy import exc
from models.autor import AutorModel, autor_campos
from models.apresentacao import ApresentacaoModel, apresentacao_campos
from models.error import ErrorModel, error_campos

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('email', required=True)
parser.add_argument('apresentacao', type=dict)

class AutoresResource(Resource):
    @auth.login_required
    @marshal_with(autor_campos)
    def get(self):
        current_app.logger.info("Get - Autores")
        autores = AutorModel.query\
        	.filter_by(is_deleted=False)\
            .order_by(AutorModel.nome)\
            .all()
        return autores, 200

    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Autores")
        try:
            # JSON
            args = parser.parse_args()
            nome = args['nome']
            email = args['email']
            apresentacao_id = args['apresentacao']['id']
            # Recovering existing resources
            apresentacao = ApresentacaoModel.query.filter_by(id=apresentacao_id).first()
            # Autor
            autor = AutorModel(nome, email, apresentacao)
            # Criação do Autor com uma apresentação.
            db.session.add(autor)
            db.session.commit()
        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            erro = ErrorModel(1, "Erro ao adicionar no banco de dados, consulte o adminstrador",
                              err.__cause__())
            return marshal(erro, error_campos), 500


        return 204

class AutorResource(Resource):
    # DELETE /autores/<id>
    @auth.login_required
    def delete(self, autor_id):
        current_app.logger.info("Delete - Autor: %s" % autor_id)
        try:
            AutorModel.query\
                .filter_by(id=autor_id)\
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204

class BuscaAutorNomeResource(Resource):
    @auth.login_required
    @marshal_with(autor_campos)
    def get(self, autor_nome):
        current_app.logger.info("Get - Autor por nome")
        autores = AutorModel.query\
        	.filter(AutorModel.nome.ilike('%'+autor_nome+'%'))\
            .order_by(AutorModel.nome)\
            .all()
        return autores, 200