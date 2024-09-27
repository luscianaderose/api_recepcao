from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from api_recepcao.database.modelos.base_modelo import BaseModelo
from .fila_modelo import fila_pessoa, FilaModelo
from .camara_modelo import CamaraModelo
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao
from sqlalchemy import func


class PessoaModelo(BaseModelo):
    __tablename__ = "pessoa"
    numero = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    dupla_numero = Column(
        Integer,
        ForeignKey("pessoa.numero", name="fk_dupla_pessoa"),
        nullable=True,
        default=None,
    )
    estado = Column(String(30), default="aguardando")
    observacao = Column(String(200), default="")
    numero_camara = Column(
        String(30), ForeignKey("camara.numero", name="fk_pessoa_camara", use_alter=True)
    )
    fila_atividade = Column(
        String(30), ForeignKey("fila.atividade", name="fk_pessoa_fila")
    )
    camara = relationship(
        "CamaraModelo", back_populates="pessoas", foreign_keys=[numero_camara]
    )
    fila = relationship("FilaModelo", secondary=fila_pessoa, back_populates="pessoas")
    dupla = relationship("PessoaModelo", remote_side=[numero], backref="duplas")


# Função para popular as pessoas apenas como teste.
def popular_pessoas(
    pessoas=[
        ("Ana Paula Soares", "2"),
        ("Beatriz Coutinho", "2"),
        ("Douglas Pinheiro", "2"),
        ("Eduardo Silva", "2"),
        ("Fabiana Feliz", "4"),
        ("Gabriela Machado", "4"),
        ("Henrique De Rose", "4"),
        ("Igor Igreja", "4"),
        ("João Caco", "3"),
        ("Keyla Barbosa", "3"),
        ("Lusciana De Rose", "3"),
        ("Mariana Figueira", "3"),
        ("Nair Wllington", "3A"),
        ("Olga Feliz", "3A"),
        ("Chico Xavier Figueira", "3A"),
        ("Thereza de Calcutá", "3A"),
    ]
):
    sessao = criar_sessao()
    db_pessoas = sessao.query(PessoaModelo).all()
    if not db_pessoas:
        for nome, numero_camara in pessoas:
            pessoa = PessoaModelo(nome=nome, numero_camara=numero_camara)
            sessao.add(pessoa)

        for nome, numero_camara in pessoas:
            pessoa = sessao.query(PessoaModelo).filter_by(nome=nome).one()
            if pessoa.numero_camara:
                camara = (
                    sessao.query(CamaraModelo)
                    .filter(CamaraModelo.numero == pessoa.numero_camara)
                    .one_or_none()
                )
                if camara.fila_atividade:
                    fila = (
                        sessao.query(FilaModelo)
                        .filter(FilaModelo.atividade == camara.fila_atividade)
                        .one_or_none()
                    )

                    pessoa.fila_atividade = fila.atividade
                    posicao = (
                        sessao.query(func.max(fila_pessoa.c.posicao))
                        .filter(fila_pessoa.c.fila_atividade == fila.atividade)
                        .scalar()
                        or 0
                    )

                    posicao += 1
                    # print(posicao)

                    nova_fila_pessoa = fila_pessoa.insert().values(
                        posicao=posicao,
                        fila_atividade=fila.atividade,
                        pessoa_numero=pessoa.numero,
                    )
                    sessao.execute(nova_fila_pessoa)

                sessao.add(pessoa)
            sessao.commit()
    fechar_sessao(sessao)
