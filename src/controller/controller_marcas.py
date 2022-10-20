from model.marcas import Marcas
from conexion.oracle_queries import OracleQueries

class Controller_Marcas:
    def __init__(self):
        pass
        
    def inserir_marca(self) -> Marcas:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CNPJ
        nome_marca = input("Marca(nova): ")

        if self.verifica_existencia_marca(oracle, nova_marca):            
            oracle.write(f"insert into fornecedores values ('{nome_marca}')")
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_fornecedor = oracle.sqlToDataFrame(f"select nome_marca from marcas where nome_marca = '{nome_marca}'")
            # Cria um novo objeto fornecedor
            nova_marca = Marcas(df_fornecedor.nome_marcas.values[0])
            # Exibe os atributos do novo fornecedor
            print(nova_marca.to_string())
            # Retorna o objeto novo_fornecedor para utilização posterior, caso necessário
            return nova_marca
        else:
            print(f"A {nova_marca} já está cadastrado.")
            return None

    

    def excluir_marca(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()


        marca = int(input("Nome da marca que deseja excluir: "))        

        # Verifica se o fornecedor existe na base de dados
        if not self.verifica_existencia_marca(oracle, marca):            
            # Recupera os dados do novo fornecedor criado transformando em um DataFrame
            df_marca = oracle.sqlToDataFrame(f"select nome_marca from marcas where nome_marca = {marca}")
            # Revome o fornecedor da tabela
            oracle.write(f"delete from nome_marca where nome_marca = {marca}")            
            # Cria um novo objeto fornecedor para informar que foi removido
            fornecedor_excluido = Marcas(df_marca.nome_marcas.values[0])
            # Exibe os atributos do fornecedor excluído
            print("fornecedor Removido com Sucesso!")
            print(fornecedor_excluido.to_string())
        else:
            print(f"O CNPJ {marca} não existe.")

    def verifica_existencia_marca(self, oracle:OracleQueries, marca:str=None) -> bool:
        # Recupera os dados do novo fornecedor criado transformando em um DataFrame
        df_marca = oracle.sqlToDataFrame(f"select nome_marca from marcas where nome_marca = {marca}")
        return df_marca.empty