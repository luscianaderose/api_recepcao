from flask import Flask, request
from flask_cors import CORS
from datetime import datetime, date, timedelta

from api_recepcao.database.conf.setup import setup_db
from api_recepcao.entities.camara import Camara
from api_recepcao.entities.pessoa import Pessoa
from api_recepcao.service.fila_service import get_filas, get_fila, salvar_fila
from api_recepcao.service.camara_service import get_dict_camaras, salvar_camara
from api_recepcao.service.pessoa_service import (
    get_pessoa,
    get_dict_pessoas,
    get_pessoa_com_posicao,
    salvar_pessoa,
    get_pessoas_fila,
    get_todas_pessoas_com_posicao,
    add_pessoa,
    deletar_pessoa,
)
from api_recepcao.service.chamar_atendido import chamar_atendido
from api_recepcao.service.trocar_posicao import trocar_posicao
from api_recepcao.service.dupla_service import criar_dupla, cancelar_dupla


#setup_db()

set_camaras_chamando = set()
set_audios_notificacoes = set()


def get_data_hora_atual():
    dias_da_semana = (
        "SEGUNDA",
        "TERÇA",
        "QUARTA",
        "QUINTA",
        "SEXTA",
        "SÁBADO",
        "DOMINGO",
    )
    dia_semana = date.today().weekday()
    data_e_hora_atuais = datetime.utcnow() + timedelta(hours=-3)
    dia_semana_usar = dias_da_semana[dia_semana]
    data_e_hora_em_texto = data_e_hora_atuais.strftime("%d %B %H:%M").upper()
    return dia_semana_usar + " " + data_e_hora_em_texto


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Bem Vindo(a) à API Recepção"


# Deveria estar na api de calendário
@app.route("/calendario")
def calendario():
    return {
        "data_e_hora": get_data_hora_atual(),
    }


@app.route("/pessoas")
def pessoas():
    return {pessoa.numero: pessoa.to_dict() for pessoa in get_dict_pessoas().values()}


@app.route("/pessoas/<numero_pessoa>")
def pessoa(numero_pessoa):
    return get_pessoa(numero_pessoa=numero_pessoa).to_dict()


@app.route("/camaras")
def camaras():
    return {camara.numero: camara.to_dict() for camara in get_dict_camaras().values()}


@app.route("/abrir_camara/<numero_camara>")
def abrir_camara(numero_camara):
    camara = get_dict_camaras()[numero_camara]
    camara.abrir()
    salvar_camara(camara)
    return camara.to_dict()


@app.route("/chamar_proximo/<numero_camara>")
def chamar_proximo(numero_camara):
    camara = get_dict_camaras()[numero_camara]
    if camara.estado == camara.atendendo:
        chamar_atendido(camara.numero)
        set_camaras_chamando.add(camara)
        global ultima_camara_chamada
        ultima_camara_chamada = camara
        camara = get_dict_camaras()[numero_camara]
    return (
        camara.pessoa_em_atendimento.to_dict() if camara.pessoa_em_atendimento else {}
    )


@app.route("/avisado/<numero_camara>")
def avisado(numero_camara):
    camara = get_dict_camaras()[numero_camara]
    if camara.estado == camara.avisar:
        camara.estado = camara.avisado
        salvar_camara(camara)
    return camara.to_dict() if camara else {}


@app.route("/fechar_camara/<numero_camara>")
def fechar_camara(numero_camara):
    camara = get_dict_camaras()[numero_camara]
    if camara.estado == camara.avisado:
        camara.estado = camara.fechada
        camara.pessoa_em_atendimento = None
        salvar_camara(camara)
    return camara.to_dict() if camara else {}


@app.route("/bolinhas")
def bolinhas():
    modo = request.args.get("modo")
    numero_camara = request.args.get("numero_camara")
    camara = get_dict_camaras()[numero_camara]
    if modo == "adicao" and camara.numero_de_atendimentos < camara.capacidade_maxima:
        camara.numero_de_atendimentos += 1
        if camara.numero_de_atendimentos >= camara.capacidade_maxima:
            camara.estado = camara.avisar
    elif modo == "subtracao" and camara.numero_de_atendimentos > 0:
        if camara.estado != camara.atendendo:
            camara.estado = camara.atendendo
        camara.numero_de_atendimentos -= 1
    salvar_camara(camara)
    return camara.to_dict() if camara else {}


@app.route("/deschamar/<numero_camara>")
def deschamar(numero_camara):
    camara = get_dict_camaras()[numero_camara]

    if not camara.pessoa_em_atendimento:
        return f"A câmara {numero_camara} não está atendendo ninguém."

    pessoa = camara.pessoa_em_atendimento
    pessoa.estado = Pessoa.aguardando
    pessoa.numero_camara = None
    salvar_pessoa(pessoa)

    if pessoa.dupla_numero:
        # pessoa_dupla = camara.fila.get(pessoa.dupla_numero)
        pessoa_dupla = get_pessoa(pessoa.dupla_numero)
        pessoa_dupla.estado = pessoa_dupla.aguardando
        pessoa_dupla.numero_camara = None
        salvar_pessoa(pessoa_dupla)

    for pessoa in get_pessoas_fila(pessoa.fila_atividade)[::-1]:
        if pessoa.estado == pessoa.riscado and pessoa.numero_camara == numero_camara:
            pessoa.estado = pessoa.atendendo
            if pessoa.dupla_numero:
                pessoa_dupla = camara.fila.get(pessoa.dupla_numero)
                pessoa_dupla.estado = pessoa_dupla.atendendo
                salvar_pessoa(pessoa=pessoa_dupla)
            camara.pessoa_em_atendimento = pessoa

            salvar_pessoa(pessoa=pessoa)
            salvar_camara(camara=camara)
            break
    else:
        camara.pessoa_em_atendimento = None
    camara.numero_de_atendimentos -= 1
    camara.estado = camara.atendendo
    salvar_camara(camara=camara)
    return camara.to_dict() if camara else {}


@app.route("/aumentar_capacidade/<numero_camara>")
def aumentar_capacidade(numero_camara):
    camara = get_dict_camaras()[numero_camara]
    if camara.capacidade_maxima < 20:
        camara.capacidade_maxima += 1
        if camara.estado != camara.atendendo and camara.numero_de_atendimentos > 0:
            camara.estado = camara.atendendo
    salvar_camara(camara=camara)
    return camara.to_dict() if camara else {}


@app.route("/diminuir_capacidade/<numero_camara>")
def diminuir_capacidade(numero_camara):
    camara = get_dict_camaras()[numero_camara]
    if camara.capacidade_maxima > 3:
        camara.capacidade_maxima -= 1
        if (
            camara.estado == camara.atendendo
            and camara.numero_de_atendimentos >= camara.capacidade_maxima
        ):
            camara.estado = camara.avisar
    salvar_camara(camara=camara)
    return camara.to_dict() if camara else {}


@app.route("/reiniciar_tudo")
def reiniciar_tudo_confirmado():
    for camara in get_dict_camaras().values():
        camara.numero_de_atendimentos = 0
        camara.fechar()
        camara.capacidade_maxima = 5
        salvar_camara(camara=camara)

    for fila in get_filas().values():
        fila.clear()
        for pessoa in get_pessoas_fila(fila_atividade=fila.atividade):
            deletar_pessoa(pessoa_numero=pessoa.numero)
        salvar_fila(fila=fila)
    return "reiniciado"


@app.route("/fila_videncia")
def fun_fila_videncia():
    return get_fila("videncia").to_dict()


@app.route("/fila_prece")
def fun_fila_prece():
    return get_fila("prece").to_dict()


@app.route("/editar_atendido")
def editar_atendido_confirmado():
    numero_atendido = int(request.args.get("numero_atendido"))
    nome_atendido = request.args.get("nome_atendido")
    pessoa = get_pessoa(numero_pessoa=numero_atendido)
    pessoa.nome = nome_atendido
    salvar_pessoa(pessoa=pessoa)
    return pessoa.to_dict()


@app.route("/remover_atendido")
def remover_atendido_confirmado():
    numero_atendido = int(request.args.get("numero_atendido"))
    deletar_pessoa(pessoa_numero=numero_atendido)
    return f"Atendido {numero_atendido} removido"


@app.route("/reposicionar_atendido")
def reposicionar_atendido():
    numero_atendido = int(request.args.get("numero_atendido"))
    mover_para = request.args.get("mover_para")

    pessoa_fila = get_pessoa_com_posicao(numero_pessoa=numero_atendido)
    pessoas_fila = get_todas_pessoas_com_posicao(pessoa_fila.fila_atividade)

    # print("numero_atendido", numero_atendido)
    # print("pessoa_fila", pessoa_fila)
    # print("pessoas_fila", pessoas_fila)
    # print("posicao_pessoa_anterior", pessoa_fila.posicao - 1)
    # print("posicao_pessoa_anterior", pessoas_fila[pessoa_fila.posicao - 1])

    # return ""

    if mover_para == "cima":
        posicao_pessoa_anterior = pessoa_fila.posicao - 1
        if posicao_pessoa_anterior >= 1:
            trocar_posicao(
                numero_atendido, pessoas_fila[posicao_pessoa_anterior].numero
            )
        else:
            return f"Atendido {numero_atendido} não pode ser movido para cima"
    elif mover_para == "baixo":
        posicao_pessoa_posterior = pessoa_fila.posicao + 1
        if posicao_pessoa_posterior < len(pessoas_fila.keys()):
            trocar_posicao(
                numero_atendido, pessoas_fila[posicao_pessoa_posterior].numero
            )

    return "Atendido Reposicionado"


@app.route("/criar_dupla")
def fun_criar_dupla():
    numero_dupla = int(request.args.get("numero_dupla"))
    numero_atendido = int(request.args.get("numero_atendido"))
    criar_dupla(numero_dupla, numero_atendido)
    return "Dupla Criada"


@app.route("/cancelar_dupla")
def fun_cancelar_dupla():
    numero_atendido = int(request.args.get("numero_atendido"))
    cancelar_dupla(numero_atendido)
    return "Dupla cancelada"


@app.route("/adicionar_atendido")
def adicionar_atendido():
    nome_fila = request.args.get("nome_fila")
    nome_atendido = request.args.get("nome_atendido")

    fila = get_fila(nome_fila)
    if fila:
        pessoa = Pessoa(numero=None, nome=nome_atendido, fila_atividade=fila.atividade)
        pessoa = add_pessoa(pessoa=pessoa)
    return pessoa.to_dict() or {}


@app.route("/observacao")
def observacao():
    numero_atendido = int(request.args.get("numero_atendido"))
    observacao = request.args.get("observacao")

    pessoa = get_pessoa(numero_pessoa=numero_atendido)
    pessoa.observacao = observacao
    salvar_pessoa(pessoa=pessoa)

    return pessoa.to_dict() or {}


@app.route("/desriscar")
def desriscar():
    nome_fila = request.args.get("nome_fila")
    numero_atendido = int(request.args.get("numero_atendido"))

    pessoas_fila = [
        pessoa.numero for pessoa in get_pessoas_fila(fila_atividade=nome_fila)
    ]

    print(pessoas_fila)
    if numero_atendido in pessoas_fila:
        pessoa = get_pessoa(numero_pessoa=numero_atendido)
        pessoa.estado = pessoa.aguardando
        pessoa.numero_camara = None
        if pessoa.dupla_numero:
            pessoa_dupla = get_pessoa(numero_pessoa=pessoa.dupla_numero)
            pessoa_dupla.estado = Pessoa.aguardando
            pessoa_dupla.numero_camara = None
            salvar_pessoa(pessoa=pessoa_dupla)
        salvar_pessoa(pessoa=pessoa)
        return f"Pessoa {numero_atendido} desrriscada"
    return "Não foi possível desriscar esse nome!"


# app.run(port=5001, debug=True)
