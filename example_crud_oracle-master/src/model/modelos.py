from asyncio import constants


class Modelos:
    def __init__(self,nome_modelo:str=None, marcas_modelo:str=None):
        self.set_nome_modelo(nome_modelo)
        self.set_marcas_modelo(marcas_modelo)

    def set_nome_modelo(self, nome:str):
        self.nome = nome

    def set_marcas_modelo(self, marcas_modelo:str):
        self.marcas_modelo = marcas_modelo
    
    def get_nome_modelo(self) -> str:
        return self.nome_modelo
    
    def get_marcas_modelo(self) -> str:
        return self.nome_modelo

    def to_string(self) -> str:
        return f"Nome modelo: {self.get_nome_modelo()} Marcas modelo: {self.get_marcas_modelo()}"
    