from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # Definindo modelo inicial de cada tabela.

class Pessoa(Base):
    __tablename__ = 'pessoa'
    numero = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    dupla = Column(Integer)
    estado = Column(String)

engine = create_engine('sqlite:///recepcao.db')
Base.metadata.create_all(engine)
Sessao = sessionmaker(bind=engine)
sessao = Sessao()

# Adicionar pessoas
#lusciana = Pessoa(nome='Lusciana', dupla=-1, estado='atendida')
livia = Pessoa(nome='Livia', dupla=-1, estado='atendida')
lucas = Pessoa(nome='Lucas', dupla=-1, estado='atendida')
pedro = Pessoa(nome='Pedro', dupla=-1, estado='atendida')
#sessao.add(lusciana)
sessao.add(livia)
sessao.add(lucas)
sessao.add(pedro)
sessao.commit()
sessao.close()