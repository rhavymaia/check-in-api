from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from common.settings import *
from common.logging import *
from resources.usuarios import *
from resources.participantes import *
from resources.eventos import *
from resources.evento_participante import *
from resources.cronogramas import *
from resources.trilhas import *
from resources.apresentacoes import *
from resources.apresentacao_participantes import *
from resources.sala import *
from resources.predio import *
from resources.autores import *


import importador

app = Flask(__name__)

# Settings
app.config['DEBUG'] = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_BINDS'] = SQLALCHEMY_BINDS

# Configure logging
handler = logging.FileHandler(LOGGING_LOCATION)
handler.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter(LOGGING_FORMAT)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

db.init_app(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/checkin/api')

# Recursos
api.add_resource(ApresentacaoParticipantesResource, '/apresentacao/<apresentacao_id>/participantes')

api.add_resource(ApresentacaoParticipanteResource, '/apresentacao/<apresentacao_id>/participante/<participante_id>')
api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(LoginResource, '/login')

api.add_resource(ParticipantesResource, '/participantes')
api.add_resource(ParticipanteResource, '/participantes/<participante_id>')
api.add_resource(BuscaParticipantesNomeResource, '/participantes/busca/<participante_nome>')

api.add_resource(ApresentacoesResource, '/apresentacoes')
api.add_resource(ApresentacaoResource, '/apresentacoes/<apresentacao_id>')
api.add_resource(BuscaApresentacoesNomeResource, '/apresentacoes/busca/<apresentacao_nome>')
api.add_resource(ApresentacaoAutoresResource, '/apresentacoes/<apresentacao_id>/autores')

api.add_resource(CronogramasResource, '/cronogramas')
api.add_resource(CronogramaResource, '/cronogramas/<cronograma_id>')
api.add_resource(BuscaCronogramasNomeResource, '/cronogramas/busca/<cronograma_nome>')

api.add_resource(EventoParticipantesResource, '/eventos/<evento_id>/participantes')
api.add_resource(EventoParticipanteResource, '/eventos/<evento_id>/participantes/<participante_id>')

api.add_resource(EventosResource, '/eventos')
api.add_resource(BuscaEventosNomeResource, '/eventos/busca/<evento_nome>')
api.add_resource(EventoResource, '/eventos/<evento_id>')
api.add_resource(EventoApresentacoesResource, '/eventos/<evento_id>/apresentacoes')
api.add_resource(EventoApresentacoesNomeResource, '/eventos/<evento_id>/apresentacoes/titulo/<titulo>')
api.add_resource(EventoCronogramasResource, '/eventos/<evento_id>/cronogramas')
api.add_resource(EventoCronogramaResource, '/eventos/<evento_id>/cronogramas/<cronograma_id>')
api.add_resource(EventoTrilhasResource, '/eventos/<evento_id>/trilhas')
api.add_resource(EventoTrilhaResource, '/eventos/<evento_id>/trilhas/<trilha_id>')
api.add_resource(EventoCronogramaTrilhaApresentacoesResource, '/eventos/<evento_id>/cronogramas/<cronograma_id>/trilhas/<trilha_id>/apresentacoes')
api.add_resource(EventoCronogramaApresentacoesResource, '/eventos/<evento_id>/cronogramas/<cronograma_id>/apresentacoes')

api.add_resource(EventoPrediosResource, '/eventos/<evento_id>/predios')
api.add_resource(EventoPredioResource, '/eventos/<evento_id>/predios/<predio_id>')

api.add_resource(SalasResource, '/salas')
api.add_resource(SalaResource, '/salas/<sala_id>')
api.add_resource(SalasNomeResource, '/salas/nome/<nome>')

api.add_resource(TrilhasResource, '/trilhas')
api.add_resource(TrilhaResource, '/trilhas/<trilha_id>')
api.add_resource(BuscaTrilhasNomeResource, '/trilhas/busca/<trilha_nome>')

api.add_resource(PrediosResource, '/predios')
api.add_resource(PredioResource, '/predios/<predio_id>')
api.add_resource(PredioSalasResource, '/predios/<predio_id>/salas')
api.add_resource(PrediosNomeResource, '/predios/nome/<nome>')

api.add_resource(AutoresResource, '/autores')
api.add_resource(AutorResource, '/autores/<autor_id>')
api.add_resource(BuscaAutorNomeResource, '/autores/busca/<autor_nome>')


# Blueprints para Restful.
app.register_blueprint(api_bp)

# CORS - requisição multi-clients
cors = CORS(app, resources={r"/checkin/api/*": {"origins": "*"}})

# Importação dos dados do OCS.
@app.cli.command()
def importar_ocs():
    importador.run()

if __name__ == '__main__':
    app.run(threaded=True)
