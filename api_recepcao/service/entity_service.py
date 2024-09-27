# from api_recepcao.repository.pessoa_repo import buscar_pessoa_por_numero
# from api_recepcao.repository.camara_repo import buscar_camara_por_numero
from api_recepcao.repository.pessoa_repo import (
    buscar_pessoas_por_fila_atividade,
    from_db_to_pessoa,
)

from api_recepcao.entities.pessoa import Pessoa

# from api_recepcao.entities.camara import Camara
# from api_recepcao.entities.fila import Fila


def buscar_pessoas_fila_com_posicao_por_atividade(atividade) -> dict[int, Pessoa]:
    pessoas = buscar_pessoas_por_fila_atividade(atividade)
    pessoas_com_posicao = {}
    for pessoa in pessoas:
        pessoas_com_posicao[pessoa.numero] = from_db_to_pessoa(pessoa)
    return pessoas_com_posicao


# def from_db_to_fila(atividade: str):
#     db_fila = buscar_fila_por_atividade(atividade=atividade)
#     if db_fila:
#         return Fila(
#             atividade=db_fila.atividade,
#             nome_display=db_fila.nome_display,
#             proximo_numero=db_fila.proximo_numero,
#         )
#     return None


# def from_db_to_camara(numero: str):
#     db_camara = buscar_camara_por_numero(numero=numero)
#     if db_camara:
#         return Camara(
#             numero=db_camara.numero,
#             estado=db_camara.estado,
#             capacidade_maxima=db_camara.capacidade_maxima,
#             fila=db_camara.fila_atividade,
#         )
#     return None


# def from_db_to_pessoa(db_pessoa: PessoaModelo):
#     return Pessoa(
#         numero=db_pessoa.numero,
#         nome=db_pessoa.nome,
#         estado=db_pessoa.estado,
#         dupla=db_pessoa.dupla,
#         observacao=db_pessoa.observacao,
#         numero_camara=db_pessoa.numero_camara,
#     )
