"""Funções utilitárias para executar comandos no Oracle."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any

from dotenv import load_dotenv

try:
    import oracledb
except ModuleNotFoundError:  # pragma: no cover
    oracledb = None  # type: ignore


load_dotenv()  # carrega variáveis definidas em .env (se existir)


def _obter_conn() -> "oracledb.Connection":
    # Abre uma conexão nova com o Oracle utilizando variáveis de ambiente para credenciais/DSN.
    if oracledb is None:  # pragma: no cover
        raise RuntimeError(
            "Dependência 'oracledb' não encontrada. Instale via 'pip install oracledb'.",
        )
    return oracledb.connect(  # type: ignore[call-arg]
        user=os.getenv("ORACLE_USER", "user"),
        password=os.getenv("ORACLE_PASSWORD", "password"),
        dsn=_build_dsn(),
    )


def _build_dsn() -> str:
    # Constrói o DSN final a partir de ORACLE_DSN ou dos componentes host/porta/SID.
    """Monta o DSN a partir das variáveis de ambiente."""
    dsn = os.getenv("ORACLE_DSN")
    if dsn:
        return dsn
    host = os.getenv("ORACLE_HOST")
    port = os.getenv("ORACLE_PORT")
    service = os.getenv("ORACLE_SERVICE")
    sid = os.getenv("ORACLE_SID")
    if host and port and (service or sid) and oracledb is not None:
        try:
            port_int = int(port)
        except ValueError:
            port_int = 1521
        if service:
            return oracledb.makedsn(host, port_int, service_name=service)  # type: ignore[no-any-return]
        return oracledb.makedsn(host, port_int, sid=sid)  # type: ignore[no-any-return]
    return "localhost/orclpdb1"


@contextmanager
def _cursor():
    # Garante criação/fechamento de conexão e cursor com commit/rollback automático.
    conn = _obter_conn()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def run_execute(sql: str, params: dict[str, Any]) -> int:
    """Executa INSERT/UPDATE/DELETE e retorna linhas afetadas."""
    # Usado pelos CRUDs para disparar instruções que modificam dados.
    with _cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.rowcount


def run_query(sql: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Executa SELECT e retorna linhas como dicionários."""
    # Centraliza os SELECTs retornando colunas sempre em minúsculo.
    with _cursor() as cursor:
        cursor.execute(sql, params or {})
        columns = [col[0].lower() for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
