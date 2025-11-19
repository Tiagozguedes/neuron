"""Serviços relacionados ao fluxo de check-in emocional."""

from __future__ import annotations

from datetime import datetime, timezone

from connect.connect import run_query, transaction
from db_utils import proximo_id, registro_existe
from services.analise_emocional import EmotionReport


def usuario_existe(usuario_id: int) -> bool:
    """Verifica se o colaborador informado está cadastrado."""
    return registro_existe("T_NRON_USUARIO", "ID_USUARIO", usuario_id)


def listar_emocoes() -> list[dict[str, object]]:
    """Obtém todas as emoções cadastradas para exibição no CLI."""
    return run_query("SELECT ID_EMOCAO, NM_EMOCAO FROM T_NRON_EMOCAO ORDER BY NM_EMOCAO", {})


def buscar_emocao_id_por_nome(nome: str) -> int | None:
    """Busca uma emoção existente a partir do nome (case insensitive)."""
    if not nome:
        return None
    linhas = run_query(
        "SELECT ID_EMOCAO FROM T_NRON_EMOCAO WHERE UPPER(NM_EMOCAO) = UPPER(:nome)",
        {"nome": nome.strip()},
    )
    if not linhas:
        return None
    return int(linhas[0]["id_emocao"])


def salvar_checkin(usuario_id: int, relato_texto: str, relatorio: EmotionReport, emocao_id: int) -> tuple[int, int]:
    """Persiste registro emocional + resposta do formulário em uma transação."""
    with transaction() as cursor:
        registro_id = _criar_registro_emocao(emocao_id, relatorio, cursor)
        resposta_id = _persistir_resposta(usuario_id, relato_texto, relatorio, registro_id, cursor)
    return registro_id, resposta_id


def _persistir_resposta(
    usuario_id: int,
    relato_texto: str,
    relatorio: EmotionReport,
    registro_id: int,
    cursor,
) -> int:
    resposta_id = proximo_id("T_NRON_RESP_FORMULARIO", "ID_RESPOSTA")
    agora = _normalizar_datetime(datetime.now(timezone.utc))
    observacao = relatorio.resumo or relato_texto
    if relatorio.insights:
        dicas = " ".join(relatorio.insights)
        observacao = f"{observacao} Recomendações: {dicas}"
    observacao = (observacao or "")[:250]
    cursor.execute(
        """
        INSERT INTO T_NRON_RESP_FORMULARIO (
            ID_RESPOSTA,
            DT_RESPOSTA,
            MOT_RESPOSTA,
            FEL_RESPOSTA,
            EST_RESPOSTA,
            OBS_RESPOSTA,
            SAU_MEN_RESPOSTA,
            PROB_RESPOSTA,
            MOD_VER_RESPOSTA,
            DT_ANL_RESPOSTA,
            ID_USUARIO,
            ID_REGIST_EMOCAO
        ) VALUES (
            :id_resposta,
            :dt_resposta,
            :motivacao,
            :felicidade,
            :estresse,
            :observacao,
            :saude_mental,
            :probabilidade,
            :modelo,
            :dt_analise,
            :id_usuario,
            :id_registro
        )
        """,
        {
            "id_resposta": resposta_id,
            "dt_resposta": agora,
            "motivacao": relatorio.motivacao,
            "felicidade": relatorio.felicidade,
            "estresse": relatorio.estresse,
            "observacao": observacao,
            "saude_mental": relatorio.saude_mental,
            "probabilidade": relatorio.probabilidade,
            "modelo": relatorio.modelo_versao,
            "dt_analise": _normalizar_datetime(relatorio.data_analise),
            "id_usuario": usuario_id,
            "id_registro": registro_id,
        },
    )
    return resposta_id


def _criar_registro_emocao(emocao_id: int, relatorio: EmotionReport, cursor) -> int:
    registro_id = proximo_id("T_NRON_REGIST_EMOCAO", "ID_REGIST_EMOCAO")
    descricao_base = relatorio.resumo or f"Emoção predominante: {relatorio.emocao_nome}"
    descricao = (descricao_base or "")[:255]
    cursor.execute(
        """
        INSERT INTO T_NRON_REGIST_EMOCAO (
            ID_REGIST_EMOCAO,
            INT_REGIST_EMOCAO,
            DS_REGIST_EMOCAO,
            DT_REGIST_EMOCAO,
            ID_EMOCAO
        ) VALUES (
            :id_registro,
            :intensidade,
            :descricao,
            :data_registro,
            :id_emocao
        )
        """,
        {
            "id_registro": registro_id,
            "intensidade": relatorio.intensidade,
            "descricao": descricao,
            "data_registro": _normalizar_datetime(relatorio.data_analise),
            "id_emocao": emocao_id,
        },
    )
    return registro_id


def _normalizar_datetime(valor: datetime) -> datetime:
    """Remove timezone para compatibilidade com colunas DATE do Oracle mantendo UTC."""
    if valor.tzinfo is None:
        return valor
    return valor.astimezone(timezone.utc).replace(tzinfo=None)
