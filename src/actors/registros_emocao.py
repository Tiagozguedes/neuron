"""CRUD para T_NRON_REGIST_EMOCAO."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import fluxo_cli, solicitar_confirmacao, solicitar_decimal, solicitar_inteiro, solicitar_texto

TABELA = "T_NRON_REGIST_EMOCAO"


def cadastrar_registro_emocao() -> None:
    """Cadastro manual de registro emocional: coleta intensidade, descrição, data e FK de emoção."""
    with fluxo_cli("--- Cadastro de Registro de Emoção ---", "Erro ao cadastrar registro"):
        registro_id = solicitar_inteiro("ID do registro")
        if registro_existe(TABELA, "ID_REGIST_EMOCAO", registro_id):
            print("ID já cadastrado.")
            return
        intensidade = solicitar_decimal("Intensidade (0-100)")
        descricao = solicitar_texto("Descrição")
        data_input = solicitar_texto("Data (YYYY-MM-DD)")
        data_registro = datetime.strptime(data_input, "%Y-%m-%d")
        id_emocao = solicitar_inteiro("ID da emoção principal")
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


def listar_registros_emocao() -> None:
    """Lista registros emocionais em ordem cronológica decrescente."""
    with fluxo_cli("--- Registros de Emoção ---", "Erro ao listar registros", mostrar_instrucao=False):
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


def atualizar_registro_emocao() -> None:
    """Permite editar intensidade, descrição, data e emoção vinculada de um registro existente."""
    with fluxo_cli("--- Atualizar Registro de Emoção ---", "Erro ao atualizar registro"):
        registro_id = solicitar_inteiro("ID do registro")
        registro = buscar_por_id(TABELA, "ID_REGIST_EMOCAO", registro_id)
        if not registro:
            print("Registro não encontrado.")
            return
        intensidade = solicitar_decimal(
            f"Intensidade atual ({registro['int_regist_emocao']}) [Enter para manter | intervalo 0-100]",
            padrao=Decimal(str(registro["int_regist_emocao"])),
        )
        descricao = solicitar_texto(
            f"Descrição atual ({registro['ds_regist_emocao']}) [Enter para manter]",
            padrao=registro["ds_regist_emocao"],
            obrigatorio=False,
        )
        data_atual = registro["dt_regist_emocao"]
        if hasattr(data_atual, "strftime"):
            data_atual = data_atual.strftime("%Y-%m-%d")
        data_input = solicitar_texto(
            f"Data atual ({data_atual}) [Enter para manter]", padrao=str(data_atual), obrigatorio=False
        )
        id_emocao = solicitar_inteiro(
            f"ID emoção atual ({registro['id_emocao']}) [Enter para manter]", padrao=int(registro["id_emocao"])
        )
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


def excluir_registro_emocao() -> None:
    """Exclui um registro emocional após validação e confirmação do usuário."""
    with fluxo_cli("--- Excluir Registro de Emoção ---", "Erro ao excluir registro"):
        registro_id = solicitar_inteiro("ID do registro")
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
