from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from api_recepcao.database.modelos.base_modelo import BaseModelo


# class CamaraModelo(BaseModelo):
#     __tablename__ = 'camara'
#     numero = Column(String(30), primary_key=True)
#     estado = Column(String(30), default='fechada')
#     capacidade = Column(Integer, default=5)
#     pessoa_em_atendimento = Column(Integer, ForeignKey('pessoa.numero'))
#     fila_atividade = Column(String(30), ForeignKey('fila.atividade'))
#     fila = relationship('FilaModelo', back_populates='camaras')
#     pessoas = relationship('PessoaModelo', back_populates='camara', foreign_keys='PessoaModelo.camara_id')

class CamaraModelo(BaseModelo):
    __tablename__ = 'camara'
    numero = Column(String(30), primary_key=True)
    estado = Column(String(30), default='fechada')
    capacidade = Column(Integer, default=5)
    pessoa_em_atendimento = Column(Integer, ForeignKey('pessoa.numero', name='fk_camara_pessoa_atendimento'))
    fila_atividade = Column(String(30), ForeignKey('fila.atividade', name='fk_camara_fila_atividade'))
    fila = relationship('FilaModelo', back_populates='camaras')
    pessoas = relationship('PessoaModelo', back_populates='camara', foreign_keys='PessoaModelo.camara_id')
