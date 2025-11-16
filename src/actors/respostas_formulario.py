"""CRUD para T_NRON_RESP_FORMULARIO."""

from __future__ import annotations

from decimal import Decimal

from connect.connect import run_execute, run_query
from db_utils import buscar_por_id, registro_existe
from utils import limpar_tela, pausar, solicitar_confirmacao

TABELA = "T_NRON_RESP_FORMULARIO"


def _decimal(valor: str) -> Decimal:
    # Normaliza entrada numérica (permite vírgula ou ponto) para Decimal.
    return Decimal(valor.replace(",", "."))


def cadastrar_resposta_formulario() -> None:
    # Coleta os indicadores retornados pela IA e grava em T_NRON_RESP_FORMULARIO.
    try:
        limpar_tela()
        print("--- Cadastro de Resposta de Formulário ---")
        resposta_id = int(input("ID da resposta: ").strip())
        if registro_existe(TABELA, "ID_RESPOSTA", resposta_id):
            print("ID já cadastrado.")
            return
        data_resposta = input("Data da resposta (YYYY-MM-DD): ").strip()
        motivacao = _decimal(input("Motivação (0-10): ").strip())
        felicidade = _decimal(input("Felicidade (0-10): ").strip())
        estresse = _decimal(input("Estresse (0-10): ").strip())
        observacao = input("Observações: ").strip()
        saude_mental = _decimal(input("Saúde mental (0-10): ").strip())
        probabilidade = _decimal(input("Confiança do modelo (0-100): ").strip())
        modelo_versao = input("Versão do modelo: ").strip()
        data_analise = input("Data da análise (YYYY-MM-DD): ").strip()
        id_usuario = int(input("ID do usuário: ").strip())
        if not registro_existe("T_NRON_USUARIO", "ID_USUARIO", id_usuario):
            print("Usuário não encontrado.")
            return
        id_registro = int(input("ID do registro de emoção: ").strip())
        if not registro_existe("T_NRON_REGIST_EMOCAO", "ID_REGIST_EMOCAO", id_registro):
            print("Registro de emoção inexistente.")
            return
        run_execute(
            """
            INSERT INTO T_NRON_RESP_FORMULARIO (
                ID_RESPOSTA, DT_RESPOSTA, MOT_RESPOSTA, FEL_RESPOSTA,
                EST_RESPOSTA, OBS_RESPOSTA, SAU_MEN_RESPOSTA,
                PROB_RESPOSTA, MOD_VER_RESPOSTA, DT_ANL_RESPOSTA,
                ID_USUARIO, ID_REGIST_EMOCAO
            ) VALUES (
                :id, TO_DATE(:dt_resposta, 'YYYY-MM-DD'), :motivacao, :felicidade,
                :estresse, :observacao, :saude_mental,
                :probabilidade, :modelo_versao, TO_DATE(:dt_analise, 'YYYY-MM-DD'),
                :id_usuario, :id_registro
            )
            """,
            {
                "id": resposta_id,
                "dt_resposta": data_resposta,
                "motivacao": motivacao,
                "felicidade": felicidade,
                "estresse": estresse,
                "observacao": observacao,
                "saude_mental": saude_mental,
                "probabilidade": probabilidade,
                "modelo_versao": modelo_versao,
                "dt_analise": data_analise,
                "id_usuario": id_usuario,
                "id_registro": id_registro,
            },
        )
        print("Resposta cadastrada.")
    except Exception as exc:
        print(f"Erro ao cadastrar resposta: {exc}")
    finally:
        pausar()


def listar_respostas_formulario() -> None:
    # Consulta as respostas ordenadas pela data mais recente para auditoria.
    try:
        limpar_tela()
        print("--- Respostas de Formulário ---")
        linhas = run_query(
            """
            SELECT ID_RESPOSTA,
                   TO_CHAR(DT_RESPOSTA, 'YYYY-MM-DD') AS DT_RESPOSTA,
                   MOT_RESPOSTA,
                   FEL_RESPOSTA,
                   EST_RESPOSTA,
                   SAU_MEN_RESPOSTA,
                   PROB_RESPOSTA,
                   MOD_VER_RESPOSTA,
                   TO_CHAR(DT_ANL_RESPOSTA, 'YYYY-MM-DD') AS DT_ANL_RESPOSTA,
                   ID_USUARIO,
                   ID_REGIST_EMOCAO
              FROM T_NRON_RESP_FORMULARIO
             ORDER BY DT_RESPOSTA DESC
            """,
            {},
        )
        if not linhas:
            print("Nenhuma resposta encontrada.")
            return
        for linha in linhas:
            print(
                f"{linha['id_resposta']:>3} | Usuário: {linha['id_usuario']} | Data: {linha['dt_resposta']} | "
                f"Motivação: {linha['mot_resposta']} | Estresse: {linha['est_resposta']} | Modelo: {linha['mod_ver_resposta']}"
            )
    except Exception as exc:
        print(f"Erro ao listar respostas: {exc}")
    finally:
        pausar()


def atualizar_resposta_formulario() -> None:
    # Possibilita ajustar notas/observações e metadados da análise.
    try:
        limpar_tela()
        print("--- Atualizar Resposta de Formulário ---")
        resposta_id = int(input("ID da resposta: ").strip())
        resposta = buscar_por_id(TABELA, "ID_RESPOSTA", resposta_id)
        if not resposta:
            print("Resposta não encontrada.")
            return
        novo_status_mot = input(f"Motivação atual ({resposta['mot_resposta']}): ").strip() or resposta["mot_resposta"]
        nova_felicidade = input(f"Felicidade atual ({resposta['fel_resposta']}): ").strip() or resposta["fel_resposta"]
        novo_estresse = input(f"Estresse atual ({resposta['est_resposta']}): ").strip() or resposta["est_resposta"]
        nova_observacao = input(f"Observação atual ({resposta['obs_resposta']}): ").strip() or resposta["obs_resposta"]
        nova_saude = input(f"Saúde mental atual ({resposta['sau_men_resposta']}): ").strip() or resposta["sau_men_resposta"]
        nova_prob = input(f"Confiança atual ({resposta['prob_resposta']}): ").strip() or resposta["prob_resposta"]
        novo_modelo = input(f"Modelo atual ({resposta['mod_ver_resposta']}): ").strip() or resposta["mod_ver_resposta"]
        data_anl_atual = resposta["dt_anl_resposta"]
        if hasattr(data_anl_atual, "strftime"):
            data_anl_atual = data_anl_atual.strftime("%Y-%m-%d")
        nova_data_analise = input(f"Data análise atual ({data_anl_atual}): ").strip() or data_anl_atual
        run_execute(
            """
            UPDATE T_NRON_RESP_FORMULARIO
               SET MOT_RESPOSTA     = :motivacao,
                   FEL_RESPOSTA     = :felicidade,
                   EST_RESPOSTA     = :estresse,
                   OBS_RESPOSTA     = :observacao,
                   SAU_MEN_RESPOSTA = :saude,
                   PROB_RESPOSTA    = :probabilidade,
                   MOD_VER_RESPOSTA = :modelo,
                   DT_ANL_RESPOSTA  = TO_DATE(:dt_analise, 'YYYY-MM-DD')
             WHERE ID_RESPOSTA      = :id
            """,
            {
                "motivacao": novo_status_mot,
                "felicidade": nova_felicidade,
                "estresse": novo_estresse,
                "observacao": nova_observacao,
                "saude": nova_saude,
                "probabilidade": nova_prob,
                "modelo": novo_modelo,
                "dt_analise": nova_data_analise,
                "id": resposta_id,
            },
        )
        print("Resposta atualizada.")
    except Exception as exc:
        print(f"Erro ao atualizar resposta: {exc}")
    finally:
        pausar()


def excluir_resposta_formulario() -> None:
    # Remove uma resposta específica mediante confirmação.
    try:
        limpar_tela()
        print("--- Excluir Resposta de Formulário ---")
        resposta_id = int(input("ID da resposta: ").strip())
        if not buscar_por_id(TABELA, "ID_RESPOSTA", resposta_id):
            print("Resposta não encontrada.")
            return
        if not solicitar_confirmacao("Confirmar exclusão?"):
            print("Operação cancelada.")
            return
        linhas = run_execute("DELETE FROM T_NRON_RESP_FORMULARIO WHERE ID_RESPOSTA = :id", {"id": resposta_id})
        if linhas:
            print("Resposta excluída.")
        else:
            print("Nenhuma linha afetada.")
    except Exception as exc:
        print(f"Erro ao excluir resposta: {exc}")
    finally:
        pausar()
