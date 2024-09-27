class Pessoa:
    riscado = "riscado"
    atendendo = "atendendo"
    aguardando = "aguardando"

    def __init__(
        self,
        numero: int,
        nome: str,
        estado: str = "aguardando",
        dupla_numero: int = None,
        observacao: str = "",
        numero_camara: str = None,
        fila_atividade: str = None,
    ):
        self.nome = nome
        self.numero = numero
        self.estado = estado
        self.numero_camara = numero_camara
        self.dupla_numero = dupla_numero
        self.observacao = observacao
        self.fila_atividade = fila_atividade

    def __repr__(self) -> str:
        return f"<Pessoa {self.numero}>"

    def to_dict(self):
        return {
            "nome": self.nome,
            "numero": self.numero,
            "estado": self.estado,
            "numero_camara": self.numero_camara,
            "dupla_numero": self.dupla_numero,
            "observacao": self.observacao,
            "fila_atividade": self.fila_atividade,
        }

    def __str__(self):
        return self.nome
