"""Menu interativo principal da solução Neuron."""

from __future__ import annotations

from typing import Callable

from actors import (
    acessos,
    categorias_emocao,
    departamentos,
    emocoes,
    registros_emocao,
    respostas_formulario,
    usuarios,
)
from actors.checkins import realizar_checkin_emocional
from utils import deseja_voltar, limpar_tela, pausar

MenuAction = Callable[[], None]


def main() -> None:
    """Exibe o menu raiz com as principais funcionalidades do sistema."""
    while True:
        limpar_tela()
        print("=== Neuron • Console Administrativo ===")
        print("1. Gerenciar usuários")
        print("2. Gerenciar departamentos")
        print("3. Gerenciar tipos de acesso")
        print("4. Gerenciar emoções")
        print("5. Gerenciar categorias de emoção")
        print("6. Gerenciar registros emocionais")
        print("7. Gerenciar respostas de formulário")
        print("8. Realizar check-in emocional")
        print("9. Consultas e relatórios (JSON)")
        print("0. Sair")
        entrada = input("\nSelecione uma opção: ").strip()
        if deseja_voltar(entrada):
            print("\nAté breve!")
            break
        opcao = entrada
        if opcao == "1":
            _menu_crud(
                "Usuários",
                usuarios.cadastrar_usuario,
                usuarios.listar_usuarios,
                usuarios.atualizar_usuario,
                usuarios.excluir_usuario,
            )
        elif opcao == "2":
            _menu_crud(
                "Departamentos",
                departamentos.cadastrar_departamento,
                departamentos.listar_departamentos,
                departamentos.atualizar_departamento,
                departamentos.excluir_departamento,
            )
        elif opcao == "3":
            _menu_crud(
                "Tipos de acesso",
                acessos.cadastrar_acesso,
                acessos.listar_acessos,
                acessos.atualizar_acesso,
                acessos.excluir_acesso,
            )
        elif opcao == "4":
            _menu_crud(
                "Emoções",
                emocoes.cadastrar_emocao,
                emocoes.listar_emocoes,
                emocoes.atualizar_emocao,
                emocoes.excluir_emocao,
            )
        elif opcao == "5":
            _menu_crud(
                "Categorias de emoção",
                categorias_emocao.cadastrar_categoria,
                categorias_emocao.listar_categorias,
                categorias_emocao.atualizar_categoria,
                categorias_emocao.excluir_categoria,
            )
        elif opcao == "6":
            _menu_crud(
                "Registros emocionais",
                registros_emocao.cadastrar_registro_emocao,
                registros_emocao.listar_registros_emocao,
                registros_emocao.atualizar_registro_emocao,
                registros_emocao.excluir_registro_emocao,
            )
        elif opcao == "7":
            _menu_crud(
                "Respostas de formulário",
                respostas_formulario.cadastrar_resposta_formulario,
                respostas_formulario.listar_respostas_formulario,
                respostas_formulario.atualizar_resposta_formulario,
                respostas_formulario.excluir_resposta_formulario,
            )
        elif opcao == "8":
            realizar_checkin_emocional()
        elif opcao == "9":
            _abrir_menu_consultas()
        else:
            print("Opção inválida.")
            pausar()


def _abrir_menu_consultas() -> None:
    """Importação tardia para evitar dependência circular."""
    from actors.consultas import menu_consultas

    menu_consultas()


def _menu_crud(
    titulo: str,
    cadastrar: MenuAction,
    listar: MenuAction,
    atualizar: MenuAction,
    excluir: MenuAction,
) -> None:
    """Renderiza um menu padrão contendo operações de CRUD."""
    while True:
        limpar_tela()
        print(f"=== {titulo} ===")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Atualizar")
        print("4. Excluir")
        print("0. Voltar")
        entrada = input("\nEscolha: ").strip()
        if deseja_voltar(entrada):
            break
        opcao = entrada
        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            excluir()
        else:
            print("Opção inválida.")
            pausar()


if __name__ == "__main__":  # pragma: no cover
    main()
