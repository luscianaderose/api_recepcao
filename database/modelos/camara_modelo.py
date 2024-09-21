from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from database.modelos.base_modelo import BaseModelo
from database.conf.sessao import criar_sessao, fechar_sessao


class CamaraModelo(BaseModelo):
    __tablename__ = 'camara'
    numero = Column(String, primary_key=True)
    estado = Column(String, default='fechada')
    capacidade = Column(Integer, default=5)
    pessoa_em_atendimento = Column(Integer, ForeignKey('pessoa.numero'))
    fila_atividade = Column(String, ForeignKey('fila.atividade'))
    fila = relationship('FilaModelo', back_populates='camaras')
    pessoas = relationship('PessoaModelo', back_populates='camara', foreign_keys='PessoaModelo.camara_id')

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

def deletar_camara_por_numero(numero):
    sessao = criar_sessao()
    camara = sessao.query(CamaraModelo).filter(CamaraModelo.numero == numero).one_or_none()
    if camara:
        sessao.delete(camara)
        sessao.commit()
        print(f'Câmara {numero} deletada com sucesso!')
    else:
        print(f'A câmara {numero} não existe no banco de dados!')
    
def popular_camaras(camaras=[('2', 'videncia'), ('4', 'videncia'), ('3', 'prece'), ('3A', 'prece')]):
    sessao = criar_sessao()
    db_camaras = sessao.query(CamaraModelo).all()
    if not db_camaras:
        for numero, fila_atividade in camaras:
            camara = CamaraModelo(numero=numero, fila_atividade=fila_atividade)
            sessao.add(camara)
            print(f'Adicionando camara {numero}.')
        sessao.commit()
    fechar_sessao(sessao)

def atualizar_camara(camara):
    sessao = criar_sessao()
    db_camara = sessao.query(CamaraModelo).filter(CamaraModelo.numero == camara.numero_camara).one_or_none()
    if db_camara:
        db_camara.estado = camara.estado
        db_camara.capacidade = camara.capcidade
        db_camara.pessoa_em_atendimento = camara.pessoa_em_atendimento
    sessao.commit()
    fechar_sessao(sessao)