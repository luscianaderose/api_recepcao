from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from database.modelos.base_modelo import BaseModelo
from .fila_modelo import fila_pessoa, FilaModelo
from .camara_modelo import CamaraModelo
from database.conf.sessao import criar_sessao, fechar_sessao


class PessoaModelo(BaseModelo):
    __tablename__ = 'pessoa'
    numero = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    dupla = Column(Integer, default=-1)
    estado = Column(String, default='aguardando')
    observacao = Column(String, default='')
    camara_id = Column(String, ForeignKey('camara.numero'))
    camara = relationship('CamaraModelo', back_populates='pessoas', foreign_keys=[camara_id])
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

# Função para popular as pessoas apenas como teste.
def popular_pessoas(
    pessoas=[
        ('Ana Paula Soares', '2'),
        ('Beatriz Coutinho', '2'),
        ('Douglas Pinheiro', '2'),
        ('Eduardo Silva', '2'),
        ('Fabiana Feliz', '4'),
        ('Gabriela Machado', '4'),
        ('Henrique De Rose', '4'),
        ('Igor Igreja', '4'),
        ('João Caco', '3'),
        ('Keyla Barbosa', '3'),
        ('Lusciana De Rose', '3'),
        ('Mariana Figueira', '3'),
        ('Nair Wllington', '3A'),
        ('Olga Feliz', '3A'),
        ('Chico Xavier Figueira', '3A'),
        ('Thereza de Calcutá', '3A'),
    ]
):
    sessao = criar_sessao()
    db_pessoas = sessao.query(PessoaModelo).all()
    if not db_pessoas:
        for nome, camara_id in pessoas:
            pessoa = PessoaModelo(nome=nome, camara_id=camara_id)
            if pessoa.camara_id:
                camara = sessao.query(CamaraModelo).filter(CamaraModelo.numero==pessoa.camara_id).one_or_none()
                if camara.fila_atividade:
                    fila = sessao.query(FilaModelo).filter(FilaModelo.atividade==camara.fila_atividade).one_or_none()
                    fila.pessoas.append(pessoa)
            sessao.add(pessoa)
            print(f'Adicionando pessoa {nome}.')
        sessao.commit()
    fechar_sessao(sessao)
