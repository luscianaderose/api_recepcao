class Camara:
    fechada = 'FECHADA'
    atendendo = 'ATENDENDO'
    avisar = 'ÚLTIMO'
    avisado = 'FOI AVISADO'

    def __init__(self, numero_camara, fila, nome_fila, estado=fechada, capacidade_maxima=5):
        self.numero_camara = numero_camara
        self.fila = fila
        self.nome_fila = nome_fila
        self.pessoa_em_atendimento = None
        self.numero_de_atendimentos = 0
        self.estado = estado
        self.audio = f'camara{numero_camara}.wav'
        self.capacidade_maxima = capacidade_maxima

    def to_dict(self):
        return {
            "numero_camara": self.numero_camara,
            "fila": self.fila.to_dict(),
            "nome_fila": self.nome_fila,
            "pessoa_em_atendimento": self.pessoa_em_atendimento.to_dict() if self.pessoa_em_atendimento else None,
            "numero_de_atendimentos": self.numero_de_atendimentos,
            "estado": self.estado,
            "audio": self.audio,
            "capacidade_maxima": self.capacidade_maxima
        }

    def fechar(self):
        self.pessoa_em_atendimento = None
        self.estado = self.fechada

    def abrir(self):
        self.numero_de_atendimentos = 0
        self.estado = self.atendendo


    def chamar_atendido(self):
        '''Encontra a primeira pessoa da fila que não foi chamada, marca como chamada 
        e adiciona a self.pessoa_em_atendimento. Caso a pessoa tenha uma dupla, 
        a sua dupla também será marcada.'''
        if self.estado != self.atendendo:
            return self.estado
        for pessoa in self.fila.values():
            if pessoa.estado == pessoa.aguardando:
                break
        else:
            self.estado = self.avisar
            return self.estado
        if self.pessoa_em_atendimento:
            self.pessoa_em_atendimento.estado = self.pessoa_em_atendimento.riscado
            if self.pessoa_em_atendimento.dupla != -1:
                dupla = self.fila.get(self.pessoa_em_atendimento.dupla)
                dupla.estado = dupla.riscado
        self.pessoa_em_atendimento = pessoa
        self.pessoa_em_atendimento.camara = self.numero_camara
        self.pessoa_em_atendimento.estado = pessoa.atendendo
        self.numero_de_atendimentos += 1
        if self.pessoa_em_atendimento.dupla != -1:
            dupla = self.fila.get(self.pessoa_em_atendimento.dupla)
            dupla.camara = self.numero_camara
            dupla.estado = dupla.atendendo
            self.numero_de_atendimentos += 1
            print("numero de atendimentos / capacidade maxima", self.numero_de_atendimentos, self.capacidade_maxima)
            # if self.numero_de_atendimentos == self.capacidade_maxima +1:
            #     print("entrou no if")
            #     self.capacidade_maxima += 1

        retorno = f'Câmara {self.numero_camara} chamando {self.pessoa_em_atendimento}.'
        if self.numero_de_atendimentos >= self.capacidade_maxima:
            self.estado = self.avisar
        self.fila.salvar_fila()
        return retorno
    
    def bolinhas(self):
        bolinhas = []
        for bola in range(0, self.numero_de_atendimentos):
            if bola > 0 and bola % 5 == 0:
                bolinhas.append('<br>&nbsp;&#9899;')
            else:
                bolinhas.append('&#9899;')
        for bola in range(self.numero_de_atendimentos, self.capacidade_maxima):
            if  bola > 0 and bola % 5 == 0:
                bolinhas.append('<br>&nbsp;&#9898;')
            else:
                bolinhas.append('&#9898;')
        return ''.join(bolinhas)
    
def salvar_camaras(dict_camaras, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for camara in dict_camaras.values():
            f.write(f'{camara.numero_camara},{camara.pessoa_em_atendimento.numero if camara.pessoa_em_atendimento is not None else ""},{camara.numero_de_atendimentos},{camara.estado},{camara.capacidade_maxima}\n')

def ler_camaras(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return f.read().splitlines()
    