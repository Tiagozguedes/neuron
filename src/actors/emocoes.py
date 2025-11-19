"""CRUD para T_NRON_EMOCAO."""

from __future__ import annotations

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import fluxo_cli, solicitar_confirmacao, solicitar_inteiro, solicitar_texto

TABELA = "T_NRON_EMOCAO"


def _mostrar_categorias_disponiveis() -> None:
    linhas = run_query(
        "SELECT ID_CATG_EMOCAO, NOME_CATG_EMOCAO FROM T_NRON_CATG_EMOCAO ORDER BY NOME_CATG_EMOCAO",
        {},
    )
    if not linhas:
        print("Nenhuma categoria cadastrada. Cadastre em 'Categorias de emoção' antes de prosseguir.")
        return
    print("\nCategorias disponíveis:")
    for linha in linhas:
        print(f"  {linha['id_catg_emocao']:>3} | {linha['nome_catg_emocao']}")


def cadastrar_emocao() -> None:
    # Coleta dados da emoção (nome/cor/categoria) e insere no Oracle.
    with fluxo_cli("--- Cadastro de Emoção ---", "Erro ao cadastrar emoção"):
        emocao_id = solicitar_inteiro("ID da emoção")
        if registro_existe(TABELA, "ID_EMOCAO", emocao_id):
            print("ID já cadastrado.")
            return
        nome = solicitar_texto("Nome da emoção").capitalize()
        cor = solicitar_texto("Cor HEX (#RRGGBB)").upper()
        _mostrar_categorias_disponiveis()
        categoria_id = solicitar_inteiro("ID da categoria")
        if not registro_existe("T_NRON_CATG_EMOCAO", "ID_CATG_EMOCAO", categoria_id):
            print("Categoria inexistente. Cadastre primeiro em 'Categorias de emoção'.")
            return
        run_execute(
            """
            INSERT INTO T_NRON_EMOCAO (ID_EMOCAO, NM_EMOCAO, COR_EMOCAO, ID_CATG_EMOCAO)
            VALUES (:id, :nome, :cor, :categoria)
            """,
            {"id": emocao_id, "nome": nome, "cor": cor, "categoria": categoria_id},
        )
        print("Emoção cadastrada.")


def listar_emocoes() -> None:
    # Lista todas as emoções cadastradas com ordenação alfabética.
    with fluxo_cli("--- Emoções ---", "Erro ao listar emoções", mostrar_instrucao=False):
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


def atualizar_emocao() -> None:
    # Permite editar atributos da emoção individualmente.
    with fluxo_cli("--- Atualizar Emoção ---", "Erro ao atualizar emoção"):
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
        _mostrar_categorias_disponiveis()
        nova_cat = solicitar_inteiro(
            f"Categoria atual ({emocao['id_catg_emocao']}) [Enter para manter]",
            padrao=int(emocao["id_catg_emocao"]),
        )
        if not registro_existe("T_NRON_CATG_EMOCAO", "ID_CATG_EMOCAO", int(nova_cat)):
            print("Categoria inexistente.")
            return
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


def excluir_emocao() -> None:
    # Remove uma emoção já existente após confirmação do usuário.
    with fluxo_cli("--- Excluir Emoção ---", "Erro ao excluir emoção"):
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
