from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from api_recepcao.database.modelos.base_modelo import BaseModelo
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao


class CamaraModelo(BaseModelo):
    __tablename__ = "camara"
    numero = Column(String(30), primary_key=True)
    estado = Column(String(30), default="fechada")
    numero_de_atendimentos = Column(Integer, default=0)
    capacidade_maxima = Column(Integer, default=5)
    pessoa_em_atendimento = Column(
        Integer,
        ForeignKey(
            "pessoa.numero", name="fk_camara_pessoa_atendimento", use_alter=True
        ),
    )
    fila_atividade = Column(
        String(30), ForeignKey("fila.atividade", name="fk_camara_fila_atividade")
    )
    fila = relationship("FilaModelo", back_populates="camaras")
    pessoas = relationship(
        "PessoaModelo",
        back_populates="camara",
        foreign_keys="PessoaModelo.numero_camara",
    )
