"""Camada de domínio responsável por produzir relatórios emocionais a partir da análise local."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Mapping, Sequence

from services.analise_emocional_local import EMOTION_PROFILES, analisar_texto_local


class AnaliseEmocionalError(RuntimeError):
    """Erro amigável emitido quando não é possível processar o relato."""


@dataclass(slots=True)
class MensagemAnalise:
    """Representa cada mensagem analisada pela heurística local."""

    texto: str
    timestamp: datetime | None
    data: datetime | None
    emocao: str | None
    sentimento: str | None
    emocao_scores: Mapping[str, Decimal]
    sentimento_scores: Mapping[str, Decimal]
    sentimento_fonte: str | None


@dataclass(slots=True)
class EmotionReport:
    """Estrutura consolidada consumida pelo fluxo de check-in."""

    mensagens: tuple[MensagemAnalise, ...]
    resumo: str
    resumo_detalhado: Mapping[str, Any] | None
    motivacao: Decimal
    felicidade: Decimal
    estresse: Decimal
    saude_mental: Decimal
    energia: Decimal
    probabilidade: Decimal
    modelo_versao: str
    data_analise: datetime
    emocao_nome: str
    emocao_id: int | None
    intensidade: Decimal
    insights: tuple[str, ...]
    emocoes_secundarias: tuple[tuple[str, Decimal], ...]
    emocoes_distribuicao: Mapping[str, Decimal]
    sentimentos_distribuicao: Mapping[str, Decimal]


def analisar_conversa(mensagens: Sequence[Mapping[str, Any]]) -> EmotionReport:
    """Processa uma sequência de mensagens usando a heurística local."""
    if not mensagens:
        raise AnaliseEmocionalError("Forneça ao menos uma mensagem para a análise emocional.")
    mensagens_normalizadas = tuple(_processar_mensagem(item) for item in mensagens)
    return _construir_relatorio(mensagens_normalizadas)


def analisar_texto(texto: str, usuario_id: int | None = None) -> EmotionReport:
    """Compatibilidade com chamadas legadas que enviavam apenas um texto."""
    _ = usuario_id
    mensagem = {"texto": texto, "timestamp": datetime.now(timezone.utc)}
    return analisar_conversa([mensagem])


def _processar_mensagem(item: Mapping[str, Any] | Any) -> MensagemAnalise:
    """Valida a entrada, normaliza texto e traduz o resultado bruto da heurística em MensagemAnalise."""
    if not isinstance(item, Mapping):
        raise AnaliseEmocionalError("Cada mensagem deve ser um dicionário com o campo 'texto'.")
    texto = str(item.get("texto") or item.get("text") or "").strip()
    if not texto:
        raise AnaliseEmocionalError("Cada mensagem precisa conter um texto para análise.")
    timestamp = _parse_datetime(item.get("timestamp"))
    resultado = analisar_texto_local(texto)
    emocao = _extrair_str(resultado.get("emocao"))
    sentimento = _extrair_str(resultado.get("sentimento"))
    emocao_scores = _scores_para_decimal(resultado.get("emocao_scores"))
    sentimento_scores = _scores_para_decimal(resultado.get("sentimento_scores"))
    return MensagemAnalise(
        texto=texto,
        timestamp=timestamp,
        data=timestamp,
        emocao=emocao,
        sentimento=sentimento,
        emocao_scores=emocao_scores,
        sentimento_scores=sentimento_scores,
        sentimento_fonte="analise_local",
    )


def _construir_relatorio(mensagens: Sequence[MensagemAnalise]) -> EmotionReport:
    """Combina mensagens analisadas em um relatório consolidado com métricas e insights."""
    referencia = mensagens[0]
    emocao_distribuicao = _combinar_emocoes(mensagens, referencia)  # mistura scores das mensagens
    sentimentos_distribuicao = _combinar_sentimentos(mensagens, referencia)  # idem para sentimentos
    emocao_nome = _selecionar_principal(emocao_distribuicao) or (referencia.emocao or "Neutro")
    resumo = _montar_resumo(referencia, emocao_distribuicao)
    motivacao, felicidade, estresse, energia = _calcular_metricas(emocao_distribuicao, referencia)
    saude_mental = _media((motivacao, felicidade, Decimal("100") - estresse))
    intensidade = _calcular_intensidade(emocao_distribuicao, energia)
    probabilidade = _estimar_confianca(emocao_distribuicao, sentimentos_distribuicao, intensidade)
    insights = _gerar_insights(emocao_nome, sentimentos_distribuicao, motivacao, estresse)
    secundarias = _listar_secundarias(emocao_distribuicao, emocao_nome)
    return EmotionReport(
        mensagens=tuple(mensagens),
        resumo=resumo,
        resumo_detalhado={"emocoes": emocao_distribuicao, "sentimentos": sentimentos_distribuicao},
        motivacao=motivacao,
        felicidade=felicidade,
        estresse=estresse,
        saude_mental=saude_mental,
        energia=energia,
        probabilidade=probabilidade,
        modelo_versao="Heuristica-Local v1",
        data_analise=datetime.now(timezone.utc),
        emocao_nome=emocao_nome,
        emocao_id=None,
        intensidade=intensidade,
        insights=insights,
        emocoes_secundarias=secundarias,
        emocoes_distribuicao=emocao_distribuicao,
        sentimentos_distribuicao=sentimentos_distribuicao,
    )


def _montar_resumo(mensagem: MensagemAnalise, distrib: Mapping[str, Decimal]) -> str:
    """Gera um texto curto destacando emoções/sentimento e trecho do relato."""
    partes: list[str] = []
    if distrib:
        principais = sorted(distrib.items(), key=lambda item: item[1], reverse=True)[:3]
        destaque = ", ".join(f"{nome} ({valor}%)" for nome, valor in principais)
        partes.append(f"Emoções: {destaque}")
    elif mensagem.emocao:
        partes.append(f"Emoção: {mensagem.emocao}")
    if mensagem.sentimento:
        partes.append(f"Sentimento: {mensagem.sentimento}")
    texto = mensagem.texto[:120]
    if texto:
        partes.append(f"Relato: {texto}")
    return " | ".join(partes)


def _calcular_metricas(distrib: Mapping[str, Decimal], referencia: MensagemAnalise) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    """Converte distribuição de emoções em métricas numéricas ponderadas (0-100)."""
    if not distrib and referencia.emocao:
        distrib = {referencia.emocao: Decimal("100")}
    if not distrib:
        return (Decimal("55"),) * 4
    motivacao = Decimal("0")
    felicidade = Decimal("0")
    estresse = Decimal("0")
    energia = Decimal("0")
    for nome, percentual in distrib.items():
        perfil = _buscar_perfil(nome)
        if not perfil:
            continue
        peso = _to_decimal(percentual) / Decimal("100")
        motivacao += Decimal(perfil.motivacao_base) * peso
        felicidade += Decimal(perfil.felicidade_base) * peso
        estresse += Decimal(perfil.estresse_base) * peso
        energia += Decimal(perfil.energia_base) * peso
    return (
        _percentual(motivacao),
        _percentual(felicidade),
        _percentual(estresse),
        _percentual(energia),
    )


def _calcular_intensidade(distrib: Mapping[str, Decimal], energia: Decimal) -> Decimal:
    if not distrib:
        return _percentual(energia)
    pico = max(distrib.values())
    intensidade = (energia + _to_decimal(pico)) / Decimal("2")
    return _percentual(intensidade)


def _estimar_confianca(
    emocao_distribuicao: Mapping[str, Decimal], sentimentos_distribuicao: Mapping[str, Decimal], intensidade: Decimal
) -> Decimal:
    if not emocao_distribuicao:
        base = Decimal("60")
    else:
        base = _to_decimal(max(emocao_distribuicao.values()))
    sent = _to_decimal(max(sentimentos_distribuicao.values())) if sentimentos_distribuicao else Decimal("50")
    media = (base + sent + intensidade) / Decimal("3")
    return _percentual(media)


def _gerar_insights(emocao: str, sentimentos: Mapping[str, Decimal], motivacao: Decimal, estresse: Decimal) -> tuple[str, ...]:
    texto_emocao = emocao.lower()
    insights: list[str] = []
    if texto_emocao in {"feliz", "motivado", "orgulhoso", "grato", "inspirado"}:
        insights.append("Mantenha os hábitos que estão contribuindo para esse momento positivo.")
    elif texto_emocao in {"triste", "cansado"}:
        insights.append("Busque dividir tarefas e converse com seu gestor ou RH para equilibrar a rotina.")
    elif texto_emocao in {"estressado", "irritado", "frustrado", "ansioso"}:
        insights.append("Faça pausas curtas, priorize o que está sob seu controle e compartilhe expectativas com o time.")
    elif texto_emocao in {"apreensivo", "inseguro"}:
        insights.append("Mapeie os riscos e procure apoio em colegas de confiança para tomar decisões com mais segurança.")
    if estresse > Decimal("75"):
        insights.append("Seu nível de estresse está elevado. Experimente técnicas de respiração ou uma breve caminhada.")
    if motivacao < Decimal("45"):
        insights.append("Reflita sobre pequenas metas do dia para recuperar motivação e senso de progresso.")
    if not insights:
        insights.append("Observe seu dia e identifique fatores que podem melhorar seu bem-estar.")
    return tuple(insights[:3])


def _listar_secundarias(distrib: Mapping[str, Decimal], principal: str) -> tuple[tuple[str, Decimal], ...]:
    if not distrib:
        return tuple()
    ordenadas = sorted(distrib.items(), key=lambda item: item[1], reverse=True)
    secundarias = [(nome, valor) for nome, valor in ordenadas if nome != principal][:3]
    return tuple(secundarias)


def _combinar_emocoes(mensagens: Sequence[MensagemAnalise], referencia: MensagemAnalise) -> dict[str, Decimal]:
    acumulado: defaultdict[str, Decimal] = defaultdict(Decimal)
    for mensagem in mensagens:
        if mensagem.emocao_scores:
            for nome, score in mensagem.emocao_scores.items():
                acumulado[nome] += _to_decimal(score)
        elif mensagem.emocao:
            acumulado[mensagem.emocao] += Decimal("100")
    if not acumulado and referencia.emocao:
        acumulado[referencia.emocao] = Decimal("100")
    return _normalizar_distribuicao(acumulado)


def _combinar_sentimentos(mensagens: Sequence[MensagemAnalise], referencia: MensagemAnalise) -> dict[str, Decimal]:
    acumulado: defaultdict[str, Decimal] = defaultdict(Decimal)
    for mensagem in mensagens:
        if mensagem.sentimento_scores:
            for nome, score in mensagem.sentimento_scores.items():
                acumulado[nome] += _to_decimal(score)
        elif mensagem.sentimento:
            acumulado[mensagem.sentimento] += Decimal("100")
    if not acumulado and referencia.sentimento:
        acumulado[referencia.sentimento] = Decimal("100")
    return _normalizar_distribuicao(acumulado)


def _normalizar_distribuicao(acumulado: Mapping[str, Decimal]) -> dict[str, Decimal]:
    total = sum(acumulado.values(), Decimal("0"))
    if not total:
        return {}
    distribuicao: dict[str, Decimal] = {}
    for nome, valor in acumulado.items():
        percentual = (valor / total) * Decimal("100")
        distribuicao[nome] = _percentual(percentual)
    return distribuicao


def _selecionar_principal(distrib: Mapping[str, Decimal]) -> str | None:
    if not distrib:
        return None
    return max(distrib.items(), key=lambda item: item[1])[0]


def _buscar_perfil(nome: str | None):
    if not nome:
        return None
    return _PERFIL_POR_NOME.get(nome.lower())


def _scores_para_decimal(valor: Any) -> dict[str, Decimal]:
    if not isinstance(valor, Mapping):
        return {}
    convertido: dict[str, Decimal] = {}
    for chave, score in valor.items():
        convertido[str(chave)] = _to_decimal(score)
    return convertido


def _media(valores: Sequence[Decimal]) -> Decimal:
    if not valores:
        return Decimal("0")
    total = sum(valores, Decimal("0"))
    media = total / Decimal(len(valores))
    return _percentual(media)


def _percentual(valor: Decimal) -> Decimal:
    if valor < 0:
        valor = Decimal("0")
    if valor > 100:
        valor = Decimal("100")
    return valor.quantize(Decimal("0.01"))


def _parse_datetime(valor: Any) -> datetime:
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, (int, float)):
        return datetime.fromtimestamp(float(valor), tz=timezone.utc)
    if isinstance(valor, str) and valor.strip():
        normalizado = valor.strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalizado)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def _extrair_str(valor: Any) -> str | None:
    if isinstance(valor, str):
        texto = valor.strip()
        return texto or None
    return None


def _to_decimal(valor: Any) -> Decimal:
    if isinstance(valor, Decimal):
        return valor
    try:
        return Decimal(str(valor))
    except Exception:
        return Decimal("0")
_PERFIL_POR_NOME = {perfil.nome.lower(): perfil for perfil in EMOTION_PROFILES}
