from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = None

def criar_engine():
    global engine

    if engine:
        return
    
    engine = create_engine('sqlite:///recepcao.db')
    
    return engine

def criar_sessao():
    global engine

    if not engine:
        criar_engine()

    Sessao = sessionmaker(bind=engine)
    return Sessao()

def criar_tabelas():
    global engine

    if not engine:
        criar_engine()

    from api_recepcao.database.modelos.camara_modelo import CamaraModelo
    from api_recepcao.database.modelos.fila_modelo import FilaModelo
    from api_recepcao.database.modelos.pessoa_modelo import PessoaModelo
    from api_recepcao.database.modelos.base_modelo import BaseModelo
    BaseModelo.metadata.drop_all(engine) #excluir banco automaticamente e criar de novo
    BaseModelo.metadata.create_all(engine)

def fechar_sessao(sessao):
    sessao.close()
    

