"""Camada intermediaria de abstracao entre o modelo CamaraModelo e a classe Camara"""
from api_recepcao.database.modelos.camara_modelo import CamaraModelo
from api_recepcao.database.conf.sessao import criar_sessao, fechar_sessao
from api_recepcao.camara import Camara
from api_recepcao.fila import Fila


def criar_camara_modelo(numero):
    sessao = criar_sessao()
    camara = CamaraModelo(numero=numero)
    sessao.add(camara)
    sessao.commit()
    fechar_sessao(sessao)

def buscar_todas_camaras():
    sessao = criar_sessao()
    lista_camaras = [
        Camara(
            camara.numero,
            fila=Fila( # TODO: mudar isso! deveria retornar apenas a Primary Key e não um dict. SRP
                atividade=camara.fila.atividade, 
                nome_display=camara.fila.nome_display, 
                proximo_numero=camara.fila.proximo_numero,
                # fila=
            ),
            estado=camara.estado,
            capacidade_maxima=camara.capacidade,
            nome_fila=camara.fila.atividade,
        )
        for camara in sessao.query(CamaraModelo).all()
    ]
    fechar_sessao(sessao)
    return lista_camaras

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
        db_camara.numero = camara.numero_camara
        db_camara.estado = camara.estado
        db_camara.capacidade = camara.capacidade_maxima
        if camara.pessoa_em_atendimento is not None:
            db_camara.pessoa_em_atendimento = camara.pessoa_em_atendimento.numero
        else:
            camara.pessoa_em_atendimento = None
        db_camara.fila_atividade = camara.nome_fila
    sessao.commit()
    fechar_sessao(sessao)
