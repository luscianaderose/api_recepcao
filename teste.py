from database.modelos.fila_modelo import popular_filas, buscar_fila_por_atividade
from database.modelos.camara_modelo import popular_camaras
from database.modelos.pessoa_modelo import popular_pessoas
from database.conf.sessao import criar_tabelas
from fila import to_fila

criar_tabelas()
popular_filas()
popular_camaras()
popular_pessoas()

# fila_videncia = Fila('videncia', ARQUIVO_FILA_VIDENCIA, 'Vidência')

#db_fila_videncia = buscar_fila_por_atividade('videncia')
fila_videncia = to_fila(buscar_fila_por_atividade('videncia'))
print('fila videncia', fila_videncia)