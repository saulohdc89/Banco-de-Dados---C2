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
        df_locacao = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where cpf = {n_cpf}")
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

            idata_devolucao = input("Data de devolucao:")
            data_hoje = date.today()

            # Atualiza o item de pedido existente
            oracle.write(f"update locacoes set data_locacao = {data_hoje}, data_devolucao = {idata_devolucao}, where cpf = {cpf}")
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_locacao = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where data_devolucao = {cpf}")
            # Cria um novo objeto Item de Pedido
            nova_locacao = Locacoes(df_locacao.data_devolucao.values[0],cliente.automoveis,marcas,df_locacao.data_locacao.values[0])
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
        if not self.verifica_existencia_locacao(oracle, cpf):            
            # Recupera os dados do novo item de pedido criado transformando em um DataFrame
            df_locacao = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where cpf = {cpf}")
            modelos = self.valida_modelo(oracle, df_locacao.nome_modelos.value[0])
            marcas = self.valida_marca(oracle, df_locacao.nome_marca.value[0]))
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
            print(f"O código {codigo_item_pedido} não existe.")

    def verifica_existencia_locacoes(self, oracle:OracleQueries, cpf) -> bool:
        # Recupera os dados do novo pedido criado transformando em um DataFrame
        df_pedido = oracle.sqlToDataFrame(f"select data_devolucao, cpf, Placa, nome_modelo, nome_marca, data_locacao from locacoes where cpf = {cpf}")
        return df_pedido.empty

    def listar_clientes(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select dl.cpf
                    , c.cpf as cliente
                    , c.nome as cliente
                    , c.endereco as cliente
                    , prd.descricao_produto as produto
                    , i.quantidade
                    , i.valor_unitario
                    , 
                from pedidos p
                inner join clientes c
                on p.cpf = c.cpf
                inner join fornecedores f
                on p.cnpj = f.cnpj
                left join itens_pedido i
                on p.codigo_pedido = i.codigo_pedido
                left join produtos prd
                on i.codigo_produto = prd.codigo_produto
                order by c.nome
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_modelos(self, oracle:OracleQueries, need_connect:bool=False):
        query = """
                select prd.codigo_produto
                    , prd.descricao_produto 
                from produtos prd
                order by prd.descricao_produto 
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_pedido(self, oracle:OracleQueries, codigo_pedido:int=None) -> Pedido:
        if self.ctrl_pedido.verifica_existencia_pedido(oracle, codigo_pedido):
            print(f"O pedido {codigo_pedido} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_pedido = oracle.sqlToDataFrame(f"select codigo_pedido, data_pedido, cpf, cnpj from pedidos where codigo_pedido = {codigo_pedido}")
            cliente = self.ctrl_pedido.valida_cliente(oracle, df_pedido.cpf.values[0])
            fornecedor = self.ctrl_pedido.valida_fornecedor(oracle, df_pedido.cnpj.values[0])
            # Cria um novo objeto cliente
            pedido = Pedido(df_pedido.codigo_pedido.values[0], df_pedido.data_pedido.values[0], cliente, fornecedor)
            return pedido

    def valida_produto(self, oracle:OracleQueries, codigo_produto:int=None) -> Produto:
        if self.ctrl_produto.verifica_existencia_produto(oracle, codigo_produto):
            print(f"O produto {codigo_produto} informado não existe na base.")
            return None
        else:
            oracle.connect()
            # Recupera os dados do novo produto criado transformando em um DataFrame
            df_produto = oracle.sqlToDataFrame(f"select codigo_produto, descricao_produto from produtos where codigo_produto = {codigo_produto}")
            # Cria um novo objeto Produto
            produto = Produto(df_produto.codigo_produto.values[0], df_produto.descricao_produto.values[0])
            return produto