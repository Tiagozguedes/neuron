"""CRUD para departamentos."""

from __future__ import annotations

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import (
    OperacaoCancelada,
    limpar_tela,
    pausar,
    solicitar_confirmacao,
    solicitar_inteiro,
    solicitar_texto,
)

TABELA = "T_NRON_DEPARTAMENTO"


def cadastrar_departamento() -> None:
    # Recolhe nome/descrição e realiza INSERT na tabela de departamentos.
    try:
        limpar_tela()
        print("--- Cadastro de Departamento ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
        depto_id = solicitar_inteiro("ID do departamento")
        if registro_existe(TABELA, "ID_DEPARTAMENTO", depto_id):
            print("Erro: ID já cadastrado.")
            return
        nome = solicitar_texto("Nome").title()
        descricao = solicitar_texto("Descrição")
        run_execute(
            """
            INSERT INTO T_NRON_DEPARTAMENTO (ID_DEPARTAMENTO, NOME_DEPARTAMENTO, DS_DEPARTAMENTO)
            VALUES (:id, :nome, :descricao)
            """,
            {"id": depto_id, "nome": nome, "descricao": descricao},
        )
        print("Departamento cadastrado!")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao cadastrar departamento: {exc}")
    finally:
        pausar()


def listar_departamentos() -> None:
    # Exibe a tabela ordenada por nome para facilitar consulta.
    try:
        limpar_tela()
        print("--- Departamentos ---")
        linhas = run_query(
            "SELECT ID_DEPARTAMENTO, NOME_DEPARTAMENTO, DS_DEPARTAMENTO "
            "FROM T_NRON_DEPARTAMENTO ORDER BY NOME_DEPARTAMENTO",
            {},
        )
        if not linhas:
            print("Nenhum departamento cadastrado.")
            return
        for linha in linhas:
            print(f"{linha['id_departamento']:>3} | {linha['nome_departamento']:<25} | {linha['ds_departamento']}")
    except Exception as exc:
        print(f"Erro ao listar departamentos: {exc}")
    finally:
        pausar()


def atualizar_departamento() -> None:
    # Permite editar nome/descrição mantendo o restante do registro.
    try:
        limpar_tela()
        print("--- Atualizar Departamento ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
        depto_id = solicitar_inteiro("ID do departamento")
        depto = buscar_por_id(TABELA, "ID_DEPARTAMENTO", depto_id)
        if not depto:
            print("Departamento não encontrado.")
            return
        novo_nome = solicitar_texto(
            f"Nome atual ({depto['nome_departamento']}) [Enter para manter]",
            padrao=depto["nome_departamento"],
            obrigatorio=False,
        ).title()
        nova_desc = solicitar_texto(
            f"Descrição atual ({depto['ds_departamento']}) [Enter para manter]",
            padrao=depto["ds_departamento"],
            obrigatorio=False,
        )
        run_execute(
            """
            UPDATE T_NRON_DEPARTAMENTO
               SET NOME_DEPARTAMENTO = :nome,
                   DS_DEPARTAMENTO   = :descricao
             WHERE ID_DEPARTAMENTO   = :id
            """,
            {"nome": novo_nome, "descricao": nova_desc, "id": depto_id},
        )
        print("Departamento atualizado.")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao atualizar departamento: {exc}")
    finally:
        pausar()


def excluir_departamento() -> None:
    # Remove departamento após checar existência e confirmar operação.
    try:
        limpar_tela()
        print("--- Excluir Departamento ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
        depto_id = solicitar_inteiro("ID do departamento")
        if not buscar_por_id(TABELA, "ID_DEPARTAMENTO", depto_id):
            print("Departamento não encontrado.")
            return
        if not solicitar_confirmacao("Confirmar exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_DEPARTAMENTO WHERE ID_DEPARTAMENTO = :id", {"id": depto_id})
        if linhas:
            print("Departamento excluído.")
        else:
            print("Nenhuma linha afetada.")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao excluir departamento: {exc}")
    finally:
        pausar()
