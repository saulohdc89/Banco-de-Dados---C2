class Marcas:
    def __init__(self,nome_marca:str=None):
        self.set_marcas(nome_marca)

    def set_marcas(self,nome_marca:str):
        self.nome_marca= nome_marca
    
    def get_marcas(self) -> str:
        return self.nome_marca

    def to_string(self) -> str:
        return f"Marcas: {self.get_marcas()}"