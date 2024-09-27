from api_recepcao.repository.fila_repo import (
    buscar_todas_filas,
    buscar_fila_por_atividade,
    atualizar_fila,
)
from api_recepcao.entities.fila import Fila


def get_filas():
    return {fila.atividade: fila for fila in buscar_todas_filas()}


def get_fila(fila_atividade):
    if fila_atividade:
        return buscar_fila_por_atividade(atividade=fila_atividade)


def salvar_fila(fila):
    if fila and isinstance(fila, Fila):
        atualizar_fila(fila=fila)
