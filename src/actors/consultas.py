"""Consultas analíticas com opção de exportação em JSON."""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from services import relatorios
from utils import (
    OperacaoCancelada,
    input_opcao,
    limpar_tela,
    pausar,
    solicitar_confirmacao,
    solicitar_data,
    solicitar_texto,
    titulo,
)

EXPORT_DIR = Path("exports")
MIN_AGREGACAO = 3


def menu_consultas() -> None:
    """Menu principal para as consultas exigidas no projeto."""
    while True:
        limpar_tela()
        titulo("Relatórios e Consultas")
        print("1. Histórico emocional dos colaboradores")
        print("2. Relatórios agregados por departamento")
        print("3. Relatórios organizacionais")
        print("4. Tendência emocional por período")
        print("5. Emoções predominantes (período/departamento)")
        print("6. Ranking de estresse por departamento")
        print("0. Voltar")
        opcao = input_opcao("\nEscolha uma opção: ", ("1", "2", "3", "4", "5", "6", "0"))
        if opcao == "0":
            break
        if opcao == "1":
            _consulta_emocoes_recorrentes()
        elif opcao == "2":
            _consulta_colaboradores_por_departamento()
        elif opcao == "3":
            _consulta_metricas_por_departamento()
        elif opcao == "4":
            _consulta_tendencia_temporal()
        elif opcao == "5":
            _consulta_emocoes_por_periodo()
        elif opcao == "6":
            _ranking_estresse_departamentos()


def _consulta_colaboradores_por_departamento() -> None:
    """Mostra quantidade de usuários (ativos/inativos) em cada departamento."""
    limpar_tela()
    titulo("Relatórios agregados por departamento")
    linhas = relatorios.colaboradores_por_departamento()
    if not linhas:
        print("Nenhum departamento cadastrado.")
    else:
        linhas_privadas = [linha for linha in linhas if linha["total_colaboradores"] >= MIN_AGREGACAO]
        ocultados = len(linhas) - len(linhas_privadas)
        if not linhas_privadas:
            print(
                "Para preservar a privacidade dos colaboradores, é necessário ter ao menos "
                f"{MIN_AGREGACAO} pessoas por departamento para exibir dados agregados.",
            )
        else:
            for linha in linhas_privadas:
                nome = linha.get("nome_departamento") or "Sem nome"
                print(
                    f"{nome:<25} | Total: {linha['total_colaboradores']:>3} | "
                    f"Ativos: {linha['ativos']:>3} | Inativos: {linha['inativos']:>3}",
                )
            if ocultados:
                print(f"\n{ocultados} departamento(s) foram ocultados para evitar reidentificação.")
            _exportar_se_desejado("colaboradores_por_departamento", linhas_privadas)
    pausar()


def _consulta_emocoes_recorrentes() -> None:
    """Apresenta o ranking das emoções mais registradas pela IA."""
    limpar_tela()
    titulo("Histórico emocional dos colaboradores")
    linhas = relatorios.historico_emocoes()
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
    titulo("Relatórios organizacionais")
    linhas = relatorios.metricas_por_departamento()
    if not linhas:
        print("Nenhum check-in registrado.")
    else:
        linhas_privadas = [linha for linha in linhas if linha["total_checkins"] >= MIN_AGREGACAO]
        ocultados = len(linhas) - len(linhas_privadas)
        if not linhas_privadas:
            print(
                "Para proteger a confidencialidade, somente departamentos com "
                f"{MIN_AGREGACAO} ou mais check-ins aparecem neste relatório.",
            )
        else:
            cabecalho = (
                f"{'Departamento':<20} | {'Check-ins':>9} | {'Motivação':>10} | {'Felicidade':>11} | "
                f"{'Estresse':>9} | {'Saúde mental':>13}"
            )
            print(cabecalho)
            print("-" * len(cabecalho))
            for linha in linhas_privadas:
                print(
                    f"{(linha['nome_departamento'] or 'N/D'):<20} | "
                    f"{linha['total_checkins']:>9} | "
                    f"{_formatar_decimal(linha.get('motivacao_media')):>10} | "
                    f"{_formatar_decimal(linha.get('felicidade_media')):>11} | "
                    f"{_formatar_decimal(linha.get('estresse_medio')):>9} | "
                    f"{_formatar_decimal(linha.get('saude_mental_media')):>13}",
                )
            if ocultados:
                print(f"\n{ocultados} departamento(s) foram omitidos para evitar identificação individual.")
            _exportar_se_desejado("bem_estar_por_departamento", linhas_privadas)
    pausar()


def _consulta_tendencia_temporal() -> None:
    """Mostra a evolução das métricas de bem-estar em um intervalo definido."""
    limpar_tela()
    titulo("Tendência emocional por período")
    try:
        inicio, fim = _solicitar_intervalo_datas()
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
        pausar()
        return
    granularidade_opcao = input_opcao(
        "Agrupar por (1=Dia, 2=Semana, 3=Mês): ",
        ("1", "2", "3"),
    )
    granularidade = {"1": "DIA", "2": "SEMANA", "3": "MES"}[granularidade_opcao]
    linhas = relatorios.tendencia_temporal(inicio, fim, granularidade)
    if not linhas:
        print("Nenhum check-in registrado no período informado.")
    else:
        cabecalho = f"{'Período':<12} | {'Check-ins':>9} | {'Motivação':>10} | {'Felicidade':>11} | {'Estresse':>9}"
        print(cabecalho)
        print("-" * len(cabecalho))
        for linha in linhas:
            periodo = _formatar_periodo(linha["periodo"])
            print(
                f"{periodo:<12} | "
                f"{linha['total_checkins']:>9} | "
                f"{_formatar_decimal(linha.get('motivacao_media')):>10} | "
                f"{_formatar_decimal(linha.get('felicidade_media')):>11} | "
                f"{_formatar_decimal(linha.get('estresse_medio')):>9}",
            )
        _exportar_se_desejado("tendencia_emocional", linhas)
    pausar()


def _consulta_emocoes_por_periodo() -> None:
    """Ranking de emoções predominantes em um intervalo, com filtro opcional de departamento."""
    limpar_tela()
    titulo("Emoções predominantes")
    try:
        inicio, fim = _solicitar_intervalo_datas()
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
        pausar()
        return
    departamento_id = _selecionar_departamento()
    linhas = relatorios.ranking_emocoes(inicio, fim, departamento_id)
    if not linhas:
        print("Nenhum registro encontrado para o filtro informado.")
    else:
        for idx, linha in enumerate(linhas, start=1):
            print(
                f"{idx:>2}. {linha['emocao']:<15} | Departamento: {linha['departamento']:<25} | "
                f"Total: {linha['total']:>3}"
            )
        _exportar_se_desejado("ranking_emocoes", linhas)
    pausar()


def _ranking_estresse_departamentos() -> None:
    """Destaca os departamentos com maior estresse médio."""
    limpar_tela()
    titulo("Ranking de estresse por departamento")
    linhas = relatorios.ranking_estresse_departamentos()
    if not linhas:
        print("Ainda não há dados suficientes para montar o ranking.")
    else:
        cabecalho = f"{'Departamento':<25} | {'Check-ins':>9} | {'Estresse médio':>15} | {'Motivação média':>16}"
        print(cabecalho)
        print("-" * len(cabecalho))
        for linha in linhas:
            print(
                f"{linha['nome_departamento']:<25} | "
                f"{linha['total_checkins']:>9} | "
                f"{_formatar_decimal(linha.get('estresse_medio')):>15} | "
                f"{_formatar_decimal(linha.get('motivacao_media')):>16}"
            )
        _exportar_se_desejado("ranking_estresse_departamentos", linhas)
    pausar()


def _formatar_decimal(valor: Any) -> str:
    """Converte Decimals para string e retorna '-' para nulos."""
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


def _solicitar_intervalo_datas() -> tuple[datetime, datetime]:
    """Pergunta ao usuário o intervalo desejado e retorna datas datetime prontas para a consulta."""
    hoje = date.today()
    inicio_padrao = hoje - timedelta(days=30)
    print("Informe o intervalo desejado (use DDMMYYYY). Enter mantém o padrão.")
    data_inicio = solicitar_data("Data inicial [últimos 30 dias]", padrao=inicio_padrao, obrigatorio=False) or inicio_padrao
    data_fim = solicitar_data("Data final [hoje]", padrao=hoje, obrigatorio=False) or hoje
    if data_inicio > data_fim:
        data_inicio, data_fim = data_fim, data_inicio
    return (
        datetime.combine(data_inicio, datetime.min.time()),
        datetime.combine(data_fim, datetime.max.time()),
    )


def _selecionar_departamento() -> int | None:
    """Exibe departamentos cadastrados e permite filtrar relatórios."""
    departamentos = relatorios.listar_departamentos()
    if not departamentos:
        return None
    print("\nDepartamentos cadastrados:")
    for depto in departamentos:
        print(f"  {depto['id_departamento']:>3} | {depto['nome_departamento']}")
    ids_validos = {int(depto["id_departamento"]) for depto in departamentos}
    while True:
        try:
            resposta = solicitar_texto("ID do departamento [Enter para todos]", obrigatorio=False)
        except OperacaoCancelada:
            return None
        if not resposta:
            return None
        try:
            valor = int(resposta)
        except ValueError:
            print("Valor inválido. Digite apenas números ou pressione Enter para considerar todos.")
            continue
        if valor in ids_validos:
            return valor
        print("Departamento não encontrado. Informe um dos IDs listados acima.")


def _formatar_periodo(valor: Any) -> str:
    """Normaliza datas/periodos retornados pelo Oracle para exibição."""
    if isinstance(valor, datetime):
        return valor.strftime("%Y-%m-%d")
    if isinstance(valor, date):
        return valor.isoformat()
    return str(valor)
