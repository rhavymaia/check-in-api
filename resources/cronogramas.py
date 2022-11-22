from flask_restful import Resource, marshal_with, abort, reqparse, current_app, marshal
from common.auth import auth
from common.database import db
from sqlalchemy import exc
from models.cronograma import CronogramaModel, cronograma_campos
from models.evento import EventoModel
from models.error import error_campos, ErrorModel
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True, help="Especifique um nome válido para o Cronograma.")
parser.add_argument('dataRealizacao', required=True, help="Especifique uma data válida para o Cronograma.")
parser.add_argument('horaInicio', required=True, help="Especifique uma hora inicial válida para o Cronograma.")
parser.add_argument('horaFim', required=True, help="Especifique uma hora final válida para o Cronograma.")
parser.add_argument('evento', type=dict)
parser.add_argument('is_deleted')


class CronogramasResource(Resource):
    # GET /cronogramas
    @auth.login_required
    @marshal_with(cronograma_campos)
    def get(self):
        current_app.logger.info("Get - Cronogramas")
        cronogramas = CronogramaModel.query\
            .filter_by(is_deleted=False)\
            .all()
        return cronogramas, 200

    # POST /cronogramas
    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Cronogramas")
        try:
            args = parser.parse_args()
            current_app.logger.info("Cronograma: %s:" % args)

            nome = args['nome']
            data_realizacao = args['dataRealizacao']
            hora_inicio = args['horaInicio']
            hora_fim = args['horaFim']
            evento_id = args['evento']['id']



            evento = EventoModel.query.filter_by(id=evento_id).first()

            if evento is None:
                erro = ErrorModel(1, "O evento informado não existe.", "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404

            dentrodoprazo = isDentroDoPrazo(evento, datetime.strptime(data_realizacao,'%Y-%m-%dT%H:%M:%S'))
            if dentrodoprazo is False:
                print('Fora do prazo')
                erro = ErrorModel(1, 'Fora do prazo do evento', "Retornar 409 por conflito de datas.")
                return marshal(erro, error_campos), 404

            cronograma = CronogramaModel(nome, data_realizacao,
                                         hora_inicio, hora_fim, evento)
            db.session.add(cronograma)
            db.session.commit()

        except exc.SQLAlchemyError as e:
            current_app.logger.error("Exceção: " + e)
            erro = ErrorModel(5, "Ocoreu um erro interno e será solucionado. Tente novamente mais tarde.", "Exceção")
            return marshal(erro, error_campos), 500

        return 204


# GET /cronogramas/<id>
class CronogramaResource(Resource):
    @marshal_with(cronograma_campos)
    def get(self, cronograma_id):
        cronograma = CronogramaModel.query.filter_by(id=cronograma_id).first()
        if cronograma is None:
            abort(404, message='Cronograma {} nao existe'.format(cronograma_id))
        return cronograma, 200

    @auth.login_required
    def put(self, cronograma_id):
        current_app.logger.info("Put - Cronograma")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Cronograma: %s:" % args)
            # Evento
            nome = args['nome']
            data_realizacao = args['dataRealizacao']
            hora_inicio = args['horaInicio']
            hora_fim = args['horaFim']
            evento_id = args['evento']['id']

            evento = EventoModel.query.filter_by(id=evento_id).first()

            if evento is None:
                erro = ErrorModel(1, "Evento %s não existe." % evento_id, "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404

            dentrodoprazo = isDentroDoPrazo(evento, datetime.strptime(data_realizacao, '%Y-%m-%dT%H:%M:%S'))
            if dentrodoprazo is False:
                erro = ErrorModel(1, "Cronograma fora do prazo do evento.", "Retorno 409, conflito de horário.")
                return marshal(erro, error_campos), 404


            CronogramaModel.query \
                .filter_by(id=cronograma_id) \
                .update(dict(nome=nome,
                             data_realizacao=data_realizacao,
                             hora_inicio=hora_inicio,
                             hora_fim=hora_fim,
                             evento_id=evento_id))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204

    @auth.login_required
    def delete(self, cronograma_id):
        current_app.logger.info("Delete - Cronograma: %s:" % cronograma_id)
        try:
            CronogramaModel.query\
                .filter_by(id=cronograma_id)\
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204


class BuscaCronogramasNomeResource(Resource):
    @auth.login_required
    @marshal_with(cronograma_campos)
    def get(self, cronograma_nome):
        current_app.logger.info("Get - Cronogramas por nome")
        cronogramas = CronogramaModel.query.filter(CronogramaModel.nome.ilike('%'+cronograma_nome+'%')).all()
        return cronogramas, 200


def isDentroDoPrazo(evento, data_realizacao):
    # Data realização tem que estar entre inicio e fim do evento.
    if data_realizacao < evento.data_inicio:
        return False

    if data_realizacao > evento.data_fim:
        return False

    return True
