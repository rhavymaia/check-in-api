from flask_restful import Resource, marshal_with, abort, reqparse, current_app, marshal
from flask import request
from sqlalchemy import exc
from common.auth import auth
from common.database import db
from models.cronograma import CronogramaModel, cronograma_campos
from models.evento import EventoModel, evento_campos
from models.predio import PredioModel, predio_campos
from models.predio_evento import EventoPredioModel
from models.trilha import TrilhaModel, trilha_campos
from models.trilha_evento import EventoTrilhaModel
from models.apresentacao import ApresentacaoModel, apresentacao_campos, apresentacao_participantes_campos
from models.error import error_campos, ErrorModel
import datetime
from datetime import timedelta

parser = reqparse.RequestParser()
parser.add_argument('nome', required=True)
parser.add_argument('inicio', required=True)
parser.add_argument('fim', required=True)


'''
    Eventos.
'''


class EventosResource(Resource):
    # GET /eventos
    @marshal_with(evento_campos)
    def get(self):
        current_app.logger.info("Get - Eventos")
        eventos = EventoModel.query\
            .order_by(EventoModel.data_inicio)\
            .filter_by(is_deleted=False)\
            .all()
        return eventos, 200

    # POST /eventos
    @auth.login_required
    def post(self):
        current_app.logger.info("Post - Eventos")
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Evento: %s:" % (args))

            # Evento
            nome = args['nome']
            data_inicio = args['inicio']
            data_fim = args['fim']
            evento = EventoModel(nome, data_inicio, data_fim)

            # Criação do Evento.
            db.session.add(evento)
            db.session.commit()

        except exc.SQLAlchemyError as err:
            current_app.logger.error(err)
            return 409

        return 204


class BuscaEventosNomeResource(Resource):
    # GET /eventos/busca/<nome_do_evento>
    @marshal_with(evento_campos)
    def get(self, evento_nome):
        current_app.logger.info("Get - Eventos por nome")
        eventos = EventoModel.query.filter(EventoModel.nome.ilike('%'+evento_nome+'%')).all()
        return eventos, 200


'''
    Evento.
'''


class EventoResource(Resource):
    # GET /eventos/<id>
    @marshal_with(evento_campos)
    def get(self, evento_id):
        current_app.logger.info("Get - Evento: %s" % evento_id)
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        return evento, 200

    # PUT /eventos/<id>
    @auth.login_required
    def put(self, evento_id):
        current_app.logger.info("Put - Evento: %s:" % evento_id)
        try:
            # Parser JSON
            args = parser.parse_args()
            current_app.logger.info("Evento: %s:" % args)

            # Dados para atualização.
            nome = args['nome']
            data_inicio = args['inicio']
            data_fim = args['fim']

            EventoModel.query\
                .filter_by(id=evento_id)\
                .update(dict(nome=nome, data_inicio=data_inicio, data_fim=data_fim))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")

        return 204

    # DELETE /eventos/<id>
    @auth.login_required
    def delete(self, evento_id):
        current_app.logger.info("Delete - Evento: %s" % evento_id)
        try:
            EventoModel.query\
                .filter_by(id=evento_id)\
                .update(dict(is_deleted=True))
            db.session.commit()

        except exc.SQLAlchemyError:
            current_app.logger.error("Exceção")
            return 404

        return 204


'''
    Cronogramas de um Evento.
'''


class EventoCronogramasResource(Resource):
    # GET /eventos/<id>/cronogramas
    @marshal_with(cronograma_campos)
    def get(self, evento_id):
        current_app.logger.info("Get - Cronogramas - Evento: %s" % evento_id)
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))

        cronogramas = CronogramaModel.query\
            .order_by(CronogramaModel.data_realizacao)\
            .filter_by(evento_id=evento_id)\
            .filter_by(is_deleted=False)\
            .all()
        return cronogramas, 200

'''
    Cronograma de um Evento.
'''


class EventoCronogramaResource(Resource):
    # POST /eventos/<evento_id>/cronogramas/<cronograma_id>
    @auth.login_required
    def post(self, evento_id, cronograma_id):
        current_app.logger.info("Post - Cronograma: %s - Evento: %s" % (cronograma_id, evento_id))
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        cronograma = CronogramaModel.query.filter_by(id=cronograma_id).first()
        if cronograma is None:
            abort(404, message='cronograma {} nao existe'.format(cronograma_id))

        # Criação do Cronograma no Evento.
        evento_cronograma = CronogramaModel(evento, cronograma)
        db.session.add(evento_cronograma)
        db.session.commit()

        return 204

    # PUT /eventos/<evento_id>/cronogramas/<cronograma_id>
    @auth.login_required
    def put(self, evento_id, cronograma_id):
        current_app.logger.info("Update - Cronograma: %s - Evento: %s" % (cronograma_id, evento_id))
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        cronograma = CronogramaModel.query.filter_by(id=cronograma_id).first()
        if cronograma is None:
            abort(404, message='cronograma {} nao existe'.format(cronograma_id))

        # Atualizar cronograma
        current_app.logger.info("Updated - Cronograma: %s - Evento: %s:" % (cronograma_id, evento_id))
        CronogramaModel.query.filter_by(id=cronograma_id).\
            update(dict(evento_id=evento_id))
        db.session.commit()

    # DELETE /eventos/<evento_id>/cronogramas/<cronograma_id>
    @auth.login_required
    def delete(self, evento_id, cronograma_id):
        current_app.logger.info("Delete - Cronograma: %s - Evento: %s:" % (cronograma_id, evento_id))
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        cronograma = CronogramaModel.query.filter_by(id=cronograma_id).first()
        if cronograma is None:
            abort(404, message='cronograma {} nao existe'.format(cronograma_id))

        # Remove cronograma do evento
        current_app.logger.info("Deleted - Cronograma: %s - Evento: %s:" % (cronograma_id, evento_id))
        CronogramaModel.query.filter_by(id=cronograma_id)\
            .update(dict(is_deleted=True))
        db.session.commit()

'''
    Trilhas de um Evento.
'''


class EventoTrilhasResource(Resource):
    # GET /eventos/<evento_id>/trilhas
    @marshal_with(trilha_campos)
    def get(self, evento_id):
        current_app.logger.info("Get - Trilhas - Evento: %s" % evento_id)
        evento_trilhas = EventoTrilhaModel.query.filter_by(evento_id=evento_id).all()
        trilhas = []
        for evento_trilha in evento_trilhas:
            trilha = evento_trilha.trilha
            trilhas.append(trilha)
        return trilhas, 200


'''
    Trilha de um Evento.
'''


class EventoTrilhaResource(Resource):
    # GET /eventos/<evento_id>/trilhas/<trilha_id>
    @marshal_with(trilha_campos)
    def get(self, evento_id, trilha_id):
        evento_trilha = EventoTrilhaModel.query.filter_by(
            evento_id=evento_id, trilha_id=trilha_id).first()
        trilha = evento_trilha.trilha
        return trilha, 200

    # POST /eventos/<evento_id>/trilhas/<trilha_id>
    @auth.login_required
    def post(self, evento_id, trilha_id):

        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))

        trilha = TrilhaModel.query.filter_by(id=trilha_id).first()
        if trilha is None:
            abort(404, message='Trilha {} nao existe'.format(trilha_id))

        et_exists = EventoTrilhaModel.query\
            .filter(EventoTrilhaModel.evento_id == evento_id)\
            .filter(EventoTrilhaModel.trilha_id == trilha_id)\
            .first()
        if et_exists:
            erro = ErrorModel(409, "A associação entre trilha e evento já existe.", "Conflito no recurso")
            return marshal(erro, error_campos), 409

        # Criação da Trilha no Evento.
        evento_trilha = EventoTrilhaModel(evento, trilha)
        db.session.add(evento_trilha)
        db.session.commit()

        return 204

    # DELETE /eventos/<evento_id>/trilhas/<trilha_id>
    @auth.login_required
    def delete(self, evento_id, trilha_id):
        current_app.logger.info("Delete - Cronograma: %s - Evento: %s:" % (evento_id, trilha_id))

        et = EventoTrilhaModel.query \
            .filter(EventoTrilhaModel.evento_id == evento_id) \
            .filter(EventoTrilhaModel.trilha_id == trilha_id) \
            .first()

        db.session.delete(et)
        db.session.commit()

        return 204
'''
    Apresentacoes de um Evento
'''
class EventoApresentacoesResource(Resource):
    # GET /eventos/<evento_id>/apresentacoes
    @marshal_with(apresentacao_participantes_campos)
    def get(self, evento_id):
        current_app.logger.info("Get - Apresentacoes - Evento: %s"
                                % (evento_id))
       
        apresentacoes = (db.session.query(ApresentacaoModel)
                         .join(CronogramaModel, CronogramaModel.id == ApresentacaoModel.cronograma_id)
                         .join(EventoModel, EventoModel.id == CronogramaModel.evento_id)
                         .join(TrilhaModel, TrilhaModel.id == ApresentacaoModel.trilha_id)
                         .filter(EventoModel.id == evento_id)
                         .order_by(ApresentacaoModel.hora_inicio, TrilhaModel.nome, ApresentacaoModel.titulo)
                         .all())

        return apresentacoes, 200


'''
    Apresentacoes de um Evento por nome
'''


class EventoApresentacoesNomeResource(Resource):
    # GET /eventos/<evento_id>/apresentacoes/titulo/<titulo>
    @marshal_with(apresentacao_participantes_campos)
    def get(self, evento_id, titulo):
        current_app.logger.info("Get - Apresentacoes - Evento: %s"
                                % (evento_id))

        apresentacoes = (db.session.query(ApresentacaoModel)
                         .join(CronogramaModel, CronogramaModel.id == ApresentacaoModel.cronograma_id)
                         .join(EventoModel, EventoModel.id == CronogramaModel.evento_id)
                         .join(TrilhaModel, TrilhaModel.id == ApresentacaoModel.trilha_id)
                         .filter(EventoModel.id == evento_id)
                         .filter(ApresentacaoModel.titulo.ilike('%' + titulo + '%'))
                         .order_by(ApresentacaoModel.hora_inicio, TrilhaModel.nome, ApresentacaoModel.titulo)
                         .all())

        return apresentacoes, 200

'''
    Prédios de um Evento
'''
class EventoPrediosResource(Resource):
    # GET /eventos/<evento_id>/predios
    @marshal_with(predio_campos)
    def get(self, evento_id):
        current_app.logger.info("Get - Predios - Evento: %s" % evento_id)
        evento_predios = EventoPredioModel.query.filter_by(evento_id=evento_id).all()
        predios = []
        for evento_predio in evento_predios:
            predio = evento_predio.predio
            predios.append(predio)
        return predios, 200


'''
    Prédio de um Evento.
'''


class EventoPredioResource(Resource):
    # GET /eventos/<evento_id>/predios/<predio_id>
    @marshal_with(predio_campos)
    def get(self, evento_id, predio_id):
        evento_predio = EventoPredioModel.query.filter_by(
            evento_id=evento_id, predio_id=predio_id).first()
        predio = evento_predio.predio
        return predio, 200

    # POST /eventos/<evento_id>/predios/<predio_id>
    @auth.login_required
    def post(self, evento_id, predio_id):
        evento = EventoModel.query.filter_by(id=evento_id).first()
        if evento is None:
            abort(404, message='Evento {} nao existe'.format(evento_id))
        predio = PredioModel.query.filter_by(id=predio_id).first()
        if predio is None:
            abort(404, message='Predio {} nao existe'.format(predio_id))

        # Criação do Prédio no Evento.
        evento_predio = EventoPredioModel(evento, predio)
        db.session.add(evento_predio)
        db.session.commit()

        return 204

    # DELETE /eventos/<evento_id>/predios/<predio_id>
    @auth.login_required
    def delete(self, evento_id, predio_id):
        current_app.logger.info("Delete - Cronograma: %s - Evento: %s:" % (evento_id, predio_id))

        PredioModel.query.filter_by(id=predio_id)\
            .update(dict(is_deleted=True))
        db.session.commit()

        return 204

class EventoCronogramaTrilhaApresentacoesResource(Resource):
    # GET /eventos/<evento_id>/cronogramas/<cronograma_id>/trilhas/<trilha_id>/apresentacoes
    @marshal_with(apresentacao_participantes_campos)
    def get(self, evento_id, cronograma_id, trilha_id):
        agora = request.args.get('agora', default=False, type=bool)
        current_app.logger.info("Get - Apresentacoes - Evento: %s:, Cronograma: %s, Trilha: %s, Agora: %s"
                                % (evento_id, cronograma_id, trilha_id, agora))
        # Verificar Apresentações por Evento, Cronograma e Trilha
        if (agora):
            # Data de hoje
            hoje = datetime.date.today()
            # Hora atual e hora com previão de 2 horas.
            horaAtual = datetime.datetime.now()
            horaPrevisaoAnterior = (horaAtual - timedelta(hours=1)).time()
            horaPrevisaoPosterior = (horaAtual + timedelta(hours=3)).time()
            current_app.logger.info("Hoje: %s" % hoje)
            current_app.logger.info("Previsão - Anterior: %s" % (horaPrevisaoAnterior))
            current_app.logger.info("Previsão - Posterior: %s" % (horaPrevisaoPosterior))

            # Verificar Apresentações por Evento, Cronograma e Trilha
            apresentacoes = (db.session.query(ApresentacaoModel)
                             .join(CronogramaModel, CronogramaModel.id == ApresentacaoModel.cronograma_id)
                             .join(EventoModel, EventoModel.id == CronogramaModel.evento_id)
                             .join(TrilhaModel, TrilhaModel.id == ApresentacaoModel.trilha_id)
                             .filter(EventoModel.id == evento_id,
                                     CronogramaModel.id == cronograma_id,
                                     TrilhaModel.id == trilha_id,
                                     # Cronograma para a data de hoje.
                                     CronogramaModel.data_realizacao == hoje,
                                     # Horário de inicio e fim
                                     ApresentacaoModel.hora_inicio >= horaPrevisaoAnterior,
                                     ApresentacaoModel.hora_fim <= horaPrevisaoPosterior)
                             .order_by(ApresentacaoModel.hora_inicio, TrilhaModel.nome, ApresentacaoModel.titulo)
                             .all())
        else:
            apresentacoes = (db.session.query(ApresentacaoModel)
                             .join(CronogramaModel, CronogramaModel.id == ApresentacaoModel.cronograma_id)
                             .join(EventoModel, EventoModel.id == CronogramaModel.evento_id)
                             .join(TrilhaModel, TrilhaModel.id == ApresentacaoModel.trilha_id)
                             .filter(EventoModel.id == evento_id,
                                     CronogramaModel.id == cronograma_id,
                                     TrilhaModel.id == trilha_id)
                             .order_by(ApresentacaoModel.hora_inicio, TrilhaModel.nome, ApresentacaoModel.titulo)
                             .all())

        return apresentacoes, 200


class EventoCronogramaApresentacoesResource(Resource):
    # GET /eventos/<evento_id>/cronogramas/<cronograma_id>/apresentacoes
    @marshal_with(apresentacao_participantes_campos)
    def get(self, evento_id, cronograma_id):
        agora = request.args.get('agora', default=False, type=bool)
        current_app.logger.info("Get - Apresentacoes Agora - Evento: %s:, Cronograma: %s, Agora: %s"
                                % (evento_id, cronograma_id, agora))
        apresentacoes = []
        # Verificar Apresentações por Evento, Cronograma e Trilha
        if (agora):
            # Data de hoje
            hoje = datetime.date.today()
            # Hora atual e hora com previão de 2 horas.
            horaAtual = datetime.datetime.now()
            horaPrevisaoAnterior = (horaAtual - timedelta(hours=1)).time()
            horaPrevisaoPosterior = (horaAtual + timedelta(hours=3)).time()
            current_app.logger.info("Hoje: %s" % hoje)
            current_app.logger.info("Previsão - Anterior: %s" % (horaPrevisaoAnterior))
            current_app.logger.info("Previsão - Posterior: %s" % (horaPrevisaoPosterior))

            # Verificar Apresentações por Evento e Cronograma que estão acontecendo nesse momento.
            apresentacoes = (db.session.query(ApresentacaoModel)
                             .join(CronogramaModel, CronogramaModel.id == ApresentacaoModel.cronograma_id)
                             .join(EventoModel, EventoModel.id == CronogramaModel.evento_id)
                             .join(TrilhaModel, TrilhaModel.id == ApresentacaoModel.trilha_id)
                             .filter(EventoModel.id == evento_id,
                                     CronogramaModel.id == cronograma_id,
                                     # Cronograma para a data de hoje.
                                     CronogramaModel.data_realizacao == hoje,
                                     # Horário de inicio e fim
                                     ApresentacaoModel.hora_inicio >= horaPrevisaoAnterior,
                                     ApresentacaoModel.hora_fim <= horaPrevisaoPosterior)
                             .order_by(ApresentacaoModel.hora_inicio, TrilhaModel.nome, ApresentacaoModel.titulo)
                             .all())
        else:
            # Verificar Apresentações por Evento e Cronograma
            apresentacoes = (db.session.query(ApresentacaoModel)
                             .join(CronogramaModel, CronogramaModel.id == ApresentacaoModel.cronograma_id)
                             .join(EventoModel, EventoModel.id == CronogramaModel.evento_id)
                             .join(TrilhaModel, TrilhaModel.id == ApresentacaoModel.trilha_id)
                             .filter(EventoModel.id == evento_id,
                                     CronogramaModel.id == cronograma_id)
                             .order_by(ApresentacaoModel.hora_inicio, TrilhaModel.nome, ApresentacaoModel.titulo)
                             .all())

        return apresentacoes, 200