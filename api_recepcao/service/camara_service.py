from api_recepcao.repository.camara_repo import buscar_todas_camaras, atualizar_camara
from api_recepcao.entities.camara import Camara


def get_dict_camaras():
    return {camara.numero: camara for camara in buscar_todas_camaras()}


def salvar_camara(camara):
    if camara and isinstance(camara, Camara):
        atualizar_camara(camara=camara)
