"""CRUD simplificado para T_NRON_USUARIO."""

from __future__ import annotations

from datetime import date, datetime

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import fluxo_cli, solicitar_confirmacao, solicitar_inteiro, solicitar_texto

TABELA = "T_NRON_USUARIO"
STATUS_LABELS = {"A": "Ativo", "I": "Inativo"}


def _mostrar_opcoes_acesso() -> None:
    linhas = run_query(
        "SELECT ID_ACESSO, TP_ACESSO, DS_ACESSO FROM T_NRON_ACESSO ORDER BY ID_ACESSO",
        {},
    )
    if not linhas:
        print("Nenhum tipo de acesso cadastrado. Use o menu 3 para criar antes de prosseguir.")
        return
    print("\nTipos de acesso disponíveis:")
    for linha in linhas:
        print(f"  {linha['id_acesso']:>3} | {linha['tp_acesso']:<15} | {linha['ds_acesso']}")


def _mostrar_opcoes_departamento() -> None:
    linhas = run_query(
        "SELECT ID_DEPARTAMENTO, NOME_DEPARTAMENTO FROM T_NRON_DEPARTAMENTO ORDER BY NOME_DEPARTAMENTO",
        {},
    )
    if not linhas:
        print("Nenhum departamento cadastrado. Use o menu 2 para criar antes de prosseguir.")
        return
    print("\nDepartamentos disponíveis:")
    for linha in linhas:
        print(f"  {linha['id_departamento']:>3} | {linha['nome_departamento']}")


def _parse_data(valor: str) -> date:
    # Converte string no formato DDMMYYYY para objeto date.
    valor = valor.strip()
    if len(valor) != 8 or not valor.isdigit():
        raise ValueError("Informe a data no formato DDMMYYYY (ex.: 01012024).")
    dia = int(valor[0:2])
    mes = int(valor[2:4])
    ano = int(valor[4:8])
    return datetime(ano, mes, dia).date()


def _solicitar_status(mensagem: str, padrao: str = "A") -> str:
    """Solicita status e valida a entrada para evitar abreviações confusas."""
    while True:
        resposta = solicitar_texto(mensagem, padrao=padrao, obrigatorio=False).strip().upper()
        if resposta in STATUS_LABELS:
            return resposta
        print("Por favor, informe 'A' para Ativo ou 'I' para Inativo.")


def cadastrar_usuario() -> None:
    # Responsável por cadastrar um colaborador/gestor informando acessos e departamento.
    with fluxo_cli("--- Cadastro de Usuário ---", "Erro ao cadastrar usuário"):
        usuario_id = solicitar_inteiro("ID do usuário")
        if registro_existe(TABELA, "ID_USUARIO", usuario_id):
            print("ID já cadastrado.")
            return
        nome = solicitar_texto("Nome completo do colaborador").title()
        email = solicitar_texto("E-mail corporativo (login)").lower()
        senha = solicitar_texto("Senha (hash) a ser armazenada")
        status = _solicitar_status("Situação do usuário [A=Ativo, I=Inativo] (padrão A)")
        data_input = solicitar_texto("Data de cadastro (formato DDMMYYYY) [hoje]", obrigatorio=False)
        data_cadastro = _parse_data(data_input) if data_input else date.today()
        _mostrar_opcoes_acesso()
        id_acesso = solicitar_inteiro("ID do tipo de acesso listado acima")
        if not registro_existe("T_NRON_ACESSO", "ID_ACESSO", id_acesso):
            print("Tipo de acesso inexistente.")
            return
        _mostrar_opcoes_departamento()
        id_depto = solicitar_inteiro("ID do departamento listado acima")
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


def listar_usuarios() -> None:
    # Lista todos os usuários ordenados por nome para consulta rápida.
    with fluxo_cli("--- Usuários ---", "Erro ao listar usuários", mostrar_instrucao=False):
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
            status_legivel = STATUS_LABELS.get(linha["stt_usuario"], linha["stt_usuario"])
            print(
                f"{linha['id_usuario']:>3} | {linha['nome']:<25} | {linha['em_usuario']:<25} | "
                f"Status: {status_legivel} | Cadastro: {linha['dt_cadastro']}"
            )


def atualizar_usuario() -> None:
    # Permite alterar status, perfis e senha de um usuário existente.
    with fluxo_cli("--- Atualizar Usuário ---", "Erro ao atualizar usuário"):
        usuario_id = solicitar_inteiro("ID do usuário")
        usuario = buscar_por_id(TABELA, "ID_USUARIO", usuario_id)
        if not usuario:
            print("Usuário não encontrado.")
            return
        novo_nome = solicitar_texto(
            f"Nome atual ({usuario['nome']}) [Enter para manter]", padrao=usuario["nome"], obrigatorio=False
        )
        status_msg = (
            f"Situação atual ({STATUS_LABELS.get(usuario['stt_usuario'], usuario['stt_usuario'])}) "
            "[A=Ativo, I=Inativo]: "
        )
        novo_status = _solicitar_status(status_msg, usuario["stt_usuario"])
        print("\nReferência de tipos de acesso cadastrados:")
        _mostrar_opcoes_acesso()
        novo_acesso = solicitar_inteiro(
            f"ID de acesso atual ({usuario['id_acesso']}) [Enter para manter]", padrao=int(usuario["id_acesso"])
        )
        print("\nReferência de departamentos cadastrados:")
        _mostrar_opcoes_departamento()
        novo_depto = solicitar_inteiro(
            f"ID do departamento atual ({usuario['id_departamento']}) [Enter para manter]",
            padrao=int(usuario["id_departamento"]),
        )
        nova_senha = solicitar_texto(
            "Nova senha (hash) [Enter para manter a atual]", padrao=usuario["sen_hash_usuario"], obrigatorio=False
        )
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


def excluir_usuario() -> None:
    # Remove usuário específico após a confirmação de exclusão.
    with fluxo_cli("--- Excluir Usuário ---", "Erro ao excluir usuário"):
        usuario_id = solicitar_inteiro("ID do usuário")
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
