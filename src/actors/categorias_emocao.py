"""CRUD para T_NRON_CATG_EMOCAO."""

from __future__ import annotations

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import fluxo_cli, solicitar_confirmacao, solicitar_inteiro, solicitar_texto

TABELA = "T_NRON_CATG_EMOCAO"


def cadastrar_categoria() -> None:
    """Coleta ID/nome, valida duplicidade e insere a categoria de emoção."""
    with fluxo_cli("--- Cadastro de Categoria de Emoção ---", "Erro ao cadastrar categoria"):
        categoria_id = solicitar_inteiro("ID da categoria")
        if registro_existe(TABELA, "ID_CATG_EMOCAO", categoria_id):
            print("ID já cadastrado.")
            return
        nome = solicitar_texto("Nome (POSITIVA/NEGATIVA/NEUTRA)").upper()
        run_execute(
            """
            INSERT INTO T_NRON_CATG_EMOCAO (ID_CATG_EMOCAO, NOME_CATG_EMOCAO)
            VALUES (:id, :nome)
            """,
            {"id": categoria_id, "nome": nome},
        )
        print("Categoria cadastrada.")


def listar_categorias() -> None:
    """Lista categorias de emoção para referência em cadastros e edições."""
    with fluxo_cli("--- Categorias de Emoção ---", "Erro ao listar categorias", mostrar_instrucao=False):
        linhas = run_query(
            "SELECT ID_CATG_EMOCAO, NOME_CATG_EMOCAO FROM T_NRON_CATG_EMOCAO ORDER BY ID_CATG_EMOCAO",
            {},
        )
        if not linhas:
            print("Nenhuma categoria cadastrada.")
            return
        for linha in linhas:
            print(f"{linha['id_catg_emocao']:>3} | {linha['nome_catg_emocao']:<10}")


def atualizar_categoria() -> None:
    """Permite renomear uma categoria existente mantendo o ID."""
    with fluxo_cli("--- Atualizar Categoria ---", "Erro ao atualizar categoria"):
        categoria_id = solicitar_inteiro("ID da categoria")
        categoria = buscar_por_id(TABELA, "ID_CATG_EMOCAO", categoria_id)
        if not categoria:
            print("Categoria não encontrada.")
            return
        novo_nome = solicitar_texto(
            f"Nome atual ({categoria['nome_catg_emocao']}) [Enter para manter]",
            padrao=categoria["nome_catg_emocao"],
            obrigatorio=False,
        ).upper()
        run_execute(
            """
            UPDATE T_NRON_CATG_EMOCAO
               SET NOME_CATG_EMOCAO = :nome
             WHERE ID_CATG_EMOCAO   = :id
            """,
            {"nome": novo_nome, "id": categoria_id},
        )
        print("Categoria atualizada.")


def excluir_categoria() -> None:
    """Exclui uma categoria após validar existência e confirmar com o usuário."""
    with fluxo_cli("--- Excluir Categoria ---", "Erro ao excluir categoria"):
        categoria_id = solicitar_inteiro("ID da categoria")
        if not buscar_por_id(TABELA, "ID_CATG_EMOCAO", categoria_id):
            print("Categoria não encontrada.")
            return
        if not solicitar_confirmacao("Confirmar exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_CATG_EMOCAO WHERE ID_CATG_EMOCAO = :id", {"id": categoria_id})
        if linhas:
            print("Categoria excluída.")
        else:
            print("Nenhuma linha afetada.")
