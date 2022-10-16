from typing_extensions import Self


class Locacoes:
    def __init__(self,data_devolucao:str=None, cpf:str=None, Placa:str=None, nome_modelo:str=None, nome_marca:str=None, data_locacao:str=None):
        self.set_data_devolucao(data_devolucao)
        self.set_cpf(cpf)
        self.set_Placa(Placa)
        self.set_nome_modelo(nome_modelo)
        self.set_nome_marca(nome_marca)
        self.set_data_locacao(data_locacao)

    def set_data_devolucao(self,data_devolucao:str):
        self.data_devolucao=data_devolucao
    
    def set_cpf(self,cpf:str):
        self.cpf= cpf
    
    def set_Placa(self,Placa:str):
        self.Placa = Placa
    
    def set_nome_modelo(self,nome_modelo:str):
        self.nome_modelo = nome_modelo
    
    def set_nome_marca(self,nome_marca:str):
        self.nome_modelo = nome_marca
    
    def set_data_locacao(self,data_locacao):
        self.data_locacao = data_locacao


    def get_data_devolucao(self) -> str:
        return self.data_devolucao

    def get_cpf(self) -> str:
        return self.cpf
    
    def get_Placa(self) -> str:
        return self.Placa
    
    def get_nome_modelo(self) -> str:
        return self.nome_modelo
    
    def get_nome_marca(self) -> str:
        return self.nome_marca
    
    def get_data_locacao(self) -> str:
        return self.data_locacao

    def to_string(self) -> str:
        return f"Data de devolução: {self.get_data_devolucao()} | CPF: {self.get_cpf()} | Placa: {self.get_Placa} | Nome do modelo: {self.get_nome_modelo} | Nome da marca {self.get_nome_marca} | Devolução: {self.get_data_devolucao}" 