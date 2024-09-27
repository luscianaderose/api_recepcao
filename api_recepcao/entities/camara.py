from api_recepcao.entities.fila import Fila
from api_recepcao.entities.pessoa import Pessoa


class Camara:
    fechada = "fechada"
    atendendo = "atendendo"
    avisar = "último"
    avisado = "Foi avisado"

    def __init__(
        self,
        numero: str,
        estado: str = fechada,
        capacidade_maxima: int = 5,
        numero_de_atendimentos: int = 0,
        fila_atividade: str = None,
        pessoa_em_atendimento: Pessoa = None,
    ):
        self.numero = numero
        self.fila_atividade = fila_atividade
        self.pessoa_em_atendimento = pessoa_em_atendimento
        self.numero_de_atendimentos = numero_de_atendimentos
        self.estado = estado
        self.capacidade_maxima = capacidade_maxima

    def __repr__(self) -> str:
        return f"<Camara {self.numero}>"

    def to_dict(self):
        return {
            "numero": self.numero,
            "fila_atividade": self.fila_atividade,
            "numero_de_atendimentos": self.numero_de_atendimentos,
            "estado": self.estado,
            "capacidade_maxima": self.capacidade_maxima,
            "pessoa_em_atendimento": (
                self.pessoa_em_atendimento.to_dict()
                if self.pessoa_em_atendimento
                else None
            ),
        }

    def fechar(self):
        self.pessoa_em_atendimento = None
        self.estado = self.fechada

    def abrir(self):
        self.numero_de_atendimentos = 0
        self.estado = self.atendendo
