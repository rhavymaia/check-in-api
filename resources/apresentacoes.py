from flask_restful import Resource, marshal_with, reqparse, current_app, abort, marshal
from sqlalchemy import exc, or_, and_

from common.auth import auth
from common.database import db
from models.apresentacao import ApresentacaoModel, apresentacao_campos
from models.cronograma import CronogramaModel
from models.error import ErrorModel, error_campos
from models.sala import SalaModel
from models.trilha import TrilhaModel
from models.autor import AutorModel, autor_campos
from models.trilha_evento import EventoTrilhaModel
from models.participante import participante_campos, ParticipanteModel
from models.apresentacao_participante import ApresentacaoParticipanteModel

parser = reqparse.RequestParser()
parser.add_argument('titulo', required=True)
parser.add_argument('horaInicio', required=True)
parser.add_argument('horaFim', required=True)
parser.add_argument('trilha', type=dict, required=True)
parser.add_argument('sala', type=dict, required=True)
parser.add_argument('cronograma', type=dict, required=True)
parser.add_argument('participantes', type=dict, required=False, action='append')

'''
    Recursos de Apresentação.
'''
class ApresentacoesResource(Resource):
    # GET /apresentacoes
    @auth.login_required
    @marshal_with(apresentacao_campos)
    def get(self):
        current_app.logger.info("Get - Apresentações")
        apresentacoes = ApresentacaoModel.query\
            .order_by(ApresentacaoModel.titulo)\
            .filter_by(is_deleted=False)\
            .all()
        return apresentacoes, 200

    # POST /apresentacoes
    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Apresentação")
        try:
            # Parser
            args = parser.parse_args()
            titulo = args['titulo']
            hora_inicio = args['horaInicio']
            hora_fim = args['horaFim']
            # Se dict, get ID
            trilha_id = args['trilha']['id']
            sala_id = args['sala']['id']
            cronograma_id = args['cronograma']['id']
            evento_id = args['cronograma']['evento']['id']

            # Recovering existing resources
            trilha = TrilhaModel.query.filter_by(id=trilha_id).first()
            sala = SalaModel.query.filter_by(id=sala_id).first()
            cronograma = CronogramaModel.query.filter_by(id=cronograma_id).first()

            # Verifications
            # If ID was sent but theres no object in database ABORT.
            if trilha is None:
                erro = ErrorModel(1, "Trilha informada não existe.", "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404
            if sala is None:
                erro = ErrorModel(1, "Sala informada não existe.", "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404
            if cronograma is None:
                erro = ErrorModel(1, "Cronograma informado não existe.", "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404


            # Constraits
            # Trilha exists in Crongrama -> Evento]
            evento_trilha = EventoTrilhaModel.query.\
                filter(EventoTrilhaModel.evento_id == evento_id,
                       EventoTrilhaModel.trilha_id == trilha_id).all()

            if not evento_trilha:
                erro = ErrorModel(1, "A trilha precisa ser associada ao evento.", "Retornar 404 por não encontrar recurso")
                return marshal(erro, error_campos), 404

            # Sala is free
            '''
            isfree = isSalaFree(sala_id=sala_id,
                                hora_inicio=hora_inicio,
                                hora_fim=hora_fim,
                                cronograma_id=cronograma_id)

            if isfree is False:
                erro = ErrorModel(1, "Sala %s não está livre neste horário." % sala.nome, "Retornar 409 por conflito no recurso.")
                return marshal(erro, error_campos), 409
            '''

            apresentacao = ApresentacaoModel(titulo,
                                             hora_inicio,
                                             hora_fim,
                                             sala=sala,
                                             trilha=trilha,
                                             cronograma=cronograma)
            db.session.add(apresentacao)
            db.session.commit()

            if args['participantes'] is not None:
                participantes_ids = [ participante['id'] for participante in args['participantes']]
                participantes=[]
                for participante_id in participantes_ids:
                    participante = ParticipanteModel.query.filter_by(id=participante_id).first()
                    if participante is None:
                        erro = ErrorModel(1, "Participante informado não existe.", "Retornar 404 por não encontrar recurso")
                        return marshal(erro, error_campos), 404
                    else:
                        participantes.append(participante)
                # Adicionando participantes
                for participante in participantes:
                    apresentacaoParticipante = ApresentacaoParticipanteModel(apresentacao, participante)
                    db.session.add_all(apresentacaoParticipante)
                    db.session.commit()

        except exc.IntegrityError as err:
            current_app.logger.error(err)
            erro = ErrorModel(1,
                              "Erro de integridade no banco de dados, consulte o adminstrador",
                              err.__cause__())

            return marshal(erro, error_campos), 500

        return 204


class ApresentacaoResource(Resource):
    # GET /apresentacao/<apresentacao_id>
    @auth.login_required
    @marshal_with(apresentacao_campos)
    def get(self, apresentacao_id):
        current_app.logger.info("Get - Apresentação: %s" % apresentacao_id)
        apresentacao = ApresentacaoModel.query.filter_by(id=apresentacao_id).first()
        if apresentacao is None:
            abort(404, message='Apresentação {} nao existe'.format(apresentacao_id))
        return apresentacao, 200


    # PUT /apresentacao/<apresentacao_id>
    @auth.login_required
    def put(self, apresentacao_id):
        current_app.logger.info("Put - Apresentação: %s" % apresentacao_id)
        try:
            # Parser
            args = parser.parse_args()
            titulo = args['titulo']
            hora_inicio = args['horaInicio']
            hora_fim = args['horaFim']
            # Se dict, get ID
            trilha_id = args['trilha']['id'] if args['trilha']['id'] else None
            sala_id = args['sala']['id'] if args['sala']['id'] else None
            cronograma_id = args['cronograma']['id'] if args['cronograma']['id'] else None

            # Recovering existing resources
            trilha = TrilhaModel.query.filter_by(id=trilha_id).first()
            sala = SalaModel.query.filter_by(id=sala_id).first()
            cronograma = CronogramaModel.query.filter_by(id=cronograma_id).first()

            # Verifications
            # If ID was sent but theres no object in database ABORT.
            if trilha is None:
                abort(404, message='Trilha {} nao existe'.format(trilha_id))
            if sala is None:
                abort(404, message='Sala {} nao existe'.format(sala_id))
            if cronograma is None:
                abort(404, message='Cronograma {} nao existe'.format(cronograma_id))

            # Constraits
            # Trilha exists in Crongrama -> Evento]
            evento_id = cronograma.evento_id
            evento_trilha = EventoTrilhaModel.query. \
                filter(EventoTrilhaModel.evento_id == evento_id,
                       EventoTrilhaModel.trilha_id == trilha_id).all()

            if not evento_trilha:
                abort(404, message='Trilha {} nao pertence ao evento {}'.format(trilha_id, evento_id))

            # Sala is free
            '''
            isfree = isSalaFree(sala_id=sala_id,
                                hora_inicio=hora_inicio,
                                hora_fim=hora_fim,
                                apresentacao_id=apresentacao_id,
                                cronograma_id=cronograma_id)

            if isfree is False:
                abort(409, message='Sala {} nao está livre'.format(sala_id))            
            '''

            ApresentacaoModel.query\
                .filter_by(id=apresentacao_id)\
                .update(dict(titulo=titulo,
                             hora_inicio=hora_inicio,
                             hora_fim=hora_fim,
                             sala_id=sala_id,
                             trilha_id=trilha_id,
                             cronograma_id=cronograma_id))
            db.session.commit()

        except exc.SQLAlchemyError as e:
            current_app.logger.error("Exceção: " + e.__str__())
            erro = ErrorModel(5, "Ocoreu um erro interno e será solucionado. Tente novamente mais tarde.", "Exceção")
            return marshal(erro, error_campos), 500

        return 204

    # DELETE /apresentacao/<id>
    @auth.login_required
    def delete(self, apresentacao_id):
        current_app.logger.info("Delete - Apresentacao: %s:" % apresentacao_id)
        try:
            ApresentacaoModel.query \
                .filter_by(id=apresentacao_id) \
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError as e:
            current_app.logger.error("Exceção: " + e.__str__())
            erro = ErrorModel(5, "Ocoreu um erro interno e será solucionado. Tente novamente mais tarde.", "Exceção")
            return marshal(erro, error_campos), 500

        return 204


def isSalaFree(sala_id, hora_inicio, hora_fim, cronograma_id, apresentacao_id=0):
    apresentacoes = ApresentacaoModel.query \
        .filter(ApresentacaoModel.id != apresentacao_id) \
        .filter(ApresentacaoModel.sala_id == sala_id) \
        .filter(or_(and_(ApresentacaoModel.hora_inicio < hora_fim, ApresentacaoModel.hora_fim > hora_fim),
                    and_(ApresentacaoModel.hora_inicio < hora_inicio, ApresentacaoModel.hora_fim > hora_inicio))) \
        .all()

    # Verifica se dentro das apresentações dentro daquele horário e sala
    # Existe alguma outra com mesmo cronograma
    for apresentacao in apresentacoes:
        if apresentacao.cronograma_id == cronograma_id:
            return False

    return True

class ApresentacaoAutoresResource(Resource):
    # GET /apresentacoes/<apresentacao_id>/autores
    @auth.login_required
    @marshal_with(autor_campos)
    def get(self, apresentacao_id):
        current_app.logger.info("Get - Apresentação: %s" % apresentacao_id)
        autores = AutorModel.query\
        .filter(AutorModel.apresentacao_id==apresentacao_id).filter_by(is_deleted=False).all()
        return autores, 200


class BuscaApresentacoesNomeResource(Resource):
    @auth.login_required
    @marshal_with(apresentacao_campos)
    def get(self, apresentacao_nome):
        current_app.logger.info("Get - Apresentacoes por nome")
        apresentacao = ApresentacaoModel.query.filter(ApresentacaoModel.titulo.ilike('%'+apresentacao_nome+'%')).all()
        return apresentacao, 200