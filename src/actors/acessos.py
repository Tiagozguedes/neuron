"""CRUD simplificado para T_NRON_ACESSO."""

from __future__ import annotations

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import limpar_tela, pausar, solicitar_confirmacao

TABELA = "T_NRON_ACESSO"


def cadastrar_acesso() -> None:
    # Solicita dados no terminal e insere um novo tipo de acesso.
    """Cria um novo tipo de acesso."""
    try:
        limpar_tela()
        print("--- Cadastro de Tipo de Acesso ---")
        id_acesso = int(input("ID do acesso: ").strip())
        if registro_existe(TABELA, "ID_ACESSO", id_acesso):
            print("Erro: ID já cadastrado.")
            return
        tipo = input("Tipo (FUNCIONARIO/GESTOR/RH_CLEVEL): ").strip().upper()
        descricao = input("Descrição: ").strip()
        run_execute(
            """
            INSERT INTO T_NRON_ACESSO (ID_ACESSO, TP_ACESSO, DS_ACESSO)
            VALUES (:id, :tipo, :descricao)
            """,
            {"id": id_acesso, "tipo": tipo, "descricao": descricao},
        )
        print("Tipo de acesso cadastrado com sucesso!")
    except Exception as exc:
        print(f"Erro ao cadastrar tipo de acesso: {exc}")
    finally:
        pausar()


def listar_acessos() -> None:
    # Executa SELECT simples e imprime tabela formatada.
    """Lista todos os tipos de acesso."""
    try:
        limpar_tela()
        print("--- Tipos de Acesso ---")
        linhas = run_query(
            "SELECT ID_ACESSO, TP_ACESSO, DS_ACESSO FROM T_NRON_ACESSO ORDER BY ID_ACESSO",
            {},
        )
        if not linhas:
            print("Nenhum registro encontrado.")
            return
        for linha in linhas:
            print(f"{linha['id_acesso']:>3} | {linha['tp_acesso']:<15} | {linha['ds_acesso']}")
    except Exception as exc:
        print(f"Erro ao listar acessos: {exc}")
    finally:
        pausar()


def atualizar_acesso() -> None:
    # Recupera registro existente e permite alterar tipo/descrição.
    """Atualiza descrição e tipo."""
    try:
        limpar_tela()
        print("--- Atualizar Tipo de Acesso ---")
        id_acesso = int(input("ID do acesso: ").strip())
        acesso = buscar_por_id(TABELA, "ID_ACESSO", id_acesso)
        if not acesso:
            print("ID não encontrado.")
            return
        novo_tipo = input(f"Tipo atual ({acesso['tp_acesso']}): ").strip() or acesso["tp_acesso"]
        nova_desc = input(f"Descrição atual ({acesso['ds_acesso']}): ").strip() or acesso["ds_acesso"]
        run_execute(
            """
            UPDATE T_NRON_ACESSO
               SET TP_ACESSO = :tipo,
                   DS_ACESSO = :descricao
             WHERE ID_ACESSO = :id
            """,
            {"tipo": novo_tipo, "descricao": nova_desc, "id": id_acesso},
        )
        print("Registro atualizado.")
    except Exception as exc:
        print(f"Erro ao atualizar: {exc}")
    finally:
        pausar()


def excluir_acesso() -> None:
    # Pergunta o ID e remove o registro após confirmação do usuário.
    """Remove um tipo de acesso."""
    try:
        limpar_tela()
        print("--- Excluir Tipo de Acesso ---")
        id_acesso = int(input("ID do acesso: ").strip())
        if not buscar_por_id(TABELA, "ID_ACESSO", id_acesso):
            print("ID não encontrado.")
            return
        if not solicitar_confirmacao("Confirma exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_ACESSO WHERE ID_ACESSO = :id", {"id": id_acesso})
        if linhas:
            print("Registro excluído.")
        else:
            print("Nenhum registro removido.")
    except Exception as exc:
        print(f"Erro ao excluir: {exc}")
    finally:
        pausar()
