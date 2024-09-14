from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # Definindo modelo inicial de cada tabela.
fila_pessoa = Table(
    'fila_pessoa',
    Base.metadata, 
    Column('fila_atividade', String, ForeignKey('fila.atividade')),
    Column('pessoa_numero', Integer, ForeignKey('pessoa.numero'))
)

class Pessoa(Base):
    __tablename__ = 'pessoa'
    numero = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    dupla = Column(Integer, default=-1)
    estado = Column(String, default='aguardando')
    observacao = Column(String, default='')
    camara_id = Column(String, ForeignKey('camara.numero'))
    camara = relationship('Camara', back_populates='pessoas')
    fila = relationship('Fila', secondary=fila_pessoa, back_populates='pessoas')

#numero_camara, fila, nome_fila, estado=fechada, capacidade_maxima=5
class Camara(Base):
    __tablename__ = 'camara'
    numero = Column(String, primary_key=True)
    estado = Column(String, default='fechada')
    capacidade = Column(Integer, default=5)
    pessoas = relationship('Pessoa', back_populates='camara')

class Fila(Base):
    __tablename__ = 'fila'
    atividade = Column(String, primary_key=True)
    nome_display = Column(String)
    proximo_numero = Column(Integer, default=1)
    pessoas = relationship('Pessoa', secondary=fila_pessoa, back_populates='fila')

engine = create_engine('sqlite:///recepcao.db')
Base.metadata.drop_all(engine) #excluir banco automaticamente e criar de novo
Base.metadata.create_all(engine)
Sessao = sessionmaker(bind=engine)
sessao = Sessao()

# Adicionar câmaras
camara2 = Camara(numero='2')
camara3 = Camara(numero='3')
camara3A = Camara(numero='3A')
camara4 = Camara(numero='4')
sessao.add_all([camara2, camara3, camara3A, camara4])

# Adicionar pessoas
lusciana = Pessoa(nome='Lusciana', estado='atendida', camara_id=camara2.numero)
livia = Pessoa(nome='Lívia', estado='atendida', camara_id=camara4.numero)
lucas = Pessoa(nome='Lucas', estado='atendida', camara_id=camara3.numero)
pedro = Pessoa(nome='Pedro', camara_id=camara3A.numero)
sessao.add(lusciana)
sessao.add(livia)
sessao.add(lucas)
sessao.add(pedro)

# Adicionar filas
videncia = Fila(atividade='videncia', nome_display='Vidência', pessoas=[lusciana, livia])
prece = Fila(atividade='prece', nome_display='Prece', pessoas=[lucas, pedro])
sessao.add(videncia)
sessao.add(prece)

sessao.commit()

# Consultar os dados
def cabecalho(descricao):
    print('-' * 10, descricao, '-' * 10)

camaras = sessao.query(Camara).all()
for camara in camaras:
    pessoas = camara.pessoas
    cabecalho('Camaras')
    print('Numero: ', camara.numero)
    print('Estado: ', camara.estado)
    print('Capacidade: ', camara.capacidade)
    if pessoas:
        print('Pessoas')
        for pessoa in pessoas:
            print(' ' * 2, '> Pessoa: ', pessoa.nome)
print('\n')
pessoas = sessao.query(Pessoa).all()
for pessoa in pessoas:
    cabecalho('Pessoas')
    print('Nome: ', pessoa.nome)
    print('Dupla: ', pessoa.dupla)
    print('Estado: ', pessoa.estado)
    print('Observação: ', pessoa.observacao)
    print('Câmara: ', pessoa.camara_id)

print('\n')
filas = sessao.query(Fila).all()
for fila in filas:
    cabecalho('Filas')
    print('Atividade: ', fila.atividade)
    print('Nome display: ', fila.nome_display)
    print('Próximo número: ', fila.proximo_numero)
    pessoas = fila.pessoas
    if pessoa:
        print('Pessoas: ')
        for pessoa in pessoas:
            print(' ' * 2, '> Pessoa: ', pessoa.nome)
            print(' ' * 2, '> Câmara: ', pessoa.camara_id)

sessao.close()
