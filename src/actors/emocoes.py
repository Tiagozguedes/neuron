"""CRUD para T_NRON_EMOCAO."""

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

TABELA = "T_NRON_EMOCAO"


def cadastrar_emocao() -> None:
    # Coleta dados da emoção (nome/cor/categoria) e insere no Oracle.
    try:
        limpar_tela()
        print("--- Cadastro de Emoção ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
        emocao_id = solicitar_inteiro("ID da emoção")
        if registro_existe(TABELA, "ID_EMOCAO", emocao_id):
            print("ID já cadastrado.")
            return
        nome = solicitar_texto("Nome da emoção").capitalize()
        cor = solicitar_texto("Cor HEX (#RRGGBB)").upper()
        categoria_id = solicitar_inteiro("ID da categoria")
        run_execute(
            """
            INSERT INTO T_NRON_EMOCAO (ID_EMOCAO, NM_EMOCAO, COR_EMOCAO, ID_CATG_EMOCAO)
            VALUES (:id, :nome, :cor, :categoria)
            """,
            {"id": emocao_id, "nome": nome, "cor": cor, "categoria": categoria_id},
        )
        print("Emoção cadastrada.")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao cadastrar emoção: {exc}")
    finally:
        pausar()


def listar_emocoes() -> None:
    # Lista todas as emoções cadastradas com ordenação alfabética.
    try:
        limpar_tela()
        print("--- Emoções ---")
        linhas = run_query(
            "SELECT ID_EMOCAO, NM_EMOCAO, COR_EMOCAO, ID_CATG_EMOCAO FROM T_NRON_EMOCAO ORDER BY NM_EMOCAO",
            {},
        )
        if not linhas:
            print("Nenhuma emoção cadastrada.")
            return
        for linha in linhas:
            print(
                f"{linha['id_emocao']:>3} | {linha['nm_emocao']:<15} | Cor: {linha['cor_emocao']:<8} | "
                f"Categoria: {linha['id_catg_emocao']}"
            )
    except Exception as exc:
        print(f"Erro ao listar emoções: {exc}")
    finally:
        pausar()


def atualizar_emocao() -> None:
    # Permite editar atributos da emoção individualmente.
    try:
        limpar_tela()
        print("--- Atualizar Emoção ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
        emocao_id = solicitar_inteiro("ID da emoção")
        emocao = buscar_por_id(TABELA, "ID_EMOCAO", emocao_id)
        if not emocao:
            print("Emoção não encontrada.")
            return
        novo_nome = solicitar_texto(
            f"Nome atual ({emocao['nm_emocao']}) [Enter para manter]", padrao=emocao["nm_emocao"], obrigatorio=False
        )
        nova_cor = solicitar_texto(
            f"Cor atual ({emocao['cor_emocao']}) [Enter para manter]", padrao=emocao["cor_emocao"], obrigatorio=False
        ).upper()
        nova_cat = solicitar_inteiro(
            f"Categoria atual ({emocao['id_catg_emocao']}) [Enter para manter]",
            padrao=int(emocao["id_catg_emocao"]),
        )
        run_execute(
            """
            UPDATE T_NRON_EMOCAO
               SET NM_EMOCAO    = :nome,
                   COR_EMOCAO   = :cor,
                   ID_CATG_EMOCAO = :categoria
             WHERE ID_EMOCAO    = :id
            """,
            {"nome": novo_nome, "cor": nova_cor, "categoria": int(nova_cat), "id": emocao_id},
        )
        print("Emoção atualizada.")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao atualizar emoção: {exc}")
    finally:
        pausar()


def excluir_emocao() -> None:
    # Remove uma emoção já existente após confirmação do usuário.
    try:
        limpar_tela()
        print("--- Excluir Emoção ---")
        print("Digite 'voltar' a qualquer momento para cancelar.\n")
        emocao_id = solicitar_inteiro("ID da emoção")
        if not buscar_por_id(TABELA, "ID_EMOCAO", emocao_id):
            print("Emoção não encontrada.")
            return
        if not solicitar_confirmacao("Confirmar exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_EMOCAO WHERE ID_EMOCAO = :id", {"id": emocao_id})
        if linhas:
            print("Emoção excluída.")
        else:
            print("Nenhuma linha afetada.")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao excluir emoção: {exc}")
    finally:
        pausar()
