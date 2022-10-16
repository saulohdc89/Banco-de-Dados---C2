class Marcas:
    def __init__(self,marcas:str=None):
        self.set_marcas(marcas)

    def set_marcas(self,marcas:str):
        self.marcas= marcas
    
    def get_marcas(self) -> str:
        return self.marcas

    def to_string(self) -> str:
        return f"Marcas: {self.get_marcas()}"