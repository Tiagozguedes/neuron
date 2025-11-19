"""Camada de serviços para consultas e relatórios agregados."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from connect.connect import run_query


def historico_emocoes() -> list[dict[str, Any]]:
    """Ranking simples das emoções mais registradas."""
    return run_query(
        """
        SELECT e.NM_EMOCAO AS emocao,
               COUNT(r.ID_REGIST_EMOCAO) AS total_registros,
               ROUND(AVG(r.INT_REGIST_EMOCAO), 2) AS intensidade_media
          FROM T_NRON_EMOCAO e
          LEFT JOIN T_NRON_REGIST_EMOCAO r ON r.ID_EMOCAO = e.ID_EMOCAO
         GROUP BY e.NM_EMOCAO
         ORDER BY total_registros DESC, intensidade_media DESC
        """,
        {},
    )


def listar_departamentos() -> list[dict[str, Any]]:
    """Lista departamentos para filtros opcionais nos relatórios."""
    return run_query(
        "SELECT ID_DEPARTAMENTO, NOME_DEPARTAMENTO FROM T_NRON_DEPARTAMENTO ORDER BY NOME_DEPARTAMENTO",
        {},
    )


def colaboradores_por_departamento() -> list[dict[str, Any]]:
    """Quantidade de colaboradores ativos/inativos por departamento."""
    return run_query(
        """
        SELECT d.NOME_DEPARTAMENTO        AS nome_departamento,
               COUNT(u.ID_USUARIO)        AS total_colaboradores,
               COALESCE(SUM(CASE WHEN u.STT_USUARIO = 'A' THEN 1 ELSE 0 END), 0) AS ativos,
               COALESCE(SUM(CASE WHEN u.STT_USUARIO <> 'A' THEN 1 ELSE 0 END), 0) AS inativos
          FROM T_NRON_DEPARTAMENTO d
          LEFT JOIN T_NRON_USUARIO u ON u.ID_DEPARTAMENTO = d.ID_DEPARTAMENTO
         GROUP BY d.NOME_DEPARTAMENTO
         ORDER BY total_colaboradores DESC, d.NOME_DEPARTAMENTO
        """,
        {},
    )


def metricas_por_departamento() -> list[dict[str, Any]]:
    """Médias de motivação/felicidade/estresse por departamento com total de check-ins."""
    return run_query(
        """
        SELECT d.NOME_DEPARTAMENTO AS nome_departamento,
               COUNT(r.ID_RESPOSTA) AS total_checkins,
               ROUND(AVG(r.MOT_RESPOSTA), 2) AS motivacao_media,
               ROUND(AVG(r.FEL_RESPOSTA), 2) AS felicidade_media,
               ROUND(AVG(r.EST_RESPOSTA), 2) AS estresse_medio,
               ROUND(AVG(r.SAU_MEN_RESPOSTA), 2) AS saude_mental_media
          FROM T_NRON_RESP_FORMULARIO r
          JOIN T_NRON_USUARIO u ON u.ID_USUARIO = r.ID_USUARIO
          JOIN T_NRON_DEPARTAMENTO d ON d.ID_DEPARTAMENTO = u.ID_DEPARTAMENTO
         GROUP BY d.NOME_DEPARTAMENTO
         ORDER BY total_checkins DESC, d.NOME_DEPARTAMENTO
        """,
        {},
    )


def tendencia_temporal(data_inicio: datetime, data_fim: datetime, granularidade: str) -> list[dict[str, Any]]:
    """Evolução de motivação/felicidade/estresse agrupada por dia/semana/mês."""
    granularidade = granularidade.upper()
    if granularidade not in {"DIA", "SEMANA", "MES"}:
        granularidade = "SEMANA"
    return run_query(
        f"""
        SELECT periodo,
               COUNT(*) AS total_checkins,
               ROUND(AVG(MOT_RESPOSTA), 2) AS motivacao_media,
               ROUND(AVG(FEL_RESPOSTA), 2) AS felicidade_media,
               ROUND(AVG(EST_RESPOSTA), 2) AS estresse_medio
          FROM (
                SELECT CASE
                         WHEN '{granularidade}' = 'DIA' THEN TRUNC(DT_RESPOSTA)
                         WHEN '{granularidade}' = 'SEMANA' THEN TRUNC(DT_RESPOSTA, 'IW')
                         ELSE TRUNC(DT_RESPOSTA, 'MM')
                       END AS periodo,
                       MOT_RESPOSTA,
                       FEL_RESPOSTA,
                       EST_RESPOSTA
                  FROM T_NRON_RESP_FORMULARIO
                 WHERE DT_RESPOSTA BETWEEN :inicio AND :fim
               )
         GROUP BY periodo
         ORDER BY periodo
        """,
        {"inicio": data_inicio, "fim": data_fim},
    )


def ranking_emocoes(
    data_inicio: datetime, data_fim: datetime, departamento_id: int | None = None
) -> list[dict[str, Any]]:
    """Quantidade de registros por emoção em um período, com filtro opcional por departamento."""
    return run_query(
        """
        SELECT e.NM_EMOCAO              AS emocao,
               d.NOME_DEPARTAMENTO      AS departamento,
               COUNT(r.ID_REGIST_EMOCAO) AS total
          FROM T_NRON_REGIST_EMOCAO r
          JOIN T_NRON_EMOCAO e ON e.ID_EMOCAO = r.ID_EMOCAO
          JOIN T_NRON_RESP_FORMULARIO f ON f.ID_REGIST_EMOCAO = r.ID_REGIST_EMOCAO
          JOIN T_NRON_USUARIO u ON u.ID_USUARIO = f.ID_USUARIO
          JOIN T_NRON_DEPARTAMENTO d ON d.ID_DEPARTAMENTO = u.ID_DEPARTAMENTO
         WHERE r.DT_REGIST_EMOCAO BETWEEN :inicio AND :fim
           AND (:departamento_id IS NULL OR d.ID_DEPARTAMENTO = :departamento_id)
         GROUP BY e.NM_EMOCAO, d.NOME_DEPARTAMENTO
         ORDER BY total DESC, e.NM_EMOCAO
        """,
        {"inicio": data_inicio, "fim": data_fim, "departamento_id": departamento_id},
    )


def ranking_estresse_departamentos(limite: int = 5) -> list[dict[str, Any]]:
    """Retorna os departamentos com maior estresse médio (com pelo menos 3 check-ins)."""
    limite = max(1, min(limite, 20))
    return run_query(
        f"""
        SELECT *
          FROM (
                SELECT d.NOME_DEPARTAMENTO AS nome_departamento,
                       COUNT(r.ID_RESPOSTA) AS total_checkins,
                       ROUND(AVG(r.EST_RESPOSTA), 2) AS estresse_medio,
                       ROUND(AVG(r.MOT_RESPOSTA), 2) AS motivacao_media
                  FROM T_NRON_RESP_FORMULARIO r
                  JOIN T_NRON_USUARIO u ON u.ID_USUARIO = r.ID_USUARIO
                  JOIN T_NRON_DEPARTAMENTO d ON d.ID_DEPARTAMENTO = u.ID_DEPARTAMENTO
                 GROUP BY d.NOME_DEPARTAMENTO
               )
         WHERE total_checkins >= 3
         ORDER BY estresse_medio DESC, motivacao_media ASC
         FETCH FIRST {limite} ROWS ONLY
        """,
        {},
    )
