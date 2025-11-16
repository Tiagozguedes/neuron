"""CRUD simplificado para T_NRON_USUARIO."""

from __future__ import annotations

from datetime import date, datetime

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import limpar_tela, pausar, solicitar_confirmacao

TABELA = "T_NRON_USUARIO"


def _parse_data(valor: str) -> date:
    # Converte string no formato YYYY-MM-DD para objeto date.
    return datetime.strptime(valor, "%Y-%m-%d").date()


def cadastrar_usuario() -> None:
    # Responsável por cadastrar um colaborador/gestor informando acessos e departamento.
    try:
        limpar_tela()
        print("--- Cadastro de Usuário ---")
        usuario_id = int(input("ID do usuário: ").strip())
        if registro_existe(TABELA, "ID_USUARIO", usuario_id):
            print("ID já cadastrado.")
            return
        nome = input("Nome completo: ").strip().title()
        email = input("E-mail corporativo: ").strip().lower()
        senha = input("Senha (hash): ").strip()
        status = input("Status (A/I): ").strip().upper()[:1] or "A"
        data_input = input("Data de cadastro (YYYY-MM-DD) [hoje]: ").strip()
        data_cadastro = _parse_data(data_input) if data_input else date.today()
        id_acesso = int(input("ID do tipo de acesso: ").strip())
        if not registro_existe("T_NRON_ACESSO", "ID_ACESSO", id_acesso):
            print("Tipo de acesso inexistente.")
            return
        id_depto = int(input("ID do departamento: ").strip())
        if not registro_existe("T_NRON_DEPARTAMENTO", "ID_DEPARTAMENTO", id_depto):
            print("Departamento inexistente.")
            return
        run_execute(
            """
            INSERT INTO T_NRON_USUARIO (
                ID_USUARIO, NOME, EM_USUARIO, SEN_HASH_USUARIO,
                STT_USUARIO, DT_CADASTRO, ID_ACESSO, ID_DEPARTAMENTO
            ) VALUES (
                :id, :nome, :email, :senha,
                :status, :data_cadastro, :id_acesso, :id_depto
            )
            """,
            {
                "id": usuario_id,
                "nome": nome,
                "email": email,
                "senha": senha,
                "status": status,
                "data_cadastro": data_cadastro,
                "id_acesso": id_acesso,
                "id_depto": id_depto,
            },
        )
        print("Usuário cadastrado!")
    except Exception as exc:
        print(f"Erro ao cadastrar usuário: {exc}")
    finally:
        pausar()


def listar_usuarios() -> None:
    # Lista todos os usuários ordenados por nome para consulta rápida.
    try:
        limpar_tela()
        print("--- Usuários ---")
        linhas = run_query(
            """
            SELECT u.ID_USUARIO,
                   u.NOME,
                   u.EM_USUARIO,
                   u.STT_USUARIO,
                   TO_CHAR(u.DT_CADASTRO, 'YYYY-MM-DD') AS DT_CADASTRO,
                   u.ID_ACESSO,
                   u.ID_DEPARTAMENTO
              FROM T_NRON_USUARIO u
             ORDER BY u.NOME
            """,
            {},
        )
        if not linhas:
            print("Nenhum usuário cadastrado.")
            return
        for linha in linhas:
            print(
                f"{linha['id_usuario']:>3} | {linha['nome']:<25} | {linha['em_usuario']:<25} | "
                f"Status: {linha['stt_usuario']} | Cadastro: {linha['dt_cadastro']}"
            )
    except Exception as exc:
        print(f"Erro ao listar usuários: {exc}")
    finally:
        pausar()


def atualizar_usuario() -> None:
    # Permite alterar status, perfis e senha de um usuário existente.
    try:
        limpar_tela()
        print("--- Atualizar Usuário ---")
        usuario_id = int(input("ID do usuário: ").strip())
        usuario = buscar_por_id(TABELA, "ID_USUARIO", usuario_id)
        if not usuario:
            print("Usuário não encontrado.")
            return
        novo_nome = input(f"Nome atual ({usuario['nome']}): ").strip() or usuario["nome"]
        novo_status = input(f"Status atual ({usuario['stt_usuario']}): ").strip() or usuario["stt_usuario"]
        novo_acesso = input(f"ID acesso atual ({usuario['id_acesso']}): ").strip() or usuario["id_acesso"]
        novo_depto = input(f"ID depto atual ({usuario['id_departamento']}): ").strip() or usuario["id_departamento"]
        nova_senha = input("Nova senha (hash) [Enter para manter]: ").strip() or usuario["sen_hash_usuario"]
        run_execute(
            """
            UPDATE T_NRON_USUARIO
               SET NOME             = :nome,
                   STT_USUARIO      = :status,
                   ID_ACESSO        = :id_acesso,
                   ID_DEPARTAMENTO  = :id_depto,
                   SEN_HASH_USUARIO = :senha
             WHERE ID_USUARIO       = :id
            """,
            {
                "nome": novo_nome,
                "status": novo_status,
                "id_acesso": int(novo_acesso),
                "id_depto": int(novo_depto),
                "senha": nova_senha,
                "id": usuario_id,
            },
        )
        print("Usuário atualizado.")
    except Exception as exc:
        print(f"Erro ao atualizar usuário: {exc}")
    finally:
        pausar()


def excluir_usuario() -> None:
    # Remove usuário específico após a confirmação de exclusão.
    try:
        limpar_tela()
        print("--- Excluir Usuário ---")
        usuario_id = int(input("ID do usuário: ").strip())
        if not buscar_por_id(TABELA, "ID_USUARIO", usuario_id):
            print("Usuário não encontrado.")
            return
        if not solicitar_confirmacao("Confirma exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_USUARIO WHERE ID_USUARIO = :id", {"id": usuario_id})
        if linhas:
            print("Usuário excluído.")
        else:
            print("Nenhum registro removido.")
    except Exception as exc:
        print(f"Erro ao excluir usuário: {exc}")
    finally:
        pausar()
