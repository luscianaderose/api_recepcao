from api_recepcao.database.modelos.fila_modelo import FilaModelo, fila_pessoa
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao
from api_recepcao.entities.fila import Fila
from api_recepcao.repository.pessoa_repo import (
    buscar_pessoas_fila_com_posicao_por_atividade,
    buscar_pessoas_fila_com_posicao,
)


def from_db_to_fila(db_fila: FilaModelo):
    return Fila(
        atividade=db_fila.atividade,
        nome_display=db_fila.nome_display,
        proximo_numero=db_fila.proximo_numero,
        fila=buscar_pessoas_fila_com_posicao_por_atividade(db_fila.atividade),
    )


def criar_fila(atividade, nome_display, pessoas=[]):
    sessao = criar_sessao()
    camara = FilaModelo(atividade=atividade, nome_display=nome_display, pessoas=pessoas)
    sessao.add(camara)
    sessao.commit()
    fechar_sessao(sessao)


def buscar_todas_filas():
    sessao = criar_sessao()
    filas = [from_db_to_fila(db_fila) for db_fila in sessao.query(FilaModelo).all()]
    fechar_sessao(sessao)
    return filas


def buscar_fila_por_atividade(atividade):
    sessao = criar_sessao()
    fila = from_db_to_fila(
        sessao.query(FilaModelo).filter(FilaModelo.atividade == atividade).one_or_none()
    )
    fechar_sessao(sessao)
    return from_db_to_fila(fila)


def atualizar_fila(fila):
    sessao = criar_sessao()
    db_fila = (
        sessao.query(FilaModelo)
        .filter(FilaModelo.atividade == fila.atividade)
        .one_or_none()
    )
    if db_fila:
        db_fila.atividade = fila.atividade
        db_fila.nome_display = fila.nome_display
        db_fila.proximo_numero = fila.proximo_numero
    sessao.commit()
    fechar_sessao(sessao)


def deletar_fila_por_atividade(atividade):
    sessao = criar_sessao()
    fila = (
        sessao.query(FilaModelo).filter(FilaModelo.atividade == atividade).one_or_none()
    )
    if fila:
        sessao.delete(fila)
        sessao.commit()
    #     print(f"A fila {atividade} foi deletada com sucesso!")
    # else:
    #     print(f"A fila {atividade} não existe no banco de dados!")


def popular_filas(filas=[("videncia", "Vidência"), ("prece", "Prece")]):
    sessao = criar_sessao()
    db_filas = sessao.query(FilaModelo).all()
    if not db_filas:
        for atividade, nome_display in filas:
            fila = FilaModelo(
                atividade=atividade, nome_display=nome_display, pessoas=[]
            )
            sessao.add(fila)
            # print(f"Adicionando fila {atividade}.")
        sessao.commit()
    fechar_sessao(sessao)


def alterar_posicao_pessoa(numero_pessoa1, numero_pessoa2):
    sessao = criar_sessao()

    fila_pessoa1 = buscar_pessoas_fila_com_posicao(numero_pessoa1)
    fila_pessoa2 = buscar_pessoas_fila_com_posicao(numero_pessoa2)

    sessao.query(fila_pessoa).filter(
        fila_pessoa.c.pessoa_numero == numero_pessoa1,
    ).update({"posicao": fila_pessoa2.posicao})

    sessao.query(fila_pessoa).filter(
        fila_pessoa.c.pessoa_numero == numero_pessoa2,
    ).update({"posicao": fila_pessoa1.posicao})

    sessao.commit()
    fechar_sessao(sessao)


# def alterar_posicao_pessoa(fila_atividade, posicao, pessoa_numero):
#     sessao = criar_sessao()

#     pessoa_fila = (
#         sessao.query(fila_pessoa)
#         .filter(
#             fila_pessoa.c.fila_atividade == fila_atividade,
#             fila_pessoa.c.posicao == posicao,
#         )
#         .one_or_none()
#     )

#     if pessoa_fila:
#         sessao.query(fila_pessoa).filter(
#             fila_pessoa.c.fila_atividade == fila_atividade,
#             fila_pessoa.c.pessoa_numero == pessoa_fila.pessoa_numero,
#         ).update({"posicao": -1})

#     sessao.query(fila_pessoa).filter(
#         fila_pessoa.c.fila_atividade == fila_atividade,
#         fila_pessoa.c.pessoa_numero == pessoa_numero,
#     ).update({"posicao": posicao})
#     sessao.commit()
#     fechar_sessao(sessao)


def remover_pessoa_da_fila(pessoa_numero, fila_atividade):
    sessao = criar_sessao()
    db_fila = (
        sessao.query(FilaModelo)
        .filter(FilaModelo.atividade == fila_atividade)
        .one_or_none()
    )
    if db_fila:
        pessoa_fila = (
            sessao.query(fila_pessoa)
            .filter(
                fila_pessoa.c.fila_atividade == fila_atividade,
                fila_pessoa.c.pessoa_numero == pessoa_numero,
            )
            .one_or_none()
        )
        if pessoa_fila:
            # sessao.delete(pessoa_fila)
            delete_stmt = fila_pessoa.delete().where(
                fila_pessoa.c.fila_atividade == fila_atividade,
                fila_pessoa.c.pessoa_numero == pessoa_numero,
            )
            sessao.execute(delete_stmt)
            sessao.commit()
    fechar_sessao(sessao)
