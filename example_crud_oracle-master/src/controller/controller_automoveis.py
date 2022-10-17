from controller.controller_marcas import Controller_Marcas
from controller.controller_modelos import Controller_Modelos
from model.automoveis import Automoveis
from model.marcas import Marcas
from model.modelos import Modelos
from conexion.oracle_queries import OracleQueries


class Controller_Automoveis:
    def __init__(self):
        self.ctrl_modelos = Controller_Modelos()
        self.ctrl_marcas = Controller_Marcas()
        
    def inserir_automovel(self) -> Automoveis:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Lista as marcas existentes para inserir em automoveis
        self.listar_marcas(oracle, need_connect=True)
        marca = str(input("Digite nome da marca: "))
        r_nome_marca = self.valida_marca(oracle, marca)
        if r_nome_marca == None:
            return None

        # Lista os modelos existentes para inserir em automoveis
        self.listar_modelos(oracle, need_connect=True)
        modelo = str(input("Digite o nome do modelo: "))
        r_nome_modelo = self.valida_modelo(oracle, modelo)
        if r_nome_modelo == None:
            return None


        #Solicita ao usuario a nova Placa
        nova_Placa = input("Placa (Novo): ")
        renavam =  input("RENAVAM: ")
        nova_cor = input("Cor:")
        N_portas = input("Numero de portas:")
        tipo_combustivel = input("Tipo de combustivel")

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, Placa = nova_Placa,r_nome_modelo = r_nome_modelo,nome_marca = r_nome_marca,RENAVAM = renavam,cor =nova_cor,n_portas=N_portas, combustivel = tipo_combustivel )
        # Executa o bloco PL/SQL anônimo para inserção do novo automovel  e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := AUTOMOVEIS_CODIGO_AUTOMOVEIS_SEQ.NEXTVAL;
            insert into automoveis values(:codigo,: nome_modelo,:nome_marca,:renavam,cor,:N_portas,:tipo_combustivel));
        end;
        """, data)
        # Recupera o código do novo produto
        codigo_automovel = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_automoveis = oracle.sqlToDataFrame(f"select codigo_produto, descricao_produto from produtos where codigo_produto = {codigo_automovel}")
        # Cria um novo objeto Produto
        novo_automoveis = Automoveis(df_automoveis.codigo_automovel.values[0], df_automoveis.values[0])
        # Exibe os atributos do novo produto
        print(novo_automoveis.to_string())
        # Retorna o objeto novo_produto para utilização posterior, caso necessário
        return novo_automoveis

    def atualizar_automoveis(self) -> Automoveis:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do automoveis a ser alterado
        codigo_automoveis = int(input("Código do Automoveis que irá alterar: "))        

        # Verifica se o produto existe na base de dados
        if not self.verifica_existencia_produto(oracle, codigo_automoveis):
            # Solicita a nova descrição do produto
            nova_descricao_produto = input("Descrição (Novo): ")
            # Atualiza a descrição do produto existente
            oracle.write(f"update produtos set descricao_produto = '{nova_descricao_produto}' where codigo_produto = {codigo_produto}")
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_automoveis = oracle.sqlToDataFrame(f"select c:codigo, nome_modelo,nome_marca,renavam,cor,N_portas,:tipo_combustivel from produtos where codigo_produto = {codigo_produto}")
            # Cria um novo objeto Produto
            produto_atualizado = Automoveis(df_automoveis.codigo_produto.values[0], df_automoveis.df_automoveis.values[0])
            # Exibe os atributos do novo produto
            print(produto_atualizado.to_string())
            # Retorna o objeto produto_atualizado para utilização posterior, caso necessário
            return produto_atualizado
        else:
            print(f"O código {codigo_produto} não existe.")
            return None

    def excluir_automoveis(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do automoveis a ser alterado
        codigo_automoveis = int(input("Código do automoveis que irá excluir: "))        

        # Verifica se o automoveis existe na base de dados
        if not self.verifica_existencia_automoveis(oracle, codigo_produto):            
            # Recupera os dados do novo automoveis criado transformando em um DataFrame
            df_produto = oracle.sqlToDataFrame(f"select codigo_produto, descricao_produto from produtos where codigo_produto = {codigo_produto}")
            # Revome o produto da tabela
            oracle.write(f"delete from produtos where codigo_produto = {codigo_produto}")            
            # Cria um novo objeto Produto para informar que foi removido
            produto_excluido = Automoveis(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            # Exibe os atributos do produto excluído
            print("Produto Removido com Sucesso!")
            print(produto_excluido.to_string())
        else:
            print(f"O código {codigo_produto} não existe.")

    def verifica_existencia_automoveis(self, oracle:OracleQueries, codigo:int=None) -> bool:
        # Recupera os dados do novo produto criado transformando em um DataFrame
        df_produto = oracle.sqlToDataFrame(f"select codigo_produto, descricao_produto from produtos where codigo_produto = {codigo}")
        return df_produto.empty 