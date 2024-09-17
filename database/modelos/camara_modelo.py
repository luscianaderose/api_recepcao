from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from modelos.base_modelo import BaseModelo
from conf.sessao import criar_sessao, fechar_sessao


class CamaraModelo(BaseModelo):
    __tablename__ = 'camara'
    numero = Column(String, primary_key=True)
    estado = Column(String, default='fechada')
    capacidade = Column(Integer, default=5)
    pessoas = relationship('PessoaModelo', back_populates='camara')

def criar_camara_modelo(numero):
    sessao = criar_sessao()
    camara = CamaraModelo(numero=numero)
    sessao.add(camara)
    sessao.commit()
    fechar_sessao(sessao)

def buscar_todas_camaras():
    sessao = criar_sessao()
    camaras = sessao.query(CamaraModelo).all()
    fechar_sessao(sessao)
    return camaras
 
def buscar_camaras_por_numero(numero):
    sessao = criar_sessao()
    camara = sessao.query(CamaraModelo).filter(CamaraModelo.numero == numero).one_or_none()
    fechar_sessao(sessao)
    return camara