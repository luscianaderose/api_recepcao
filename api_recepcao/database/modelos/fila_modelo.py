from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from api_recepcao.database.modelos.base_modelo import BaseModelo
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao


fila_pessoa = Table(
    "fila_pessoa",
    BaseModelo.metadata,
    Column("posicao", Integer, nullable=True),  # primary_key=True, autoincrement=True),
    Column("fila_atividade", String(30), ForeignKey("fila.atividade")),
    Column("pessoa_numero", Integer, ForeignKey("pessoa.numero")),
)


class FilaModelo(BaseModelo):
    __tablename__ = "fila"
    atividade = Column(String(30), primary_key=True)
    nome_display = Column(String(30))
    proximo_numero = Column(Integer, default=1)
    pessoas = relationship("PessoaModelo", secondary=fila_pessoa, back_populates="fila")
    camaras = relationship("CamaraModelo", back_populates="fila")

    def __repr__(self):
        return f"<FilaModelo {self.atividade}>"
