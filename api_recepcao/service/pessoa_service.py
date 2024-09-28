from api_recepcao.repository.pessoa_repo import (
    buscar_todas_pessoas,
    buscar_pessoa_por_numero,
    buscar_pessoas_por_fila_atividade,
    buscar_pessoas_fila_com_posicao,
    buscar_pessoas_fila_com_posicao_por_atividade,
    atualizar_pessoa,
    adicionar_pessoa,
    deletar_pessoa_por_numero,
)
from api_recepcao.entities.pessoa import Pessoa


def get_dict_pessoas():
    return {pessoa.numero: pessoa for pessoa in buscar_todas_pessoas()}


def get_pessoa(numero_pessoa):
    if numero_pessoa:
        return buscar_pessoa_por_numero(numero=numero_pessoa)


def get_pessoas_fila(fila_atividade):
    if fila_atividade:
        return buscar_pessoas_por_fila_atividade(atividade=fila_atividade)


def get_pessoa_com_posicao(numero_pessoa):
    if numero_pessoa and isinstance(numero_pessoa, int):
        return buscar_pessoas_fila_com_posicao(numero_pessoa=numero_pessoa)


def get_todas_pessoas_com_posicao(fila_atividade):
    if fila_atividade and isinstance(fila_atividade, str):
        return buscar_pessoas_fila_com_posicao_por_atividade(fila_atividade)


def salvar_pessoa(pessoa):
    if pessoa and isinstance(pessoa, Pessoa):
        atualizar_pessoa(pessoa=pessoa)


def add_pessoa(pessoa):
    if pessoa and isinstance(pessoa, Pessoa):
        return adicionar_pessoa(pessoa=pessoa)


def deletar_pessoa(pessoa_numero):
    if pessoa_numero and isinstance(pessoa_numero, int):
        deletar_pessoa_por_numero(numero=pessoa_numero)
