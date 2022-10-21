from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_marcas = config.QUERY_COUNT.format(tabela="marcas")
        self.qry_total_clientes = config.QUERY_COUNT.format(tabela="clientes")
        self.qry_total_modelos = config.QUERY_COUNT.format(tabela="modelos")
        self.qry_total_automoveis = config.QUERY_COUNT.format(tabela="automoveis")
        self.qry_total_locacoes= config.QUERY_COUNT.format(tabela="locacoes")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = "Saulo Henrique de Castro / Paulo Henrique Oliveira Marciano / Flavio Roberto Viera / Lukas da Silva Nascimento ?/ Matheus Moreiras Alves/ Fernando Carlos Vidal da Silva "
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2022/2"

    def get_total_marcas(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_marcas)["total_marcas"].values[0]

    def get_total_clientes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_clientes)["total_clientes"].values[0]

    def get_total_modelos(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_modelos)["total_modelos"].values[0]

    def get_total_automoveis(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_automoveis)["total_automoveis"].values[0]

    def get_total_locacaoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_locacoes)["total_locacoes"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #                   SISTEMA DE LOCACAO DE CARROS                     
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - CLIENTES:         {str(self.get_total_clientes()).rjust(5)}
        #      2 - MARCAS:         {str(self.get_total_marcas()).rjust(5)}
        #      3 - MODELOS:     {str(self.get_total_modelos()).rjust(5)}
        #      4 - AUTOMOVEIS:          {str(self.get_total_automoveis()).rjust(5)}
        #      5 - LOCACAO: {str(self.get_total_locacaoes()).rjust(5)}
        #
        #  CRIADO POR: {self.created_by}
        #
        #  PROFESSOR:  {self.professor}
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        ########################################################
        """