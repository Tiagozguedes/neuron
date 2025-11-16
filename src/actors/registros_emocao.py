"""CRUD para T_NRON_REGIST_EMOCAO."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import limpar_tela, pausar, solicitar_confirmacao

TABELA = "T_NRON_REGIST_EMOCAO"


def _parse_decimal(valor: str) -> Decimal:
    # Converte valores informados na CLI (com vírgula/ponto) para Decimal.
    return Decimal(valor.replace(",", "."))


def cadastrar_registro_emocao() -> None:
    # Fluxo de inserção manual de registros (usado por administradores).
    try:
        limpar_tela()
        print("--- Cadastro de Registro de Emoção ---")
        registro_id = int(input("ID do registro: ").strip())
        if registro_existe(TABELA, "ID_REGIST_EMOCAO", registro_id):
            print("ID já cadastrado.")
            return
        intensidade = _parse_decimal(input("Intensidade (0-10): ").strip())
        descricao = input("Descrição: ").strip()
        data_input = input("Data (YYYY-MM-DD): ").strip()
        data_registro = datetime.strptime(data_input, "%Y-%m-%d")
        id_emocao = int(input("ID da emoção principal: ").strip())
        if not registro_existe("T_NRON_EMOCAO", "ID_EMOCAO", id_emocao):
            print("Emoção inexistente.")
            return
        run_execute(
            """
            INSERT INTO T_NRON_REGIST_EMOCAO (
                ID_REGIST_EMOCAO, INT_REGIST_EMOCAO, DS_REGIST_EMOCAO,
                DT_REGIST_EMOCAO, ID_EMOCAO
            ) VALUES (
                :id, :intensidade, :descricao,
                :data_registro, :id_emocao
            )
            """,
            {
                "id": registro_id,
                "intensidade": intensidade,
                "descricao": descricao,
                "data_registro": data_registro,
                "id_emocao": id_emocao,
            },
        )
        print("Registro de emoção cadastrado.")
    except Exception as exc:
        print(f"Erro ao cadastrar registro: {exc}")
    finally:
        pausar()


def listar_registros_emocao() -> None:
    # Mostra o histórico em ordem cronológica inversa.
    try:
        limpar_tela()
        print("--- Registros de Emoção ---")
        linhas = run_query(
            """
            SELECT ID_REGIST_EMOCAO,
                   INT_REGIST_EMOCAO,
                   DS_REGIST_EMOCAO,
                   TO_CHAR(DT_REGIST_EMOCAO, 'YYYY-MM-DD') AS DT_REGIST_EMOCAO,
                   ID_EMOCAO
              FROM T_NRON_REGIST_EMOCAO
             ORDER BY DT_REGIST_EMOCAO DESC
            """,
            {},
        )
        if not linhas:
            print("Nenhum registro encontrado.")
            return
        for linha in linhas:
            print(
                f"{linha['id_regist_emocao']:>3} | Intensidade: {linha['int_regist_emocao']} | "
                f"Data: {linha['dt_regist_emocao']} | Emoção: {linha['id_emocao']}"
            )
    except Exception as exc:
        print(f"Erro ao listar registros: {exc}")
    finally:
        pausar()


def atualizar_registro_emocao() -> None:
    # Permite ajustar detalhes (intensidade, descrição, data, emoção).
    try:
        limpar_tela()
        print("--- Atualizar Registro de Emoção ---")
        registro_id = int(input("ID do registro: ").strip())
        registro = buscar_por_id(TABELA, "ID_REGIST_EMOCAO", registro_id)
        if not registro:
            print("Registro não encontrado.")
            return
        intensidade = input(f"Intensidade atual ({registro['int_regist_emocao']}): ").strip() or registro["int_regist_emocao"]
        descricao = input(f"Descrição atual ({registro['ds_regist_emocao']}): ").strip() or registro["ds_regist_emocao"]
        data_atual = registro["dt_regist_emocao"]
        if hasattr(data_atual, "strftime"):
            data_atual = data_atual.strftime("%Y-%m-%d")
        data_input = input(f"Data atual ({data_atual}): ").strip() or data_atual
        id_emocao = input(f"ID emoção atual ({registro['id_emocao']}): ").strip() or registro["id_emocao"]
        run_execute(
            """
            UPDATE T_NRON_REGIST_EMOCAO
               SET INT_REGIST_EMOCAO = :intensidade,
                   DS_REGIST_EMOCAO  = :descricao,
                   DT_REGIST_EMOCAO  = TO_DATE(:data_registro, 'YYYY-MM-DD'),
                   ID_EMOCAO         = :id_emocao
             WHERE ID_REGIST_EMOCAO  = :id
            """,
            {
                "intensidade": intensidade,
                "descricao": descricao,
                "data_registro": data_input,
                "id_emocao": int(id_emocao),
                "id": registro_id,
            },
        )
        print("Registro atualizado.")
    except Exception as exc:
        print(f"Erro ao atualizar registro: {exc}")
    finally:
        pausar()


def excluir_registro_emocao() -> None:
    # Exclui o registro solicitado após confirmação (limpeza de dados).
    try:
        limpar_tela()
        print("--- Excluir Registro de Emoção ---")
        registro_id = int(input("ID do registro: ").strip())
        if not buscar_por_id(TABELA, "ID_REGIST_EMOCAO", registro_id):
            print("Registro não encontrado.")
            return
        if not solicitar_confirmacao("Confirmar exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_REGIST_EMOCAO WHERE ID_REGIST_EMOCAO = :id", {"id": registro_id})
        if linhas:
            print("Registro excluído.")
        else:
            print("Nenhuma linha afetada.")
    except Exception as exc:
        print(f"Erro ao excluir registro: {exc}")
    finally:
        pausar()
