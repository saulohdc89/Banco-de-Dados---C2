from model.marcas import Marcas
from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_modelos import Controller_Modelos
from controller.controller_clientes import Controller_Clientes
from controller.controller_marcas import Controller_Marcas
from controller.controller_locacoes import Controller_Locacoes
from controller.controller_automoveis import Controller_Automoveis

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_modelos = Controller_Modelos()
ctrl_clientes = Controller_Clientes()
ctrl_automoveis = Controller_Automoveis()
ctrl_marcas = Controller_Marcas()
ctrl_locacoes = Controller_Locacoes()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_pedidos_por_fornecedor()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_pedidos()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_produtos()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_clientes()
    elif opcao_relatorio == 5:
        relatorio.get_relatorio_fornecedores()
    elif opcao_relatorio == 6:
        relatorio.get_relatorio_itens_pedidos()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_cliente = ctrl_clientes.inserir_cliente()
    elif opcao_inserir == 2:
        nova_marca = ctrl_marcas.inserir_marca()
    elif opcao_inserir == 3:
        novo_modelo = ctrl_modelos.inserir_modelos()
    elif opcao_inserir == 4:
        novo_automovel = ctrl_automoveis.inserir_automovel()
    elif opcao_inserir == 5:
        nova_locacao = ctrl_locacoes.inserir_locacoes()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
      #  relatorio.get_relatorio_produtos()
        clientes_atualizado = ctrl_clientes.atualizar_produto()
    elif opcao_atualizar == 2:
       # relatorio.get_relatorio_clientes()
        print(f'sem necessidade de update') 
    elif opcao_atualizar == 3:
        # relatorio.get_relatorio_fornecedores()
        modelo_atualizado = ctrl_modelos.atualizar_modelo()
    elif opcao_atualizar == 4:
    #    relatorio.get_relatorio_pedidos()
        automovel_atualizado = ctrl_automoveis.atualizar_automoveis()
    elif opcao_atualizar == 5:
   #     relatorio.get_relatorio_itens_pedidos()
        locacao_atualizada = ctrl_locacoes.atualizar_locacoes()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
       # relatorio.get_relatorio_produtos()
        ctrl_clientes.excluir_cliente()
    elif opcao_excluir == 2:                
        #relatorio.get_relatorio_clientes()
        ctrl_marcas.excluir_marca()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_fornecedores()
        ctrl_modelos.excluir_pedido()
    elif opcao_excluir == 4:                
        #relatorio.get_relatorio_pedidos()
        ctrl_automoveis.excluir_automoveis();
    elif opcao_excluir == 5:
        #relatorio.get_relatorio_itens_pedidos()
        ctrl_locacoes.excluir_locacoes()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-6]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()