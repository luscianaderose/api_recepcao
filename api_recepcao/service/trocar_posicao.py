from api_recepcao.repository.pessoa_repo import buscar_pessoa_por_numero
from api_recepcao.repository.fila_repo import (
    alterar_posicao_pessoa,
)
from api_recepcao.repository.pessoa_repo import buscar_pessoas_por_fila_atividade
from api_recepcao.service.entity_service import (
    buscar_pessoas_fila_com_posicao_por_atividade,
)


def trocar_posicao(numero_pessoa1, numero_pessoa2, ignorar_duplas=False):
    print(numero_pessoa1, numero_pessoa2)
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

    if numero_pessoa1 not in pessoas_fila or numero_pessoa2 not in pessoas_fila:
        raise Exception("Não foi possível mover!")
    if numero_pessoa2 < numero_pessoa1:
        return trocar_posicao(numero_pessoa2, numero_pessoa1, ignorar_duplas)

    if (
        not ignorar_duplas
        and pessoa1.dupla_numero != numero_pessoa2
        and (pessoa1.dupla_numero or pessoa2.dupla_numero)
    ):
        if (
            pessoa1.dupla_numero and pessoa2.dupla_numero
        ):  # p1+p2 tem dupla. Se tiver dupla e se for trocar com alguem que nao é a propria dupla
            trocar_posicao(numero_pessoa1, pessoa2.dupla, ignorar_duplas=True)
            trocar_posicao(pessoa1.dupla, numero_pessoa2, ignorar_duplas=True)
        elif not pessoa1.dupla_numero:  # somente a p1 tem dupla
            trocar_posicao(numero_pessoa1, numero_pessoa2, ignorar_duplas=True)
            trocar_posicao(numero_pessoa1, pessoa1.dupla, ignorar_duplas=True)
        elif not pessoa2.dupla_numero:  # somente a p2 tem dupla
            trocar_posicao(numero_pessoa1, numero_pessoa2, ignorar_duplas=True)
            trocar_posicao(numero_pessoa2, pessoa2.dupla, ignorar_duplas=True)
        return

    if pessoa1.dupla_numero:
        pessoa_dupla = buscar_pessoa_por_numero(pessoa1.dupla_numero)
        pessoa_dupla.dupla_numero = numero_pessoa2
    if pessoa2.dupla_numero:
        pessoa_dupla = buscar_pessoa_por_numero(pessoa2.dupla_numero)
        pessoa_dupla.dupla_numero = numero_pessoa1

    alterar_posicao_pessoa(numero_pessoa1=pessoa1.numero, numero_pessoa2=pessoa2.numero)

    # posicao_pessoa1 = None
    # posicao_pessoa2 = None

    # for posicao, pessoa in buscar_pessoas_fila_com_posicao_por_atividade(
    #     pessoa1.fila_atividade
    # ).items():
    #     if pessoa.numero == numero_pessoa1:
    #         posicao_pessoa1 = posicao
    #     elif pessoa.numero == numero_pessoa2:
    #         posicao_pessoa2 = posicao

    # alterar_posicao_pessoa(
    #     fila_atividade=pessoa1.fila_atividade,
    #     posicao=posicao_pessoa1,
    #     pessoa_numero=numero_pessoa2,
    # )

    # alterar_posicao_pessoa(
    #     fila_atividade=pessoa2.fila_atividade,
    #     posicao=posicao_pessoa2,
    #     pessoa_numero=numero_pessoa1,
    # )
