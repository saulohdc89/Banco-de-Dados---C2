from pydoc import cli
from model.marcas import Marcas
from model.modelos import Modelos
from controller.controller_marcas import Controller_Marcas
from conexion.oracle_queries import OracleQueries
from datetime import date

class Controller_Modelos:
    def __init__(self):
        self.ctrl_marcas = Controller_Marcas()
        
    def inserir_modelos(self) -> Modelos:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        
        # Lista as marcas existentes para inserir nos Modelos
        self.listar_marcas(oracle, need_connect=True)
        marca = str(input("Digite a marca: "))
        marcas = self.valida_marcas(oracle, marca)
        if marcas == None:
            return None

        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)
        novo_modelo = input("Modelo: (Novo)")

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo = output_value, nome_modelo = novo_modelo, nome_marca=marcas.get_marcas())
        # Executa o bloco PL/SQL anônimo para inserção do novo produto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := MODELOS_CODIGO_MODELOS_SEQ.NEXTVAL;
            insert into modelos values(:codigo, :nome_modelo, :nomemarca);
        end;
        """, data)
        # Recupera o código do novo modelo
        codigo_modelo = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo modelo criado transformando em um DataFrame
        df_modelo = oracle.sqlToDataFrame(f"select nome_modelo, nome_marca from pedidos where nome_modelo = {codigo_modelo}")
        # Cria um novo objeto modelo
        novo_modelo = Modelos(df_modelo.codigo_modelo.values[0], df_modelo.nome_modelo.values[0], marcas)
        # Exibe os atributos do novo produto
        print(novo_modelo.to_string())
        # Retorna o objeto novo_pedido para utilização posterior, caso necessário
        return novo_modelo

    def atualizar_modelo (self) -> Modelos:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_modelo = int(input("Código do Modelo que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_modelo(oracle, codigo_modelo):

            # Lista os marcas existentes para inserir no pedido
            self.listar_marcas(oracle)
            marca = str(input("Digite a marca: "))
            alterar_modelo = str("Alterar modelo")
            marcas = self.valida_marca(oracle, marca)
            if marcas == None:
                return None
            # Atualiza a descrição do produto existente
            oracle.write(f"update modelos set nome_modelo = '{alterar_modelo}',nome_marca = '{marcas}') where codigo_modelo = {codigo_modelo}")
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_modelo = oracle.sqlToDataFrame(f"select nome_modelo, nome_marca from pedidos where nome_modelo = {codigo_modelo}")
            # Cria um novo objeto Modelos
            modelo_atualizado = Modelos(df_modelo.codigo_modelo.values[0], df_modelo.nome_modelo.values[0], marcas.get_char())
            # Exibe os atributos do novo modelo
            print(modelo_atualizado.to_string())
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return modelo_atualizado
        else:
            print(f"O código {codigo_modelo} não existe.")
            return None

    def excluir_modelo(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do produto a ser alterado
        codigo_modelo = int(input("Código do modelo que irá excluir: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_modelo(oracle, codigo_modelo):            
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_modelo = oracle.sqlToDataFrame(f"select codigo, data_pedido, cpf, cnpj from pedidos where codigo_pedido = {codigo_modelo}")
            marcas = self.marca(oracle, df_modelo.nome_marca.values[0])
            
            opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_modelo} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                print("Atenção, caso o modelo possua itens, também serão excluídos!")
                opcao_excluir = input(f"Tem certeza que deseja excluir o pedido {codigo_modelo} [S ou N]: ")
                if opcao_excluir.lower() == "s":
                    # Remove o produto da tabela
                    oracle.write(f"delete from itens_modelo where codigo_modelo = {codigo_modelo}")
                    print("Itens do modelo removidos com sucesso!")
                    oracle.write(f"delete from pedidos where codigo_modelo = {codigo_modelo}")
                    # Cria um novo objeto modelo para informar que foi removido
                    modelo_excluido = Modelos(df_modelo.codigo_modelo.values[0], df_modelo.nome_modelo.values[0], marcas)
                    # Exibe os atributos do modeloo excluído
                    print("Pedido Removido com Sucesso!")
                    print(modelo_excluido.to_string())
        else:
            print(f"O código {codigo_modelo} não existe.")

    def verifica_existencia_modelo(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = oracle.sqlToDataFrame(f"select codigo_modelo, nome_modelo from modelo where codigo_modelo = {codigo}")
        return df_pedido.empty

    def listar_marcas(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select c.nome_marca
                from clientes c
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_marca(self, oracle:OracleQueries, marca:str=None) -> Marcas:
        if self.ctrl_marcas.verifica_existencia_marca(oracle, marca):
            print(f"A marca {marca} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_marca = oracle.sqlToDataFrame(f"select nome_marca from marca where marca = {marca}")
            # Cria um novo objeto cliente
            cliente = Marcas(df_marca .marca.values[0])
            return cliente
