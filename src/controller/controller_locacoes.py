from model.locacoes import Locacoes
from model.clientes import Clientes
from model.automoveis import Automoveis
from model.modelos import Modelos
from model.marcas import Marcas
from controller.controller_clientes import Controller_Clientes
from controller.controller_automoveis import Controller_Automoveis
from controller.controller_modelos import Controller_Modelos
from controller.controller_marcas import Controller_Marcas
from conexion.oracle_queries import OracleQueries
from datetime import date

class Controller_Locacoes:
    def __init__(self):
        self.ctrl_clientes = Controller_Clientes()
        self.ctrl_automoveis = Controller_Automoveis()
        self.ctrl_marcas= Controller_Marcas()
        self.ctrl_modelos = Controller_Modelos()
        


    def inserir_locacoes(self) -> Locacoes:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        data_hoje = date.today()
        # Lista os automoveis existentes para inserir na locacao
        self.listar_clientes(oracle, need_connect=True)
        n_cpf = str(input("Digite o número do CPF do Cliente: "))
        cliente = self.valida_cliente(oracle, n_cpf)
        if cliente == None:
            return None

        # Lista os modelos existentes para inserir no locacao
        self.listar_modelos(oracle, need_connect=True)
        novo_modelo = str(input("Digite modelo: "))
        modelos = self.valida_modelo(oracle, novo_modelo)
        if modelos == None:
            return None

        #Lista os modelos existentes para inserir no locacao
        self.listar_marcas(oracle, need_connect=True)
        novo_marcas = str(input("Digite a marca  "))
        marcas = self.valida_marca(oracle, novo_marcas)
        if marcas == None:
            return None


        self.listar_automoveis(oracle, need_connect=True)
        codigo_automoveis = str(input("Digite a placa do automovel: "))
        automoveis = self.valida_automoveis(oracle, codigo_automoveis)
        if automoveis == None:
            return None
        # Solicita a quantidade de itens do pedido para o produto selecionado
        # Solicita o valor unitário do produto selecionado
        idata_devolucao = input("Data de devolucao:")

        # Recupera o cursor para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(data_devolucao = idata_devolucao, cpf=cliente.get_cpf(),Placa =automoveis.get_Placa() ,nome_modelo = modelos.get_modelo(),nome_marca = marcas.get_marcas(),data_locacao = data_hoje)
        # Executa o bloco PL/SQL anônimo para inserção do novo item de pedido e recuperação da chave primária criada pela sequence

        #Locacaoes data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao
        cursor.execute("""
        begin
            :cpf := LOCACOES_SEQ.NEXTVAL;
            insert into locacoes values(data_devolucao:cpf,:nome_modelo,:nome_marca :data_locacao);
        end;
        """, data)
       
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo item de pedido criado transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(f"select data_devolucao, cpf, placa, nome_modelo, nome_marca, data_locacao from locacoes where cpf = {n_cpf}")
        # Cria um novo objeto Item de Pedido
        nova_locacao = Locacoes(df_locacao.data_devolucao.values[0],cliente,automoveis,marcas,df_locacao.data_locacao.values[0])
        # Exibe os atributos do novo Item de Pedido
        print(nova_locacao.to_string())
        # Retorna o objeto novo_item_pedido para utilização posterior, caso necessário
        return nova_locacao

    def atualizar_locacoes (self) -> Locacoes:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        codigo_item_pedido = input("Digite o cpf: ")        

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_locacoes(oracle, codigo_item_pedido):

            data_hoje = date.today()

            # Lista os pedido existentes para inserir no item de pedido
            self.listar_clientes(oracle, need_connect=True)
            cpf = str(input("Digite o número do CPF do Cliente: "))
            cliente = self.valida_cliente(oracle, cpf)
            if cliente == None:
                return None

            # Lista os produtos existentes para inserir no item de pedido
            self.listar_modelos(oracle, need_connect=True)
            novo_modelo = str(input("Digite o modelo "))
            modelos = self.valida_modelo(oracle, novo_modelo)
            if modelos == None:
                return None
            
            self.listar_automoveis(oracle, need_connect=True)
            codigo_automoveis = str(input("Digite a placa do automovel: "))
            automoveis = self.valida_automoveis(oracle, codigo_automoveis)
            if automoveis == None:
                return None

            idata_devolucao = input("Data de devolucao:")
            data_hoje = date.today()

            # Atualiza o item de pedido existente
            oracle.write(f"update locacoes set data_locacao = {data_hoje}, data_devolucao = {idata_devolucao}, where cpf = {cpf}")
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_locacao = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where data_devolucao = {cpf}")
            # Cria um novo objeto Item de Pedido
            nova_locacao = Locacoes(df_locacao.data_devolucao.values[0],cliente,automoveis,modelos,modelos.get_marcas_modelo(),df_locacao.data_locacao.values[0])
            # Exibe os atributos do item de pedido
            print(nova_locacao.to_string())
            # Retorna o objeto pedido_atualizado para utilização posterior, caso necessário
            return nova_locacao
        else:
            print(f"O {cpf} não existe.")
            return None

    def excluir_locacoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do item de pedido a ser alterado
        cpf = str(input("Digite o número do CPF do Cliente: "))        

        # Verifica se o item de pedido existe na base de dados
        if not self.verifica_existencia_locacoes(oracle, cpf):            
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_locacao = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where cpf = {cpf}")
            modelos = self.valida_modelo(oracle, df_locacao.nome_modelos.value[0])
            marcas = self.valida_marca(oracle, df_locacao.nome_marca.value[0])
            automoveis = self.valida_automoveis(oracle, df_locacao.Placa.value[0])
            
            
            opcao_excluir = input(f"Tem certeza que deseja excluir locacao CFP {cpf} [S ou N]: ")
            if opcao_excluir.lower() == "s":
                # Revome o produto da tabela
                oracle.write(f"delete from locacao where cpf = {cpf}")                
                # Cria um novo objeto Item de Pedido para informar que foi removido
                item_pedido_excluido = Locacoes(df_locacao.data_devolucao.values(0), df_locacao.Placa.values(0),df_locacao.nome_modelo.values(0),df_locacao.nome_marca.values(0),df_locacao.data_locacao.values(0))
                # Exibe os atributos do produto excluído
                print("Item do Pedido Removido com Sucesso!")
                print(item_pedido_excluido.to_string())
        else:
            print(f"O código {cpf} não existe.")

    def verifica_existencia_locacoes(self, oracle:OracleQueries, cpf) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where data_locacao = {cpf}")
        return df_pedido.empty

    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select C.CPF
                , C.NOME
                , C.TELEFONE 
                ,C.ENDERECO
                from CLIENTES C
                order by C.NOME
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_modelos(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select M.NOME_MODELO
                , M.NOME_MARCA
                , MC.NOME_MARCA as MARCAS
                from MODELOS M
                inner join MARCAS MC
                on  M.NOME_MARCA = MC.NOME_MARCA
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_automoveis(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select A.PLACA
                , A.NOME_MODELO
                , A.NOME_MARCA
                , A.RENAVAM
                , A.COR
                , A.N_PORTAS
                , A.TIPO_COMBUSTIVEL
                , M.NOME_MODELO as MODELOS
                , MC.NOME_MARCA as MARCAS
                from AUTOMOVEIS A
                inner join MODELOS M
                on A.NOME_MODELO = M.NOME_MODELO
                inner join A.NOME_MARCA MC
                on A.NOME_MARCA = MC.NOME_MARCA
                left join MARCAS MC
                on M.NOME_MARCA = MC.NOME_MARCA
                order by A.PLACA
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_marca(self, oracle:OracleQueries, marca:int=None) -> Modelos:
        if self.ctrl_marcas.verifica_existencia_marca(oracle, marca):
            print(f"O pedido {marca} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_marca = oracle.sqlToDataFrame(f"select nome_marca from marcas where nome_marca = {marca}")
            modelo = self.ctrl_modelos.valida_marca(oracle, df_marca.nome_modelo.values[0])
            # Cria um novo objeto cliente
            modelos = Modelos(df_marca.nome_marca.values[0])
            return modelos

    def valida_modelo(self, oracle:OracleQueries, nome_modelo:int=None) -> Modelos:
        if self.ctrl_modelos.verifica_existencia_modelo(oracle, nome_modelo):
            print(f"O pedido {nome_modelo} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_modelo = oracle.sqlToDataFrame(f"select nome_modelo nome_marca from modelos where nome_modelo = {nome_modelo}")
            modelo = self.ctrl_modelos.valida_marca(oracle, df_modelo.nome_modelo.values[0])
            # Cria um novo objeto cliente
            modelos = Modelos(df_modelo.nome_modelo.values[0], df_modelo.nome_marca.values[0])
            return modelos

    def valida_cliente(self, oracle:OracleQueries, cliente:int=None) -> Clientes:
        if self.ctrl_clientes.verifica_existencia_cliente(oracle, cliente):
            print(f"O produto {cliente} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select cpf,nome,endereco,telefone from clientes where cliente = {cliente}")
            # Cria um novo objeto Produto
            cliente = Clientes(df_cliente.cpf.values[0], df_cliente.nome.values[0],df_cliente.endereco.values[0],df_cliente.telefone.values)
            return cliente
    def valida_automoveis(self, oracle:OracleQueries, placa:int=None) -> Clientes:
        if self.ctrl_automoveis.verifica_existencia_automoveis(oracle, placa):
            print(f"O produto {placa} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_cliente = oracle.sqlToDataFrame(f"select placa,nome_modelo,nome where  automoveis = {placa}")
            # Cria um novo objeto Produto
            placa = Clientes(df_cliente.cpf.values[0], df_cliente.nome.values[0],df_cliente.endereco.values[0],df_cliente.telefone.values)
            return placa