from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from modelos.base_modelo import BaseModelo
from .fila_modelo import fila_pessoa
from conf.sessao import criar_sessao, fechar_sessao


class PessoaModelo(BaseModelo):
    __tablename__ = 'pessoa'
    numero = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    dupla = Column(Integer, default=-1)
    estado = Column(String, default='aguardando')
    observacao = Column(String, default='')
    camara_id = Column(String, ForeignKey('camara.numero'))
    camara = relationship('CamaraModelo', back_populates='pessoas')
    fila = relationship('FilaModelo', secondary=fila_pessoa, back_populates='pessoas')

def criar_pessoa(nome, camara_id):
    sessao = criar_sessao()
    pessoa = PessoaModelo(nome=nome, camara_id=camara_id)
    sessao.add(pessoa)
    sessao.commit()
    fechar_sessao(sessao)

def buscar_todas_pessoas():
    sessao = criar_sessao()
    pessoas = sessao.query(PessoaModelo).all()
    fechar_sessao(sessao)
    return pessoas

def buscar_pessoa_por_numero(numero):
    sessao = criar_sessao()
    pessoa = sessao.query(PessoaModelo).filter(PessoaModelo.numero == numero).one_or_none()
    fechar_sessao(sessao)
    return pessoa

def buscar_pessoas_por_camara(camara_id):
    sessao = criar_sessao()
    pessoas = sessao.query(PessoaModelo).filter(PessoaModelo.camara_id == camara_id).all()
    fechar_sessao(sessao)
    return pessoas

def deletar_pessoa_por_numero(numero):
    sessao = criar_sessao()
    pessoa = sessao.query(PessoaModelo).filter(PessoaModelo.numero == numero).one_or_none()
    if pessoa:
        sessao.delete(pessoa)
        sessao.commit()
        print(f'Pessoa com número {numero} deletada com sucesso!')
    else:
        print(f'A pessoa com número {numero} não existe no banco de dados!')
    fechar_sessao(sessao)
