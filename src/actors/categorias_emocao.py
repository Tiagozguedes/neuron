"""CRUD para T_NRON_CATG_EMOCAO."""

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

TABELA = "T_NRON_CATG_EMOCAO"


def cadastrar_categoria() -> None:
    # Responsável por coletar ID/nome e inserir a categoria.
    try:
        limpar_tela()
        print("--- Cadastro de Categoria de Emoção ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
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
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao cadastrar categoria: {exc}")
    finally:
        pausar()


def listar_categorias() -> None:
    # Lista todas as categorias disponíveis, usado para referência em outras telas.
    try:
        limpar_tela()
        print("--- Categorias de Emoção ---")
        linhas = run_query(
            "SELECT ID_CATG_EMOCAO, NOME_CATG_EMOCAO FROM T_NRON_CATG_EMOCAO ORDER BY ID_CATG_EMOCAO",
            {},
        )
        if not linhas:
            print("Nenhuma categoria cadastrada.")
            return
        for linha in linhas:
            print(f"{linha['id_catg_emocao']:>3} | {linha['nome_catg_emocao']:<10}")
    except Exception as exc:
        print(f"Erro ao listar categorias: {exc}")
    finally:
        pausar()


def atualizar_categoria() -> None:
    # Permite renomear uma categoria após recuperar o registro corrente.
    try:
        limpar_tela()
        print("--- Atualizar Categoria ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
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
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao atualizar categoria: {exc}")
    finally:
        pausar()


def excluir_categoria() -> None:
    # Remove a categoria caso exista e o usuário confirme.
    try:
        limpar_tela()
        print("--- Excluir Categoria ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
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
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao excluir categoria: {exc}")
    finally:
        pausar()
