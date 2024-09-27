from api_recepcao.repository.pessoa_repo import (
    atualizar_pessoa,
    buscar_pessoa_por_numero,
)
from api_recepcao.repository.fila_repo import (
    buscar_fila_por_atividade,
)
from api_recepcao.service.entity_service import buscar_pessoas_por_fila_atividade
from api_recepcao.entities.pessoa import Pessoa


def criar_dupla(numero_pessoa1: int, numero_pessoa2: int):
    pessoa1 = buscar_pessoa_por_numero(numero_pessoa1)
    pessoa2 = buscar_pessoa_por_numero(numero_pessoa2)

    if pessoa1.fila_atividade != pessoa2.fila_atividade:
        raise Exception(
            f"Pessoa {numero_pessoa1} e pessoa {numero_pessoa2} não pertecem à mesma fila"
        )

    pessoas_fila = [
        pessoa.numero
        for pessoa in buscar_pessoas_por_fila_atividade(pessoa1.fila_atividade)
    ]

    if pessoa1 and pessoa2:
        if pessoa1.numero not in pessoas_fila or pessoa2.numero not in pessoas_fila:
            raise Exception("Não foi possível criar dupla!")

        if pessoa1.dupla_numero is not None or pessoa2.dupla_numero is not None:
            raise Exception("Não é possível criar dupla com uma pessoa de outra dupla!")

        if pessoa1.estado != Pessoa.aguardando or pessoa2.estado != Pessoa.aguardando:
            raise Exception(
                "Não é possível criar dupla depois que a pessoa já foi chamada!"
            )

        pessoa1.dupla_numero = pessoa2.numero
        pessoa2.dupla_numero = pessoa1.numero

        atualizar_pessoa(pessoa=pessoa1)
        atualizar_pessoa(pessoa=pessoa2)


def cancelar_dupla(numero_pessoa):
    pessoa = buscar_pessoa_por_numero(numero_pessoa)
    fila_pessoa1 = buscar_fila_por_atividade(pessoa.fila_atividade)

    if pessoa and fila_pessoa1:
        pessoas_fila = [
            pessoa.numero
            for pessoa in buscar_pessoas_por_fila_atividade(pessoa.fila_atividade)
        ]
        if pessoa.numero not in pessoas_fila:
            raise Exception("Não foi possível cancelar a dupla!")

        pessa_dupla = buscar_pessoa_por_numero(pessoa.dupla_numero)

        pessoa.dupla_numero = None
        pessa_dupla.dupla_numero = None

        atualizar_pessoa(pessoa=pessoa)
        atualizar_pessoa(pessoa=pessa_dupla)
