class Automoveis:
    def __init__(self,Placa:str=None,nome_modelo:str=None,nome_marca:str=None,renavam:str=None,cor:str=None,N_portas:str=None,tipo_combustivel:str=None ):
        self.set_Placa(Placa)
        self.set_nome_modelo(nome_modelo)
        self.set_nome_marca(nome_marca)
        self.set_renavam(renavam)
        self.set_cor(cor)
        self.set_N_portas(N_portas)
        self.set_tipo_combustivel(tipo_combustivel)

    def set_Placa(self,Placa):
        self.Placa = Placa
    
    def set_nome_modelo(self,nome_modelo):
        self.nome_modelo = nome_modelo
    
    def set_nome_marca(self,nome_marca):
        self.nome_marca = nome_marca
    
    def set_renavam(self,renavam):
        self.renavam = renavam

    def set_cor(self,cor):
        self.cor = cor
    
    def set_N_portas(self,N_portas):
        self.N_portas = N_portas

    def set_tipo_combustivel(self,tipo_combustivel):
        self.tipo_combustivel = tipo_combustivel


    def get_Placa(self) -> str:
        return self.Placa 
    
    def get_nome_modelo(self) -> str:
        return self.nome_modelo
    
    def get_nome_marca(self) -> str:
        return self.nome_marca
    
    def get_renavam(self) -> str:
        return self.renavam

    def get_cor(self)  -> str:
        return self.cor
    
    def get_N_portas(self) -> str:
        return self.N_portas

    def get_tipo_combustivel(self) -> str:
        return self.tipo_combustivel 

    def to_string(self) -> str:
        return f"Placa: {self.get_Placa()} | Nome modelo: {self.get_nome_modelo()} | Nome  da Marca: {self.get_nome_marca()} | Renavam: {self.get_renavam()} | cor: {self.get_cor} | Numero de portas: {self.get_N_portas} | Tipo de combustivel: {self.get_tipo_combustivel} |" 
    
