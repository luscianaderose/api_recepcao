
from api_recepcao.database.conf.sessao import criar_tabelas
from api_recepcao.database.modelos.fila_modelo import popular_filas
from api_recepcao.repository.camara_repo import popular_camaras
from api_recepcao.database.modelos.pessoa_modelo import popular_pessoas

def setup_db():
    criar_tabelas()
    popular_filas()
    popular_camaras()
    # popular_pessoas() # TODO remover isto

