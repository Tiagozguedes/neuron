"""Consultas auxiliares para reuso entre CRUDs."""

from __future__ import annotations

from typing import Any

from connect.connect import run_query


def registro_existe(tabela: str, campo: str, valor: Any) -> bool:
    """Retorna True se o valor existir na tabela/campo informado."""
    # Auxilia nos CRUDs evitando duplicidade ou FK inválida.
    sql = f"SELECT 1 FROM {tabela} WHERE {campo} = :valor FETCH FIRST 1 ROWS ONLY"
    return bool(run_query(sql, {"valor": valor}))


def buscar_por_id(tabela: str, campo_id: str, valor: Any) -> dict[str, Any] | None:
    """Busca um registro por ID e devolve o dicionário da linha."""
    # Usado antes de updates/deletes para validar existência e preencher valores padrão.
    sql = f"SELECT * FROM {tabela} WHERE {campo_id} = :valor"
    rows = run_query(sql, {"valor": valor})
    return rows[0] if rows else None


def proximo_id(tabela: str, campo_id: str) -> int:
    """Retorna o próximo ID sequencial usando MAX + 1 (útil para tabelas sem sequence)."""
    # Evita ter de solicitar manualmente o ID ao usuário quando o Oracle não tem sequence.
    sql = f"SELECT NVL(MAX({campo_id}), 0) + 1 AS proximo FROM {tabela}"
    rows = run_query(sql, {})
    if not rows:
        return 1
    return int(rows[0]["proximo"])
