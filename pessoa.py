class Pessoa:
    riscado = 'riscado'
    atendendo = 'atendendo'
    aguardando = 'aguardando'
    
    def __init__(self, numero, nome, estado='aguardando', camara=None, dupla=-1, asterisco=0, observacao=''):
        self.nome = nome
        self.numero = numero
        self.estado = estado
        self.camara = camara
        self.dupla = dupla
        self.asterisco = asterisco
        self.observacao = observacao

    def to_dict(self):
        return {
            "nome": self.nome,
            "numero": self.numero,
            "estado": self.estado,
            "camara": self.camara,
            "dupla": self.dupla,
            "asterisco": self.asterisco,
            "observacao": self.observacao
        }

    def __str__(self):
        return self.nome
     
    def csv(self):
        return f'{self.numero},{self.nome},{self.estado},{self.camara},{self.dupla},{self.asterisco},{self.observacao}'
    
    def nome_exibicao(self):
        if self.estado == self.riscado:
            return f'<s>{self.nome}</s> - {self.camara}'
        elif self.estado == self.atendendo:
            return f'<b>{self.nome}</b> - {self.camara}'
        else:
            return f'{self.nome}'
        
    def __repr__(self):
        return self.nome
