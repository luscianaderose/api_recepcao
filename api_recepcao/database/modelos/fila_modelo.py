from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from api_recepcao.database.modelos.base_modelo import BaseModelo
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao


fila_pessoa = Table(
    'fila_pessoa',
    BaseModelo.metadata, 
    Column('posicao', Integer, primary_key=True, autoincrement=True),
    Column('fila_atividade', String(30), ForeignKey('fila.atividade')),
    Column('pessoa_numero', Integer, ForeignKey('pessoa.numero'))
)

class FilaModelo(BaseModelo):
    __tablename__ = 'fila'
    atividade = Column(String(30), primary_key=True)
    nome_display = Column(String(30))
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

def buscar_pessoas_da_fila_por_atividade(atividade):
    sessao = criar_sessao()
    fila = sessao.query(FilaModelo).filter(FilaModelo.atividade == atividade).one_or_none()
    pessoas_com_posicao = {}
    for pessoa in fila.pessoas:
        #resultado_pessoa_fila é uma linha da tabela pessoa_fila
        resultado_pessoa_fila = sessao.query(fila_pessoa).filter(
            fila_pessoa.c.fila_atividade == fila.atividade,
            fila_pessoa.c.pessoa_numero == pessoa.numero
        ).one_or_none()
        pessoas_com_posicao[pessoa.numero] = resultado_pessoa_fila.posicao
    fechar_sessao(sessao)
    return pessoas_com_posicao

def atualizar_fila(fila):
    sessao = criar_sessao()
    db_fila = sessao.query(FilaModelo).filter(FilaModelo.atividade == fila.atividade).one_or_none()
    if db_fila:
        db_fila.atividade = fila.atividade
        db_fila.nome_display = fila.nome_display
        db_fila.proximo_numero = fila.proximo_numero
    sessao.commit()
    fechar_sessao(sessao)

def remover_pessoa_da_fila(pessoa_numero, fila_atividade):
    sessao = criar_sessao()
    db_fila = sessao.query(FilaModelo).filter(FilaModelo.atividade == fila_atividade).one_or_none()
    if db_fila:
        pessoa_fila = sessao.query(fila_pessoa).filter(
            fila_pessoa.c.fila_atividade == fila_atividade,
            fila_pessoa.c.pessoa_numero == pessoa_numero
        ).one_or_none()
        if pessoa_fila:
            # sessao.delete(pessoa_fila)
            delete_stmt = fila_pessoa.delete().where(
                fila_pessoa.c.fila_atividade == fila_atividade,
                fila_pessoa.c.pessoa_numero == pessoa_numero
            )
            sessao.execute(delete_stmt)
            sessao.commit()
    fechar_sessao(sessao)
            