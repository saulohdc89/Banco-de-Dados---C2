class Clientes:
    def __init__(self,cpf:str=None,nome:str=None,endereco:str=None,telefone:str=None):
        self.set_cpf(cpf)
        self.set_nome(nome)
        self.set_endereco(endereco)
        self.set_telefone(telefone)
    
    def set_cpf(self,cpf:str):
        self.cpf= cpf
    
    def set_nome(self, nome:str):
        self.nome = nome
    
    def set_endereco(self, endereco:str):
        self.endereco = endereco
    
    def set_telefone(self, telefone:str):
        self.nome = telefone
    
    def get_cpf(self) -> str:
        return self.cpf

    def get_nome(self) -> str:
        return self.nome
    
    def get_endereco(self) -> str:
        return self.endereco
    
    def get_telefone(self) -> str:
        return self.nome
    
    def to_string(self) -> str:
        return f"CPF: {self.get_cpf()} | Nome: {self.get_nome()} | Endereço: {self.get_endereco()} | Telefone: {self.get_telefone()}"


