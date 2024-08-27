from pessoa import Pessoa


class Fila():
    def __init__(self, atividade, nome_arquivo, nome_display):
        self.atividade = atividade
        self.nome_display = nome_display
        self.nome_arquivo = nome_arquivo
        self.fila = {}
        self.proximo_numero = 1

    def to_dict(self):
        return {
            "atividade": self.atividade,
            "nome_display": self.nome_display,
            "nome_arquivo": self.nome_arquivo,
            "fila": {key:value.to_dict() for key,value in self.fila.items()},
            "proximo_numero": self.proximo_numero
        }
    
    def __contains__(self, numero):
        return numero in self.fila
    
    
    def adicionar_pessoa(self, pessoa, numero):
        for p in self.fila.values():
            if p.nome == pessoa.nome:
                raise Exception('Não foi possível registrar porque o nome já existe.')
        if numero in self.fila:
            raise Exception('Não foi possível registrar porque o número já existe.')
        self.fila[numero] = pessoa
        self.proximo_numero += 1
        self.salvar_fila()

    def remover_pessoa(self, numero):
        if numero not in self.fila:
            raise Exception('Não foi possível remover porque a pessoa não existe.')
        pessoa = self.fila[numero]
        if pessoa.dupla != - 1:
            self.fila[pessoa.dupla].dupla = -1
        del self.fila[numero]
        self.salvar_fila()

    def editar_pessoa(self, numero, nome):
        for p in self.fila.values():
            if p.nome == nome:
                return #Exception('Não foi possível registrar porque o nome já existe.')
        if numero not in self.fila:
            raise Exception('Não foi possível registrar porque o número não existe.')
        self.fila[numero].nome = nome
        self.salvar_fila()

    def values(self):
        return sorted(self.fila.values(), key=lambda p: p.numero)
    
    def clear(self):
        self.fila.clear()

    def get(self, numero):
        if numero in self.fila:
            return self.fila[numero]
        return None
    
    def trocar_posicao(self, n1, n2, ignorar_duplas=False):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível mover!')
        if n2 < n1:
            return self.trocar_posicao(n2, n1, ignorar_duplas)
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        if ignorar_duplas == False and pessoa1.dupla != n2 and (pessoa1.dupla != -1 or pessoa2.dupla != -1):
            if pessoa1.dupla != -1 and pessoa2.dupla != -1: #p1+p2 tem dupla. Se tiver dupla e se for trocar com alguem que nao é a propria dupla
                self.trocar_posicao(n1, pessoa2.dupla, ignorar_duplas=True)
                self.trocar_posicao(pessoa1.dupla, n2, ignorar_duplas=True)
            elif pessoa1.dupla != -1: #somente a p1 tem dupla
                self.trocar_posicao(n1, n2, ignorar_duplas=True)
                self.trocar_posicao(n1, pessoa1.dupla, ignorar_duplas=True)
            elif pessoa2.dupla != -1: #somente a p2 tem dupla
                self.trocar_posicao(n1, n2, ignorar_duplas=True)
                self.trocar_posicao(n2, pessoa2.dupla, ignorar_duplas=True)
            return 
        if pessoa1.dupla != -1:
            dupla = self.fila[pessoa1.dupla]
            dupla.dupla = n2
        if pessoa2.dupla != -1:
            dupla = self.fila[pessoa2.dupla]
            dupla.dupla = n1
        pessoa1.numero = n2
        pessoa2.numero = n1
        self.fila[n1] = pessoa2
        self.fila[n2] = pessoa1
        self.salvar_fila()

    def keys(self):
        return sorted(self.fila.keys())
    
    def criar_dupla(self, n1, n2):
        if n1 not in self.fila or n2 not in self.fila:
            raise Exception('Não foi possível criar dupla!')
        pessoa1 = self.fila[n1]
        pessoa2 = self.fila[n2]
        if pessoa1.dupla != -1 or pessoa2.dupla != -1:
            raise Exception ('Não é possível criar dupla com uma pessoa de outra dupla!')
        if pessoa1.estado != pessoa1.aguardando or pessoa2.estado != pessoa2.aguardando:
            raise Exception('Não é possível criar dupla depois que a pessoa já foi chamada!')
        pessoa1.dupla = n2
        pessoa2.dupla = n1
        self.salvar_fila()

    def cancelar_dupla(self, n1):
        if n1 not in self.fila:
            raise Exception ('Não foi possível cancelar a dupla!')
        pessoa1 = self.get(n1)
        pessoa2 = self.get(pessoa1.dupla)
        pessoa1.dupla = -1
        pessoa2.dupla = -1
        self.salvar_fila()

    def salvar_fila(self):
        with open(self.nome_arquivo, 'w') as f:
            for pessoa in self.values():
                f.write(f'{pessoa.csv()}\n')

    def ler_fila(self):
        with open(self.nome_arquivo, 'r') as f:
            for linha in f.read().splitlines():
                if not linha:
                    continue
                numero, nome, estado, camara, dupla, asterisco, observacao = linha.split(',', 6)
                pessoa = Pessoa(int(numero), nome, estado, camara, int(dupla), int(asterisco), observacao)
                self.adicionar_pessoa(pessoa, pessoa.numero)

    def toggle_asterisco(self, numero_atendido):
        pessoa = self.get(numero_atendido)
        pessoa.asterisco = 0 if pessoa.asterisco else 1
        self.salvar_fila()
    
    def adicionar_observacao(self, numero_atendido, observacao):
        pessoa = self.get(numero_atendido)
        pessoa.observacao = observacao
        self.salvar_fila()

    def get_posicao(self, numero):
        if numero in self.fila:
            for index, pessoa in enumerate(self.values()):
                if pessoa.numero == numero:
                    return index + 1
        return None
    
