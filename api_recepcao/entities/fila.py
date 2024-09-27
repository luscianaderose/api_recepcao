from api_recepcao.entities.pessoa import Pessoa


class Fila:
    def __init__(
        self,
        atividade: str,
        nome_display: str,
        proximo_numero: int = 1,
        fila: dict[int, Pessoa] = {},
    ):
        self.atividade = atividade
        self.nome_display = nome_display
        self.fila = fila
        self.proximo_numero = proximo_numero

    def __repr__(self) -> str:
        return f"<Fila {self.atividade}>"

    def __contains__(self, numero):
        return numero in self.fila

    def to_dict(self):
        return {
            "atividade": self.atividade,
            "nome_display": self.nome_display,
            "proximo_numero": self.proximo_numero,
            "fila": {
                posicao: pessoa.to_dict() for posicao, pessoa in self.fila.items()
            },
        }

    def get(self, numero):
        if numero in self.fila:
            return self.fila[numero]
        return None

    def values(self):
        return sorted(self.fila.values(), key=lambda p: p.numero)

    def keys(self):
        return sorted(self.fila.keys())

    def clear(self):
        self.proximo_numero = 1
        self.fila.clear()

    def get_posicao(self, numero):
        if numero in self.fila:
            for index, pessoa in enumerate(self.values()):
                if pessoa.numero == numero:
                    return index + 1
        return None
