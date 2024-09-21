from database.modelos.fila_modelo import popular_filas, buscar_todas_filas
from database.modelos.camara_modelo import popular_camaras, buscar_todas_camaras
from database.modelos.pessoa_modelo import popular_pessoas, buscar_todas_pessoas
from database.conf.sessao import criar_tabelas
from fila import to_fila
from camara import to_camara
from pessoa import to_pessoa

criar_tabelas()
popular_filas()
popular_camaras()
popular_pessoas()

# fila_videncia = Fila('videncia', ARQUIVO_FILA_VIDENCIA, 'Vidência')

#db_fila_videncia = buscar_fila_por_atividade('videncia')

dict_filas = {}
for fila in buscar_todas_filas():
    dict_filas[fila.atividade] = to_fila(fila)

print('dict_filas: ', dict_filas)

dict_camaras = {}
for camara in buscar_todas_camaras():
    dict_camaras[camara.numero] = to_camara(camara)



print('dict-camaras: ', dict_camaras)

dict_pessoas = {}

for pessoa in buscar_todas_pessoas():
    dict_pessoas[pessoa.numero] = to_pessoa(pessoa)

print('dict_pessoas: ', dict_pessoas)
print('dict_camaras[2].fila: ', dict_camaras['2'].fila)
print('dict_pessoas[1].camara: ', dict_pessoas[1].camara)
print('dict_filas[videncia].fila: ', dict_filas['videncia'].fila)

