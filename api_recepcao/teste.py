from api_recepcao.repository.fila_repo import (
    buscar_fila_por_atividade,
    buscar_pessoas_fila_com_posicao_por_atividade,
)
from api_recepcao.repository.pessoa_repo import (
    buscar_pessoa_por_numero,
    atualizar_pessoa,
)
from api_recepcao.repository.camara_repo import (
    buscar_camara_por_numero,
    atualizar_camara,
)

from api_recepcao.service.chamar_atendido import chamar_atendido
from api_recepcao.service.trocar_posicao import trocar_posicao
from api_recepcao.service.dupla_service import criar_dupla, cancelar_dupla

from api_recepcao.entities.fila import Fila
from api_recepcao.entities.pessoa import Pessoa
from api_recepcao.entities.camara import Camara

from api_recepcao.database.conf.setup import setup_db

from api_recepcao.service.camara_service import get_dict_camaras

setup_db()
p1 = buscar_pessoa_por_numero(1)
p2 = buscar_pessoa_por_numero(2)

p1.dupla_numero = None
p2.dupla_numero = None

atualizar_pessoa(p1)
atualizar_pessoa(p2)

criar_dupla(1, 2)
# cancelar_dupla(1)

trocar_posicao(1, 2)

for numero_camara in ["2", "4"]:
    camara = buscar_camara_por_numero(numero_camara)
    camara.estado = Camara.atendendo
    atualizar_camara(camara)

for i in range(8):
    chamar_atendido("2")

# for i in range(5):
#     chamar_atendido("4")
