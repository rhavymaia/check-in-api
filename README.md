# Check-in

API de controle de entrada do portal de eventos do IFPB


### Resources
#### Eventos
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
OK | `/eventos/` | GET | Todos eventos
OK | `/eventos/` | POST | Novo evento.
OK | `/eventos/busca/<nome_do_evento>` | GET | Busca evento por nome.
OK | `/eventos/<evento_id>` | GET | Evento especifico.
OK | `/eventos/<evento_id>` | PUT | Atualiza um evento.
OK | `/eventos/<evento_id>` | DELETE | Desativa um evento.
OK | `/eventos/<evento_id>/cronomgrama` | GET | Cronogramas de um evento.
OK | `/eventos/<evento_id>/cronomgrama/<cronograma_id>` | POST | Associa o cronograma no evento.
OK | `/eventos/<evento_id>/cronomgrama/<cronograma_id>` | PUT | Edita cronograma no evento evento.
OK | `/eventos/<evento_id>/cronomgrama/<cronograma_id>` | DELETE | Desassocia cronograma no evento evento.
OK | `/eventos/<evento_id>/trilhas` | GET | Trilhas de um evento.
OK | `/eventos/<evento_id>/trilhas/<trilha_id>` | GET | Trilhas especifica.
OK | `/eventos/<evento_id>/trilhas/<trilha_id>` | POST | Adiciona uma trilha à um evento.
Not Tested | `/eventos/<evento_id>/cronogramas/<cronograma_id>/trilhas/<trilha_id>/apresentacoes` | GET | Todas apresentações em evento, cronograma e trilha especificadas pelo id.

#### Participantes
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
To refactor | `/participantes` | GET | Todos participantes (Filtra por CPF e por Nome)
OK | `/participantes` | POST | Novo participante.
OK | `/participantes/<participante_id>` | GET | Recupera Participante.
OK | `/participantes/<participante_id>` | PUT | Atualiza Participante.
OK | `/participantes/<participante_id>` | Delete | Desativa Participante.

#### EventoParticipante
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
To refactor | `/eventos/<evento_id>/participantes` | GET | Todos participantes do evento.
To refactor | `/eventos/<evento_id>/participantes` | POST | Associa participante (id via args) ao evento.
To refactor | `/eventos/<evento_id>/participantes/<participante_id>` | PUT | Faz o checkin do participante.

#### Cronogramas
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
OK | `/cronogramas` | GET | Todos cronogramas.
OK | `/cronogramas` | POST | Novo cronograma.
OK | `/cronogramas/<cronograma_id>` | GET | Recupera cronograma.
OK | `/cronogramas/<cronograma_id>` | PUT | Edita cronograma.
OK | `/cronogramas/<cronograma_id>` | DELETE | Desativa cronograma.

#### Trilhas
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
OK | `/trilhas` | GET | Todas Trilhas.
OK | `/trilhas` | POST | Nova Trilhas.
OK | `/trilhas/<trilha_id>` | GET | Recupera Trilha.
OK | `/trilhas/<trilha_id>` | PUT | Edita Trilha.
OK | `/trilhas/<trilha_id>` | DELETE | Desativa Trilha.
OK | `/trilhas/busca/<trilha_nome>''` | DELETE | Desativa Trilha.

#### Salas e Predios
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
OK | `/salas` | GET | Todas Salas.
OK | `/salas` | POST | Nova Sala.
OK | `/salas/<sala_id>` | GET | Recupera Sala.
OK | `/salas/<sala_id>` | PUT | Edita Sala.
OK | `/salas/<sala_id>` | DELETE | Desativa Sala.
OK | `/predios` | GET | Todos Prédios.
OK | `/predios` | POST | Novo Prédio.
OK | `/predios/<predio_id>` | GET | Recupera Prédio.
OK | `/predios/<predio_id>` | PUT | Edita Prédio.
OK | `/predios/<predio_id>` | DELETE | Desativa Prédio.

#### Apresentações
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
OK | `/apresentacoes` | GET | Todas Apresentações.
OK | `/apresentacoes` | POST | Nova Apresentação.
OK | `/apresentacoes/<apresentacao_id>` | GET | Recupera Apresentação.
OK | `/apresentacoes/<apresentacao_id>` | PUT | Edita Apresentação.
OK | `/apresentacoes/<apresentacao_id>` | DELETE | Desativa Apresentação.

#### ApresentaçãoParticipantes
Status | Endpoint | Method | Action
--------|--------|:--------:|-------
OK | `/apresentacoes/<apresentacao_id>/participantes` | GET | Todos participantes de uma apresentação.
To Do  | `/apresentacoes/<apresentacao_id>/participantes/<participante_id>` | POST | Associa um participante à uma apresentação.



### Instalação

Para a instalação, você precisa:

- Python >= 3.5
- MySQL

Criando o ambiente:
```sh
$ python -m venv .env
```
Ativando o ambiente para usar:
```sh
$ . .env/bin/activate
```
Instalando as dependências:
```sh
$ pip install -r requirements.txt
```
Criando o banco:
```sh
$ mysql -u<dbuser> -p<dbpwd> < sql/ddl.sql
```

Vamos criar as variáveis de ambiente com as credenciais do banco de dados:
```sh
$ export DB_USUARIO=<dbuser>
$ export DB_SENHA=<dbpwd>
```

Agora, vamos criar a variável de ambiente para rodar a API com o comando flask:
```sh
$ export FLASK_APP=app.py
* Execução Local
$ flask run
* Running on http://127.0.0.1:5000/
* Execução Externa
flask run -h 0.0.0.0 -p 5000
* Execução Interna
flask run -h 127.0.0.1 -p 5000
* Running on http://0.0.0.0:5000/
```
Debug Mode - não usar em produção
```sh
$ export FLASK_DEBUG=1
```
[Clique aqui](RESOURCES.md) para acessar a documentação da API