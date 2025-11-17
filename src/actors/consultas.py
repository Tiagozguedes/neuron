"""Consultas analíticas com opção de exportação em JSON."""

from __future__ import annotations

import json
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from typing import Any

from connect.connect import run_query
from utils import deseja_voltar, limpar_tela, pausar, solicitar_confirmacao

EXPORT_DIR = Path("exports")


def menu_consultas() -> None:
    """Menu principal para as consultas exigidas no projeto."""
    while True:
        limpar_tela()
        print("=== Consultas e Relatórios ===")
        print("1. Distribuição de colaboradores por departamento")
        print("2. Emoções mais registradas")
        print("3. Panorama de bem-estar por departamento")
        print("0. Voltar")
        entrada = input("\nEscolha: ").strip()
        if deseja_voltar(entrada):
            break
        opcao = entrada
        if opcao == "1":
            _consulta_colaboradores_por_departamento()
        elif opcao == "2":
            _consulta_emocoes_recorrentes()
        elif opcao == "3":
            _consulta_metricas_por_departamento()
        else:
            print("Opção inválida.")
            pausar()


def _consulta_colaboradores_por_departamento() -> None:
    """Mostra quantidade de usuários (ativos/inativos) em cada departamento."""
    limpar_tela()
    print("--- Distribuição de Colaboradores ---\n")
    linhas = run_query(
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
    if not linhas:
        print("Nenhum departamento cadastrado.")
    else:
        for linha in linhas:
            nome = linha.get("nome_departamento") or "Sem nome"
            print(
                f"{nome:<25} | Total: {linha['total_colaboradores']:>3} | "
                f"Ativos: {linha['ativos']:>3} | Inativos: {linha['inativos']:>3}",
            )
        _exportar_se_desejado("colaboradores_por_departamento", linhas)
    pausar()


def _consulta_emocoes_recorrentes() -> None:
    """Apresenta o ranking das emoções mais registradas pela IA."""
    limpar_tela()
    print("--- Emoções Mais Registradas ---\n")
    linhas = run_query(
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
    if not linhas:
        print("Nenhuma emoção cadastrada.")
    else:
        for idx, linha in enumerate(linhas, 1):
            print(
                f"{idx:>2}. {linha['emocao']:<20} | Registros: {linha['total_registros']:>3} | "
                f"Intensidade média: {linha.get('intensidade_media') or 0}",
            )
        _exportar_se_desejado("emocoes_mais_registradas", linhas)
    pausar()


def _consulta_metricas_por_departamento() -> None:
    """Exibe médias das métricas de bem-estar por departamento."""
    limpar_tela()
    print("--- Panorama de Bem-estar ---\n")
    linhas = run_query(
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
    if not linhas:
        print("Nenhum check-in registrado.")
    else:
        cabecalho = (
            f"{'Departamento':<20} | {'Check-ins':>9} | {'Motivação':>10} | {'Felicidade':>11} | "
            f"{'Estresse':>9} | {'Saúde mental':>13}"
        )
        print(cabecalho)
        print("-" * len(cabecalho))
        for linha in linhas:
            print(
                f"{(linha['nome_departamento'] or 'N/D'):<20} | "
                f"{linha['total_checkins']:>9} | "
                f"{_formatar_decimal(linha.get('motivacao_media')):>10} | "
                f"{_formatar_decimal(linha.get('felicidade_media')):>11} | "
                f"{_formatar_decimal(linha.get('estresse_medio')):>9} | "
                f"{_formatar_decimal(linha.get('saude_mental_media')):>13}",
            )
        _exportar_se_desejado("bem_estar_por_departamento", linhas)
    pausar()


def _formatar_decimal(valor: Any) -> str:
    if valor is None:
        return "-"
    return str(valor)


def _exportar_se_desejado(nome_base: str, linhas: list[dict[str, Any]]) -> None:
    """Pergunta ao usuário se deseja salvar o resultado em disco."""
    if not linhas:
        return
    if not solicitar_confirmacao("\nDeseja exportar este resultado para JSON?"):
        return
    EXPORT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo = EXPORT_DIR / f"{nome_base}_{timestamp}.json"
    conteudo = [_normalizar_linha(linha) for linha in linhas]
    arquivo.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nArquivo exportado em: {arquivo.resolve()}")


def _normalizar_linha(linha: dict[str, Any]) -> dict[str, Any]:
    """Converte valores não serializáveis (Decimal, datetime) para strings ou floats."""
    return {chave: _normalizar_valor(valor) for chave, valor in linha.items()}


def _normalizar_valor(valor: Any) -> Any:
    if isinstance(valor, Decimal):
        return float(valor)
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    return valor
