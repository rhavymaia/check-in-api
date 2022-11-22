from flask_restful import current_app
from ftfy import fix_text
from models.ocs import *
from models.evento import EventoModel
from models.participante import ParticipanteModel
from models.participante_evento import *
from models.predio import *
from models.autor import AutorModel
from models.sala import *
from models.predio_evento import *
from models.apresentacao import *
from models.apresentacao_participante import ApresentacaoParticipanteModel
from models.trilha import *
from models.modalidade import *
from common.database import db
import datetime
import string

ID_VAZIO = 0
PAPER_APROVADO = 3
TRILHA_TRABALHO = 1

def myfilter(name):
    def func(x):
        return x.setting_name == name
    return func


def correct_date(value):
    result = None
    if value is not None:
        try:
            result = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except:
            result = datetime.datetime.strptime(value, '%d-%m-%Y %H:%M:%S')
    return result

def correct_decode(value):
    try:
        result = fix_text(value)
    except:
        result = value
    return result


def get_setting_by_name(name, settings):
    res = list(filter(myfilter(name), settings))
    if not res and len(res)==0:
        return None
    value = res[0].setting_value
    if isinstance(value, str):
        result = correct_decode(value)
    elif isinstance(value, datetime):
        result = correct_date(res[0].setting_value)
    else:
        result = res[0].setting_value
    return result

'''
    Importar os Eventos do OCS.
    Etapa 1 - 1º Passo.
'''

def salvar_evento(conf):
    settings = conf.settings.all()
    nome = get_setting_by_name('title', settings)
    data_inicio = correct_date(get_setting_by_name('startDate', settings))
    data_fim = correct_date(get_setting_by_name('endDate', settings))
    ocs_conferencia_id = conf.conference_id
    ocs_evento_id = conf.sched_conf_id
    # Evento
    evento = EventoModel(nome, data_inicio, data_fim, ocs_conferencia_id, ocs_evento_id)
    db.session.add(evento)
    db.session.commit()
    current_app.logger.info("Salvando EventoModel: %s" % (evento))
    return evento

'''
    Importar tipos de participantes inscritos em Eventos do OCS.
    Etapa 1 - 2º Passo.
'''

def salvar_papeis(registrationTypes: RegistrationTypesModel, evento: EventoModel):
    for registrationType in registrationTypes:
        current_app.logger.info("Importando RegistrationTypesModel: %d" % (registrationType.type_id))
        tipo_participante_existente = TipoParticipanteEventoModel.query.filter_by(id=registrationType.type_id).first()
        if (tipo_participante_existente is None):
            settings = registrationType.settings.all()
            ocs_tipo_participante_id = registrationType.type_id
            nome = get_setting_by_name('name', settings)
            tipo_participante = TipoParticipanteEventoModel(nome, evento.id,
                    ocs_tipo_participante_id=ocs_tipo_participante_id)
            db.session.add(tipo_participante)
            db.session.commit()
            current_app.logger.info("Salvando TipoParticipante: %s" % (tipo_participante))

'''
    Importar participantes inscritos em Eventos do OCS.
    Etapa 1 - 3º Passo.
'''

def salvar_participantes(conf: SchedConfsModel, evento: EventoModel):

    for registration in conf.registrations:
        current_app.logger.info("Importando RegistrationsModel: %d" % (
            registration.registration_id))
        participante = ParticipanteModel.query.filter_by(
            ocs_participante_id=registration.user.user_id).first()
        if (participante is None):
            if registration.user.middle_name:
                nome = '{} {} {}'.format(registration.user.first_name,
                                         registration.user.middle_name,
                                         registration.user.last_name)
            else:
                nome = '{} {}'.format(registration.user.first_name,
                                      registration.user.last_name)
            # Participante.
            nome = string.capwords(correct_decode(nome))
            cpf = registration.user.cpf
            email = registration.user.email
            ocs_participante_id = registration.user.user_id
            participante = ParticipanteModel(nome, cpf, email, ocs_participante_id=ocs_participante_id)
        # Tipo do Participante.
        ocs_tipo_participante_id = registration.type_id
        tipoParticipanteEvento = TipoParticipanteEventoModel.query.filter_by(
            ocs_tipo_participante_id=ocs_tipo_participante_id).first()
        # Participante do Evento.
        participante_evento = ParticipanteEventoModel(participante, evento, tipoParticipanteEvento)
        db.session.add(participante_evento)
        db.session.commit()
        current_app.logger.info("Salvando ParticipanteEventoModel: %s" % (participante_evento))

'''
    Importar Prédios e Salas dos Eventos do OCS.
    Etapa 1 - 4º Passo.
'''

def salvar_predios(conf: SchedConfsModel, evento: EventoModel):
    # Listar prédios
    buildings = BuildingsModel.query.filter_by(
        sched_conf_id=conf.sched_conf_id)
    for building in buildings:
        current_app.logger.info("Importando BuildingsModel: %s" % (building))
        settings = building.settings.all()
        nome = get_setting_by_name('name', settings)
        descricao = get_setting_by_name('description', settings)
        ocs_predio_id = building.building_id
        # Prédio
        predio = PredioModel(nome, descricao, ocs_predio_id)
        db.session.add(predio)
        db.session.commit()
        current_app.logger.info("Salvando PredioModel: %s" % (predio))
        # Prédio e Evento
        if (predio is not None):
            # Criação do Prédio no Evento.
            evento_predio = EventoPredioModel(evento, predio)
            db.session.add(evento_predio)
            db.session.commit()
            current_app.logger.info("Salvando EventoPredioModel: %s" % (evento_predio))
            # Salas
            rooms = RoomsModel.query.filter_by(building_id=predio.ocs_predio_id)
            for room in rooms:
                current_app.logger.info("Importando RoomsModel: %s" % (room))
                settings = room.settings.all()
                nome = get_setting_by_name('name', settings)
                descricao = get_setting_by_name('description', settings)
                # Sala
                sala = SalaModel(nome, descricao, predio, ocs_sala_id = room.room_id)
                db.session.add(sala)
                db.session.commit()
                current_app.logger.info("Salvando SalaModel: %s" % (sala))

'''
    Importar Trabalhos dos Eventos do OCS.
    Etapa 2 - 1º Passo.
'''
def salvar_paper(paper: PapersModel):
    current_app.logger.info("Importando Paper: %s" % (paper))
    settings = paper.settings.all()
    # Verificar se o paper foi aprovado para publicação.
    if paper.status >= PAPER_APROVADO:
        # Título
        cleanTitle = string.capwords(get_setting_by_name('cleanTitle', settings))
        # Conferência OCS
        schedConfId = paper.sched_conf_id
        # Trabalho publicado
        publishPaper = PublishedPapersModel.query.filter_by(
            paper_id=paper.paper_id).first()
        if publishPaper is not None:
            current_app.logger.info("Importando PublishedPapersModel: %s" % (publishPaper))
            # Verificar se apresentação já foi incluida.
            apresentacao = ApresentacaoModel.query.filter_by(ocs_pub_id=publishPaper.pub_id).first()
            if apresentacao is None:
                # Sala
                room = RoomsModel.query.filter_by(
                    room_id=publishPaper.room_id).first()
                if room is not None:
                    current_app.logger.info("Importando RoomsModel: %s" % (room))
                    # Cronograma - O cronograma já deve existir no checkin.
                    evento = EventoModel.query.filter_by(
                        ocs_evento_id=schedConfId).first()
                    cronograma = getCronograma(evento.cronogramas, paper.start_time)
                    # Sala
                    sala = SalaModel.query.filter_by(
                        ocs_sala_id=room.room_id).first()
                    # Hora de inicio e fim.
                    startTime = paper.start_time
                    endTime = paper.end_time
                    # Trilha
                    trilha = TrilhaModel.query.filter_by(id=TRILHA_TRABALHO).first()
                    # Participante, Sala, Hora de inicio e fim.
                    apresentacao = ApresentacaoModel(cleanTitle, startTime, endTime,
                                                     cronograma=cronograma,
                                                     trilha=trilha,
                                                     sala=sala,
                                                     ocs_pub_id = publishPaper.pub_id)
                    db.session.add(apresentacao)
                    db.session.commit()
                    current_app.logger.info("Salvando ApresentacaoModel: %s" % (apresentacao))
                    # Primeiro Autor.
                    user = UserModel.query.filter_by(
                        user_id=paper.user_id).first()
                    current_app.logger.info("Importando UserModel: %s" % (user))
                    # Procurar participante cadastrado no Evento.
                    participante = ParticipanteModel.query.filter_by(ocs_participante_id=user.user_id).first()
                    if participante is None:
                        nomeParticipante = getNomeCompleto(user)
                        participante = ParticipanteModel(nomeParticipante, user.cpf,
                                                         user.email, user.user_id)
                        db.session.add(participante)
                        db.session.commit()
                        current_app.logger.info("Salvando ParticipanteModel - não inscrito no evento: %s" % (participante))
                    # Apresentação e Participante - Autor principal.
                    apresentacaoParticipante = ApresentacaoParticipanteModel(
                        apresentacao, participante)
                    db.session.add(apresentacaoParticipante)
                    db.session.commit()
                    current_app.logger.info("Salvando ApresentacaoParticipanteModel: %s"
                                            % (apresentacaoParticipante))
                    # Co-autores.
                    authors = PaperAuthorsModel.query.filter_by(
                        paper_id=paper.paper_id).all()
                    for author in authors:
                        current_app.logger.info("Importando PaperAuthorsModel: %s" % (author))
                        nomeAutor = getNomeCompleto(author)
                        autor = AutorModel(nomeAutor, author.email, apresentacao, author.author_id)
                        current_app.logger.info("Autor: %s" % (autor))
                        db.session.add(autor)
                        db.session.commit()
                        current_app.logger.info("Salvando AutorModel: %s" % (autor))
            else:
                current_app.logger.info("Apresentação já existente.")

def getCronograma(cronogramas: list, hora_inicio: datetime):
    cronogramaSelecionado = None
    for cronograma in cronogramas:
        dataRealizacao = cronograma.data_realizacao
        startDateTime = hora_inicio
        if (dataRealizacao.date() == startDateTime.date()):
            current_app.logger.info("Cronograma definido: %s" % (cronograma))
            cronogramaSelecionado = cronograma
            break
    return cronogramaSelecionado

def getNomeCompleto(autor):
    return string.capwords(correct_decode("%s %s %s" % (autor.first_name, autor.middle_name,
                                        autor.last_name)))
def isEventoFuturo(conf):
    isFuturo = False
    settings = conf.settings.all()
    data_inicio = correct_date(get_setting_by_name('startDate', settings))
    if data_inicio is not None:

        isFuturo = data_inicio.date() >= datetime.date.today()
        current_app.logger.info("Evento Futuro - %s, %s" % (data_inicio.date(), isFuturo))
    return isFuturo

'''
    Menu da Importação dos dados do OCS.
'''

def exibir_menu():
    print('''
    Opções:
        1 - Importar: Eventos, Participantes, Prédios e Salas;
        2 - Importar: Apresentações e autores (Executar a opção 1 como primeiro passo);
        3 - Sair
    ''')

def salvar_trilhas(evento: EventoModel):
    tracks = TracksModel.query.filter_by(sched_conf_id=evento.ocs_evento_id)\
        .all()
    for track in tracks:
        current_app.logger.info("Importando TracksModel: %s" % (track))
        settings = track.settings.all()
        nome = get_setting_by_name('title', settings)
        modalidade = ModalidadeModel(nome, evento, track.track_id)
        db.session.add(modalidade)
        db.session.commit()
        current_app.logger.info("Salvando Modalidade: %s" % (modalidade))

'''
    Importar Eventos, Participantes, Prédios e Salas.
'''

def opcao1():
    current_app.logger.info("Importação - OCS-Checkin: Eventos, Participantes, Prédios e Salas")
    sched_confs = SchedConfsModel.query.all()
    for conf in sched_confs:
        current_app.logger.info("Importando SchedConfs: %d" % (conf.sched_conf_id))
        # Novos Eventos em OCS.
        if (isEventoFuturo(conf)):
            # Verificar existência do Evento em Checkin.
            evento = EventoModel.query.filter_by(
                ocs_evento_id=conf.sched_conf_id).first()
            if (evento is None):
                # Evento.
                evento = salvar_evento(conf)
                # Trilhas
                salvar_trilhas(evento)
                # Tipos de participantes.
                registration_types = RegistrationTypesModel.query.filter_by(sched_conf_id=conf.sched_conf_id).all()
                salvar_papeis(registration_types, evento)
                papeis = TipoParticipanteEventoModel.query.filter_by(
                    evento_id=evento.id).first()
                if (papeis is not None):
                    # Participantes
                    salvar_participantes(conf, evento)
                # Prédios e Salas
                salvar_predios(conf, evento)
            else:
                current_app.logger.info("Evento já existente.")

'''
    Importar Apresentações e autores.
'''

def opcao2():
    current_app.logger.info("Importação - OCS-Checkin: Apresentações e autores")
    agora = datetime.datetime.now()
    # Eventos incluidos na primeira etapa da importação.
    eventos = EventoModel.query\
        .filter(EventoModel.data_inicio>=agora).all()
    for evento in eventos:
        sched_conf = SchedConfsModel.query.filter_by(sched_conf_id=evento.ocs_evento_id).first()
        if (sched_conf is not None):
            # Trabalhos/Apresentações do OCS
            papers = PapersModel.query.filter_by(
                sched_conf_id=sched_conf.sched_conf_id).all()
            for paper in papers:
                salvar_paper(paper)
def run():
    continuar = True
    while(continuar):
        try:
            exibir_menu()
            opcao = int(input("Digite a opção desejada:"))
            if(opcao == 1):
                opcao1()
            elif(opcao == 2):
                opcao2()
            elif (opcao == 3):
                continuar = False
            else:
                current_app.logger.info("Opção inválida!")
        except Exception as e:
            current_app.logger.error(e)