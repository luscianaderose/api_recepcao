from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from database.modelos.base_modelo import BaseModelo
from database.conf.sessao import criar_sessao, fechar_sessao


fila_pessoa = Table(
    'fila_pessoa',
    BaseModelo.metadata, 
    Column('fila_atividade', String, ForeignKey('fila.atividade')),
    Column('pessoa_numero', Integer, ForeignKey('pessoa.numero'))
)

class FilaModelo(BaseModelo):
    __tablename__ = 'fila'
    atividade = Column(String, primary_key=True)
    nome_display = Column(String)
    proximo_numero = Column(Integer, default=1)
    pessoas = relationship('PessoaModelo', secondary=fila_pessoa, back_populates='fila')
    camaras = relationship('CamaraModelo', back_populates='fila')

    def __repr__(self):
        return f'<FilaModelo {self.atividade}>'

def criar_fila(atividade, nome_display, pessoas=[]):
    sessao = criar_sessao()
    camara = FilaModelo(atividade=atividade, nome_display=nome_display, pessoas=pessoas)
    sessao.add(camara)
    sessao.commit()
    fechar_sessao(sessao)

def buscar_todas_filas():
    sessao = criar_sessao()
    filas = sessao.query(FilaModelo).all()
    fechar_sessao(sessao)
    return filas

def buscar_fila_por_atividade(atividade):
    sessao = criar_sessao()
    fila = sessao.query(FilaModelo).filter(FilaModelo.atividade == atividade).one_or_none()
    fechar_sessao(sessao)
    return fila

def deletar_fila_por_atividade(atividade):
    sessao = criar_sessao()
    fila = sessao.query(FilaModelo).filter(FilaModelo.atividade == atividade).one_or_none()
    if fila:
        sessao.delete(fila)
        sessao.commit()
        print(f'A fila {atividade} foi deletada com sucesso!')
    else:
        print(f'A fila {atividade} não existe no banco de dados!')

def popular_filas(filas=[('videncia', 'Vidência'), ('prece', 'Prece')]):
    sessao = criar_sessao()
    db_filas = sessao.query(FilaModelo).all()
    if not db_filas:
        for atividade, nome_display in filas:
            fila = FilaModelo(atividade=atividade, nome_display=nome_display, pessoas=[])
            sessao.add(fila)
            print(f'Adicionando fila {atividade}.')
        sessao.commit()
    fechar_sessao(sessao)