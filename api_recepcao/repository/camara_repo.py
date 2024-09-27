"""Camada intermediaria de abstracao entre o modelo CamaraModelo e a classe Camara"""

from api_recepcao.database.modelos.camara_modelo import CamaraModelo
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao
from api_recepcao.entities.camara import Camara
from api_recepcao.entities.fila import Fila
from api_recepcao.repository.pessoa_repo import buscar_pessoa_por_numero


def from_db_to_camara(db_camara: CamaraModelo) -> Camara:
    return Camara(
        numero=db_camara.numero,
        estado=db_camara.estado,
        capacidade_maxima=db_camara.capacidade_maxima,
        numero_de_atendimentos=db_camara.numero_de_atendimentos,
        pessoa_em_atendimento=(
            buscar_pessoa_por_numero(db_camara.pessoa_em_atendimento)
            if db_camara.pessoa_em_atendimento
            else None
        ),
        fila_atividade=db_camara.fila_atividade,
    )


def criar_camara_modelo(numero):
    sessao = criar_sessao()
    camara = CamaraModelo(numero=numero)
    sessao.add(camara)
    sessao.commit()
    fechar_sessao(sessao)


def buscar_todas_camaras():
    sessao = criar_sessao()
    lista_camaras = [
        from_db_to_camara(camara) for camara in sessao.query(CamaraModelo).all()
    ]
    fechar_sessao(sessao)
    return lista_camaras


def buscar_camara_por_numero(numero):
    sessao = criar_sessao()
    camara = from_db_to_camara(
        sessao.query(CamaraModelo).filter(CamaraModelo.numero == numero).one_or_none()
    )
    fechar_sessao(sessao)
    return camara


def deletar_camara_por_numero(numero):
    sessao = criar_sessao()
    camara = (
        sessao.query(CamaraModelo).filter(CamaraModelo.numero == numero).one_or_none()
    )
    if camara:
        sessao.delete(camara)
        sessao.commit()
    #     print(f"Câmara {numero} deletada com sucesso!") # TODO isso deve retornar OK ou NOK ao inves de print
    # else:
    #     print(f"A câmara {numero} não existe no banco de dados!")


def popular_camaras(
    camaras=[("2", "videncia"), ("4", "videncia"), ("3", "prece"), ("3A", "prece")]
):
    sessao = criar_sessao()
    db_camaras = sessao.query(CamaraModelo).all()
    if not db_camaras:
        for numero, fila_atividade in camaras:
            camara = CamaraModelo(numero=numero, fila_atividade=fila_atividade)
            sessao.add(camara)
            # print(f"Adicionando camara {numero}.")
        sessao.commit()
    fechar_sessao(sessao)


def atualizar_camara(camara):
    try:
        sessao = criar_sessao()
        db_camara = (
            sessao.query(CamaraModelo)
            .filter(CamaraModelo.numero == camara.numero)
            .one_or_none()
        )
        if db_camara:
            db_camara.numero = camara.numero
            db_camara.estado = camara.estado
            db_camara.numero_de_atendimentos = camara.numero_de_atendimentos
            db_camara.capacidade_maxima = camara.capacidade_maxima
            db_camara.pessoa_em_atendimento = (
                camara.pessoa_em_atendimento.numero
                if camara.pessoa_em_atendimento
                else None
            )
            db_camara.fila_atividade = camara.fila_atividade
        sessao.commit()
        fechar_sessao(sessao)
    except ZeroDivisionError as e:
        print(f"Erro: {e}")
