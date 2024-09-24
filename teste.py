from database.modelos.fila_modelo import popular_filas, buscar_todas_filas, buscar_pessoas_da_fila_por_atividade, atualizar_fila, remover_pessoa_da_fila
from database.modelos.camara_modelo import popular_camaras, buscar_todas_camaras, buscar_camaras_por_numero, atualizar_camara
from database.modelos.pessoa_modelo import popular_pessoas, buscar_todas_pessoas, atualizar_pessoa
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
dict_fila_pessoas = {}

for db_fila in buscar_todas_filas():
    dict_filas[db_fila.atividade] = to_fila(db_fila)
    dict_fila_pessoas[db_fila.atividade] = buscar_pessoas_da_fila_por_atividade(db_fila.atividade)

print('dict_fila_pessoas: ', dict_fila_pessoas)
print('dict_filas: ', dict_filas)

dict_camaras = {}
for camara in buscar_todas_camaras():
    dict_camaras[camara.numero] = to_camara(camara)

print('dict-camaras: ', dict_camaras)

dict_pessoas = {}

for db_pessoa in buscar_todas_pessoas():
    pessoa = to_pessoa(db_pessoa)
    if db_pessoa.camara_id:
        pessoa.camara = dict_camaras[db_pessoa.camara_id]
        db_camara = buscar_camaras_por_numero(db_pessoa.camara_id)
        if db_camara.fila_atividade:
            fila = dict_filas[db_camara.fila_atividade]
            posicao_pessoas = dict_fila_pessoas[fila.atividade]
            fila.fila[posicao_pessoas[pessoa.numero]] = pessoa
            camara = dict_camaras[db_pessoa.camara_id]
            camara.fila = fila
    dict_pessoas[db_pessoa.numero] = pessoa

dict_camaras['2'].capacidade_maxima = 10
atualizar_camara(dict_camaras['2'])

dict_filas['prece'].proximo_numero = 2
atualizar_fila(dict_filas['prece'])

dict_pessoas[1].estado = 'atendido'
atualizar_pessoa(dict_pessoas[1])

remover_pessoa_da_fila(dict_pessoas[2].numero, 'videncia')

# print('buscar_pessoas_da_fila_por_atividade(prece) num-pessoa / posicao: ', buscar_pessoas_da_fila_por_atividade('prece'))
# print('dict_pessoas: ', dict_pessoas)
# print('dict_camaras[2].fila: ', dict_camaras['2'].fila)
# print('dict_pessoas[1].camara: ', dict_pessoas[1].camara)
# print('dict_filas[videncia].fila: ', dict_filas['videncia'].fila)
# print('dict_pessoas[5].camara: ', dict_pessoas[5].camara)
