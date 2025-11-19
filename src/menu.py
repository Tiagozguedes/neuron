"""Menu interativo principal da solução Neuron."""

from __future__ import annotations

from typing import Callable

from actors import acessos, categorias_emocao, departamentos, emocoes, registros_emocao, respostas_formulario, usuarios
from actors.checkins import realizar_checkin_emocional
from connect.connect import verificar_conexao_oracle
from utils import input_opcao, limpar_tela, pausar, titulo

MenuAction = Callable[[], None]


def main() -> None:
    """Exibe o menu principal agrupando as funcionalidades por intenção."""
    try:
        oracle_status = verificar_conexao_oracle()
    except RuntimeError as exc:
        limpar_tela()
        print("Não foi possível iniciar porque o Oracle não respondeu.")
        print(exc)
        pausar("Pressione Enter para sair...")
        return
    while True:
        limpar_tela()
        print("===========================================")
        print("        SISTEMA NEURON — MENU PRINCIPAL    ")
        print("===========================================\n")
        print(f"{oracle_status}\n")
        print("1. Cadastros básicos")
        print("2. Realizar check-in emocional (envia seu relato para a IA)")
        print("3. Consultas e relatórios agregados de emoções")
        print("0. Sair")
        opcao = input_opcao("\nEscolha uma opção: ", ("1", "2", "3", "0"))
        if opcao == "0":
            print("\nAté breve!")
            break
        if opcao == "1":
            _menu_cadastros()
        elif opcao == "2":
            realizar_checkin_emocional()
        elif opcao == "3":
            _abrir_menu_consultas()


def _menu_cadastros() -> None:
    """Menu intermediário com os cadastros essenciais do RH."""
    while True:
        limpar_tela()
        titulo("Cadastros básicos")
        print("1. Gerenciar colaboradores")
        print("2. Gerenciar departamentos")
        print("3. Gerenciar perfis de acesso")
        print("4. Gerenciar emoções e categorias")
        print("0. Voltar")
        opcao = input_opcao("\nSelecione uma opção: ", ("1", "2", "3", "4", "0"))
        if opcao == "0":
            break
        if opcao == "1":
            _menu_crud(
                "Colaboradores",
                "colaborador",
                usuarios.cadastrar_usuario,
                usuarios.listar_usuarios,
                usuarios.atualizar_usuario,
                usuarios.excluir_usuario,
            )
        elif opcao == "2":
            _menu_crud(
                "Departamentos",
                "departamento",
                departamentos.cadastrar_departamento,
                departamentos.listar_departamentos,
                departamentos.atualizar_departamento,
                departamentos.excluir_departamento,
            )
        elif opcao == "3":
            _menu_crud(
                "Perfis de acesso",
                "perfil de acesso",
                acessos.cadastrar_acesso,
                acessos.listar_acessos,
                acessos.atualizar_acesso,
                acessos.excluir_acesso,
            )
        elif opcao == "4":
            _menu_emocoes_e_categorias()


def _menu_emocoes_e_categorias() -> None:
    while True:
        limpar_tela()
        titulo("Emoções e Categorias")
        print("1. Gerenciar emoções")
        print("2. Gerenciar categorias de emoção")
        print("3. Registros emocionais")
        print("4. Respostas de formulários")
        print("0. Voltar")
        opcao = input_opcao("\nSelecione uma opção: ", ("1", "2", "3", "4", "0"))
        if opcao == "0":
            break
        if opcao == "1":
            _menu_crud(
                "Emoções",
                "emoção",
                emocoes.cadastrar_emocao,
                emocoes.listar_emocoes,
                emocoes.atualizar_emocao,
                emocoes.excluir_emocao,
            )
        elif opcao == "2":
            _menu_crud(
                "Categorias de emoção",
                "categoria",
                categorias_emocao.cadastrar_categoria,
                categorias_emocao.listar_categorias,
                categorias_emocao.atualizar_categoria,
                categorias_emocao.excluir_categoria,
            )
        elif opcao == "3":
            _menu_crud(
                "Registros emocionais",
                "registro emocional",
                registros_emocao.cadastrar_registro_emocao,
                registros_emocao.listar_registros_emocao,
                registros_emocao.atualizar_registro_emocao,
                registros_emocao.excluir_registro_emocao,
            )
        elif opcao == "4":
            _menu_crud(
                "Respostas de formulários",
                "resposta",
                respostas_formulario.cadastrar_resposta_formulario,
                respostas_formulario.listar_respostas_formulario,
                respostas_formulario.atualizar_resposta_formulario,
                respostas_formulario.excluir_resposta_formulario,
            )


def _menu_crud(
    titulo_menu: str,
    nome_item: str,
    cadastrar: MenuAction,
    listar: MenuAction,
    atualizar: MenuAction,
    excluir: MenuAction,
) -> None:
    """Renderiza um menu padronizado de CRUD."""
    while True:
        limpar_tela()
        print(f"------ Gerenciar {titulo_menu.upper()} ------")
        print(f"1. Cadastrar {nome_item}")
        print(f"2. Listar {titulo_menu.lower()}")
        print(f"3. Editar {nome_item}")
        print(f"4. Excluir {nome_item}")
        print("0. Voltar")
        opcao = input_opcao("\nEscolha uma opção: ", ("1", "2", "3", "4", "0"))
        if opcao == "0":
            break
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            excluir()
        else:
            print("Opção inválida. Tente novamente.")
            pausar()


def _abrir_menu_consultas() -> None:
    """Importação tardia para evitar dependência circular."""
    from actors.consultas import menu_consultas

    menu_consultas()


if __name__ == "__main__":  # pragma: no cover
    main()
