from api_recepcao.service.entity_service import (
    buscar_pessoas_fila_com_posicao_por_atividade,
)

from api_recepcao.repository.camara_repo import (
    buscar_camara_por_numero,
    atualizar_camara,
)
from api_recepcao.repository.pessoa_repo import (
    buscar_pessoa_por_numero,
    atualizar_pessoa,
)
from api_recepcao.entities.pessoa import Pessoa
from api_recepcao.entities.camara import Camara


def chamar_atendido(numero_camara):
    """Encontra a primeira pessoa da fila que não foi chamada, marca como chamada
    e adiciona a self.pessoa_em_atendimento. Caso a pessoa tenha uma dupla,
    a sua dupla também será marcada."""

    camara = buscar_camara_por_numero(numero_camara)

    if camara.estado != Camara.atendendo:
        return

    proxima_pessoa_para_atender: Pessoa = None
    posicao_pessoas_fila: dict[int, Pessoa] = (
        buscar_pessoas_fila_com_posicao_por_atividade(camara.fila_atividade)
    )

    for posicao, pessoa in posicao_pessoas_fila.items():
        if pessoa.estado == Pessoa.aguardando:
            proxima_pessoa_para_atender = pessoa
            break
    else:
        camara.estado = Camara.avisar
        atualizar_camara(camara=camara)

    if camara.pessoa_em_atendimento:
        camara.pessoa_em_atendimento.estado = Pessoa.riscado
        camara.pessoa_em_atendimento.numero_camara = camara.numero
        atualizar_camara(camara=camara)
        atualizar_pessoa(pessoa=camara.pessoa_em_atendimento)

        if camara.pessoa_em_atendimento.dupla_numero:
            pessoa_dupla = buscar_pessoa_por_numero(
                camara.pessoa_em_atendimento.dupla_numero
            )

            pessoa_dupla.estado = Pessoa.riscado
            pessoa_dupla.numero_camara = camara.numero
            atualizar_pessoa(pessoa=pessoa_dupla)

        # pessoa_em_atendimento = buscar_camara_por_numero()

    if proxima_pessoa_para_atender or camara.numero_de_atendimentos == 0:
        camara.pessoa_em_atendimento = proxima_pessoa_para_atender
        camara.numero_de_atendimentos += 1
        atualizar_camara(camara=camara)

        camara.pessoa_em_atendimento.numero_camara = camara.numero
        camara.pessoa_em_atendimento.estado = Pessoa.atendendo
        atualizar_pessoa(pessoa=camara.pessoa_em_atendimento)

        if camara.pessoa_em_atendimento.dupla_numero:
            pessoa_dupla = buscar_pessoa_por_numero(
                camara.pessoa_em_atendimento.dupla_numero
            )

            pessoa_dupla.estado = Pessoa.atendendo
            pessoa_dupla.numero_camara = camara.numero
            atualizar_pessoa(pessoa=pessoa_dupla)

            camara.numero_de_atendimentos += 1
            atualizar_camara(camara=camara)

    if camara.numero_de_atendimentos >= camara.capacidade_maxima:
        camara.estado = Camara.avisar
        atualizar_camara(camara=camara)
