from sqlalchemy import func

from api_recepcao.database.modelos.pessoa_modelo import PessoaModelo
from api_recepcao.database.modelos.fila_modelo import FilaModelo, fila_pessoa
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao
from api_recepcao.entities.pessoa import Pessoa

# from api_recepcao.entities.fila import Fila


def from_db_to_pessoa(db_pessoa: PessoaModelo):
    return Pessoa(
        numero=db_pessoa.numero,
        nome=db_pessoa.nome,
        estado=db_pessoa.estado,
        dupla_numero=db_pessoa.dupla_numero,
        observacao=db_pessoa.observacao,
        numero_camara=db_pessoa.numero_camara,
        fila_atividade=db_pessoa.fila_atividade,
    )


def adicionar_pessoa(pessoa):
    sessao = criar_sessao()
    pessoa = PessoaModelo(
        nome=pessoa.nome,
        estado=pessoa.estado,
        dupla_numero=pessoa.dupla_numero,
        observacao=pessoa.observacao,
        fila_atividade=pessoa.fila_atividade,
    )
    sessao.add(pessoa)

    posicao = (
        sessao.query(func.max(fila_pessoa.c.posicao))
        .filter(fila_pessoa.c.fila_atividade == pessoa.fila_atividade)
        .scalar()
        or 0
    )
    posicao += 1

    nova_fila_pessoa = fila_pessoa.insert().values(
        posicao=posicao,
        fila_atividade=pessoa.fila_atividade,
        pessoa_numero=pessoa.numero,
    )
    sessao.execute(nova_fila_pessoa)

    sessao.commit()
    fechar_sessao(sessao)
    return from_db_to_pessoa(pessoa)


def atualizar_pessoa(pessoa):
    sessao = criar_sessao()
    db_pessoa = (
        sessao.query(PessoaModelo)
        .filter(PessoaModelo.numero == pessoa.numero)
        .one_or_none()
    )
    if db_pessoa:
        db_pessoa.numero = pessoa.numero
        db_pessoa.nome = pessoa.nome
        db_pessoa.dupla_numero = pessoa.dupla_numero
        db_pessoa.fila_atividade = pessoa.fila_atividade
        db_pessoa.estado = pessoa.estado
        db_pessoa.observacao = pessoa.observacao
        if pessoa.numero_camara:
            db_pessoa.numero_camara = pessoa.numero_camara
    sessao.commit()
    fechar_sessao(sessao)


def deletar_pessoa_por_numero(numero):
    sessao = criar_sessao()
    pessoa = (
        sessao.query(PessoaModelo).filter(PessoaModelo.numero == numero).one_or_none()
    )
    if pessoa:
        sessao.delete(pessoa)
        sessao.commit()
    #     print(f"Pessoa com número {numero} deletada com sucesso!")
    # else:
    #     print(f"A pessoa com número {numero} não existe no banco de dados!")
    fechar_sessao(sessao)


def buscar_todas_pessoas():
    sessao = criar_sessao()
    pessoas = [
        from_db_to_pessoa(db_pessoa) for db_pessoa in sessao.query(PessoaModelo).all()
    ]
    fechar_sessao(sessao)
    return pessoas


def buscar_pessoa_por_numero(numero):
    sessao = criar_sessao()
    pessoa = from_db_to_pessoa(
        sessao.query(PessoaModelo).filter(PessoaModelo.numero == numero).one_or_none()
    )
    fechar_sessao(sessao)
    return pessoa


def buscar_pessoas_por_camara(numero_camara):
    sessao = criar_sessao()
    pessoas = [
        from_db_to_pessoa(db_pessoa)
        for db_pessoa in (
            sessao.query(PessoaModelo)
            .filter(PessoaModelo.numero_camara == numero_camara)
            .all()
        )
    ]
    fechar_sessao(sessao)
    return from_db_to_pessoa(pessoas)


def adicionar_observacao(numero_pessoa, observacao):
    sessao = criar_sessao()
    db_pessoa = buscar_pessoa_por_numero(numero=numero_pessoa)
    if db_pessoa:
        db_pessoa.observacao = observacao
        sessao.commit()
    fechar_sessao(sessao)


def buscar_pessoas_por_fila_atividade(atividade):
    sessao = criar_sessao()
    pessoas = [
        from_db_to_pessoa(db_pessoa)
        for db_pessoa in (
            sessao.query(PessoaModelo)
            .filter(PessoaModelo.fila_atividade == atividade)
            .all()
        )
    ]
    fechar_sessao(sessao)
    return pessoas


def buscar_pessoas_fila_com_posicao(numero_pessoa) -> tuple:
    sessao = criar_sessao()
    fila_pessoa_resultado = (
        sessao.query(fila_pessoa)
        .filter(fila_pessoa.c.pessoa_numero == numero_pessoa)
        .one_or_none()
    )
    fechar_sessao(sessao)
    return fila_pessoa_resultado


def buscar_pessoas_fila_com_posicao_por_atividade(fila_atividade) -> dict[int, Pessoa]:
    sessao = criar_sessao()
    fila_pessoas = (
        sessao.query(fila_pessoa)
        .filter(fila_pessoa.c.fila_atividade == fila_atividade)
        .order_by(fila_pessoa.c.posicao)
        .all()
    )

    pessoas_com_posicao = {}
    for posicao, fila_atividade, numero_pessoa in fila_pessoas:
        pessoa = buscar_pessoa_por_numero(numero_pessoa)
        pessoas_com_posicao[posicao] = from_db_to_pessoa(pessoa)
    fechar_sessao(sessao)
    return pessoas_com_posicao
