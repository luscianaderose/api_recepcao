from conf.sessao import criar_tabelas, criar_sessao, fechar_sessao
from modelos.camara_modelo import criar_camara_modelo, buscar_todas_camaras, buscar_camaras_por_numero, deletar_camara_por_numero
from modelos.pessoa_modelo import criar_pessoa, buscar_todas_pessoas, buscar_pessoa_por_numero, buscar_pessoas_por_camara, deletar_pessoa_por_numero
from modelos.fila_modelo import criar_fila, buscar_todas_filas, buscar_fila_por_atividade, deletar_fila_por_atividade


criar_tabelas()
criar_camara_modelo('2')
criar_camara_modelo('3')
criar_camara_modelo('3A')
criar_camara_modelo('4')
# sessao = criar_sessao()
# fechar_sessao(sessao)

criar_pessoa('Lusciana', '2')
criar_pessoa('Lívia', '2')
criar_pessoa('Pedro', '3')
criar_pessoa('Lucas', '3A')

lusciana = buscar_pessoa_por_numero(1)
livia = buscar_pessoa_por_numero(2)
pedro = buscar_pessoa_por_numero(3)
lucas = buscar_pessoa_por_numero(4)

criar_fila(atividade='videncia', nome_display='Vidêcia', pessoas=[lusciana, livia])
criar_fila(atividade='prece', nome_display='Prece', pessoas=[pedro, lucas])



# pessoas = buscar_todas_pessoas()
# print(pessoas)
# for pessoa in pessoas:
#     print(pessoa.nome)

# print('Quem é o número 1? ', buscar_pessoa_por_numero(1).nome)

# print('Quem está na câmara 2 (inserir o número da câmara)? ', buscar_pessoas_por_camara('2')[1].nome)

# for pessoa in buscar_pessoas_por_camara('2'):
#     print('Quem está na câmara 2? ', pessoa.nome)

# print('Quem está na câmara 1? ')
# for pessoa in buscar_pessoas_por_camara('1'):
#     print(pessoa.nome)

print('-> Câmaras: ')
for camara in buscar_todas_camaras():
    print('Câmara: ', camara.numero, 'Estado: ', camara.estado)

print('Qual câmara? ', 'Número: ', buscar_camaras_por_numero('2').numero, 'Estado: ', buscar_camaras_por_numero('2').estado)

print('Filas: ', buscar_todas_filas()) # Para ver como fica o nome da instânica da classe personalizado.

print('Filas: ')
for fila in buscar_todas_filas():
    print('Nome Display: ', fila.nome_display)

print('Fila por atividade: ', buscar_fila_por_atividade('videncia').nome_display)



#deletar_pessoa_por_numero(1)

#deletar_camara_por_numero('2')

#deletar_fila_por_atividade('prece')






# from modelos.camara_modelo import CamaraModelo
# from modelos.fila_modelo import FilaModelo
# from modelos.pessoa_modelo import PessoaModelo
# from modelos.base_modelo import BaseModelo


# engine = create_engine('sqlite:///recepcao.db')

# BaseModelo.metadata.drop_all(engine) #excluir banco automaticamente e criar de novo
# BaseModelo.metadata.create_all(engine)
# Sessao = sessionmaker(bind=engine)
# sessao = Sessao()

# # Adicionar câmaras
# camara2 = CamaraModelo(numero='2')
# camara3 = CamaraModelo(numero='3')
# camara3A = CamaraModelo(numero='3A')
# camara4 = CamaraModelo(numero='4')
# sessao.add_all([camara2, camara3, camara3A, camara4])

# # Adicionar pessoas
# lusciana = PessoaModelo(nome='Lusciana', estado='atendida', camara_id=camara2.numero)
# livia = PessoaModelo(nome='Lívia', estado='atendida', camara_id=camara4.numero)
# lucas = PessoaModelo(nome='Lucas', estado='atendida', camara_id=camara3.numero)
# pedro = PessoaModelo(nome='Pedro', camara_id=camara3A.numero)
# sessao.add(lusciana)
# sessao.add(livia)
# sessao.add(lucas)
# sessao.add(pedro)

# # Adicionar filas
# videncia = FilaModelo(atividade='videncia', nome_display='Vidência', pessoas=[lusciana, livia])
# prece = FilaModelo(atividade='prece', nome_display='Prece', pessoas=[lucas, pedro])
# sessao.add(videncia)
# sessao.add(prece)

# sessao.commit()

# # Consultar os dados
# def cabecalho(descricao):
#     print('-' * 10, descricao, '-' * 10)

# camaras = sessao.query(CamaraModelo).all()
# for camara in camaras:
#     pessoas = camara.pessoas
#     cabecalho('CamaraModelos')
#     print('Numero: ', camara.numero)
#     print('Estado: ', camara.estado)
#     print('Capacidade: ', camara.capacidade)
#     if pessoas:
#         print('PessoaModelos')
#         for pessoa in pessoas:
#             print(' ' * 2, '> PessoaModelo: ', pessoa.nome)
# print('\n')
# pessoas = sessao.query(PessoaModelo).all()
# for pessoa in pessoas:
#     cabecalho('PessoaModelos')
#     print('Nome: ', pessoa.nome)
#     print('Dupla: ', pessoa.dupla)
#     print('Estado: ', pessoa.estado)
#     print('Observação: ', pessoa.observacao)
#     print('Câmara: ', pessoa.camara_id)

# print('\n')
# filas = sessao.query(FilaModelo).all()
# for fila in filas:
#     cabecalho('Filas')
#     print('Atividade: ', fila.atividade)
#     print('Nome display: ', fila.nome_display)
#     print('Próximo número: ', fila.proximo_numero)
#     pessoas = fila.pessoas
#     if pessoa:
#         print('PessoaModelos: ')
#         for pessoa in pessoas:
#             print(' ' * 2, '> PessoaModelo: ', pessoa.nome)
#             print(' ' * 2, '> Câmara: ', pessoa.camara_id)

# sessao.close()
