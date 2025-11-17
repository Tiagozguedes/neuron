"""Cliente HTTP para a API de análise emocional da Neuron."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Mapping, Sequence

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover
    requests = None  # type: ignore[assignment]

DEFAULT_ENDPOINT = "https://neuron-ai-v1yi.onrender.com/api/v1/analises-emocionais"


@dataclass(slots=True)
class EmotionReport:
    """Representa o retorno consolidado da IA."""

    motivacao: Decimal
    felicidade: Decimal
    estresse: Decimal
    saude_mental: Decimal
    probabilidade: Decimal
    modelo_versao: str
    data_analise: datetime
    resumo: str
    emocao_nome: str
    emocao_id: int | None
    intensidade: Decimal
    insights: tuple[str, ...]


def analisar_texto(texto: str, usuario_id: int | None = None) -> EmotionReport:
    """Envia o relato do colaborador para a API externa e devolve o relatório estruturado."""
    # Função principal consumida pelo CLI de check-in; encapsula validações e parsing do JSON.
    if not texto.strip():
        raise ValueError("O texto para análise não pode estar vazio.")
    if requests is None:  # pragma: no cover
        raise RuntimeError("Dependência 'requests' ausente. Instale com 'pip install requests'.")
    endpoint = _endpoint()
    headers = _build_headers()
    payload = _build_payload(texto, usuario_id)
    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=_timeout())  # type: ignore[call-arg]
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - depende da rede
        detalhe = ""
        resposta_http = getattr(exc, "response", None)
        if resposta_http is not None and hasattr(resposta_http, "status_code"):
            detalhe = f"{resposta_http.status_code} {getattr(resposta_http, 'text', '')}".strip()
        mensagem = detalhe or str(exc)
        raise RuntimeError(f"Falha ao chamar a API Neuron-AI: {mensagem}") from exc
    try:
        data = response.json()
    except ValueError as exc:  # pragma: no cover
        raise RuntimeError("A API da Neuron retornou uma resposta inválida (JSON esperado).") from exc
    if not isinstance(data, Mapping):
        raise RuntimeError("Formato inesperado retornado pela IA (objeto JSON era esperado).")
    return _parse_payload(data)


def _build_headers() -> dict[str, str]:
    # Monta cabeçalhos obrigatórios (JSON + Bearer token opcional).
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("NEURON_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _timeout() -> float:
    # Permite ajustar o timeout via NEURON_API_TIMEOUT.
    try:
        return float(os.getenv("NEURON_API_TIMEOUT", "15"))
    except ValueError:
        return 15.0


def _endpoint() -> str:
    # Garante endpoint configurável sem barras duplicadas.
    return os.getenv("NEURON_API_ENDPOINT", DEFAULT_ENDPOINT).rstrip("/")


def _build_payload(texto: str, usuario_id: int | None) -> dict[str, Any]:
    # Monta o corpo aceito pela API pública (lista de mensagens com timestamp ISO).
    mensagem = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "texto": texto,
    }
    if usuario_id is not None:
        mensagem["usuarioId"] = usuario_id
    return {"mensagens": [mensagem]}


def _parse_payload(data: Mapping[str, Any]) -> EmotionReport:
    if isinstance(data.get("mensagens"), Sequence):
        try:
            return _parse_render_payload(data)
        except Exception:
            pass
    return _parse_legacy_payload(data)


def _parse_render_payload(data: Mapping[str, Any]) -> EmotionReport:
    # Converte o contrato novo da API (mensagens/resumo) para nosso relatório interno.
    mensagens = data.get("mensagens")
    mensagem = mensagens[0] if isinstance(mensagens, Sequence) and mensagens else {}
    mensagem = mensagem if isinstance(mensagem, Mapping) else {}
    sentimento_scores = _maybe_mapping(mensagem.get("sentimento_scores"))
    emocao_scores = _maybe_mapping(mensagem.get("emocao_scores"))

    positivo = _percentual(_extrair_score(sentimento_scores, "positivo", "positive"))
    negativo = _percentual(_extrair_score(sentimento_scores, "negativo", "negative"))
    felicidade = _percentual(_extrair_score(emocao_scores, "alegria", "felicidade", "joy", "happiness"))
    if felicidade == Decimal("0"):
        felicidade = positivo
    motivacao = positivo
    estresse = negativo
    saude_mental = _media([motivacao, felicidade])
    intensidade = _percentual(_maior_score(emocao_scores))
    probabilidade = max(motivacao, felicidade, estresse, saude_mental, intensidade, Decimal("0"))

    modelo = str(data.get("modelo") or data.get("modeloVersao") or "neuron-ai@render")
    data_analise = _parse_datetime(mensagem.get("timestamp") or mensagem.get("data"))
    emocao_nome = str(mensagem.get("emocao") or mensagem.get("sentimento") or "").strip()
    resumo_partes = []
    if emocao_nome:
        resumo_partes.append(f"Emoção: {emocao_nome}")
    sentimento_nome = str(mensagem.get("sentimento") or "").strip()
    if sentimento_nome:
        resumo_partes.append(f"Sentimento: {sentimento_nome}")
    resumo = " | ".join(resumo_partes)
    insights = _insights_from_resumo(_maybe_mapping(data.get("resumo")))

    return EmotionReport(
        motivacao=motivacao,
        felicidade=felicidade,
        estresse=estresse,
        saude_mental=saude_mental,
        probabilidade=probabilidade,
        modelo_versao=modelo,
        data_analise=data_analise,
        resumo=resumo,
        emocao_nome=emocao_nome,
        emocao_id=None,
        intensidade=intensidade,
        insights=insights,
    )


def _parse_legacy_payload(data: Mapping[str, Any]) -> EmotionReport:
    # Faz a leitura resiliente do JSON, considerando chaves alternativas que a API possa enviar.
    metricas = _maybe_mapping(data.get("metricas") or data.get("scores"))
    motivacao = _to_decimal(_buscar(metricas, data, "motivacao", "motivation"))
    felicidade = _to_decimal(_buscar(metricas, data, "felicidade", "happiness", "alegria"))
    estresse = _to_decimal(_buscar(metricas, data, "estresse", "stress"))
    saude_mental_bruta = _buscar(metricas, data, "saudeMental", "saude_mental", "mentalHealth", "mental_health")
    saude_mental = _to_decimal(saude_mental_bruta) if saude_mental_bruta is not None else _media(
        [motivacao, felicidade]
    )
    probabilidade = _normalizar_probabilidade(_to_decimal(_buscar(data, "probabilidade", "confidence", "score")))
    modelo = str(_buscar(data, "modeloVersao", "modelo_versao", "modelVersion", "model_version") or "desconhecido")
    data_analise = _parse_datetime(
        _buscar(data, "dataAnalise", "dt_analise", "analysisDate", "timestamp", "createdAt", "data")
    )
    resumo = str(_buscar(data, "resumo", "relatorio", "summary", "report") or "").strip()
    emocao_nome, emocao_id, intensidade = _parse_emocao(
        _buscar(data, "emocao", "emocaoPrincipal", "dominantEmotion", "emotion")
    )
    insights = _parse_insights(_buscar(data, "insights", "recomendacoes", "recommendations"))

    return EmotionReport(
        motivacao=motivacao,
        felicidade=felicidade,
        estresse=estresse,
        saude_mental=saude_mental,
        probabilidade=probabilidade,
        modelo_versao=modelo,
        data_analise=data_analise,
        resumo=resumo,
        emocao_nome=emocao_nome,
        emocao_id=emocao_id,
        intensidade=intensidade,
        insights=insights,
    )


def _maybe_mapping(value: Any) -> Mapping[str, Any] | None:
    # Ajuda na validação antes de tratar campos como dicionário.
    return value if isinstance(value, Mapping) else None


def _buscar(*args: Any) -> Any:
    # Procura uma sequência de chaves em múltiplas fontes (ex.: payload raiz e bloco de métricas).
    if not args:
        return None
    fontes = [arg for arg in args if isinstance(arg, Mapping)]
    chaves = [arg for arg in args if isinstance(arg, str)]
    if not chaves:
        return args[0] if args else None
    for fonte in fontes:
        for chave in chaves:
            if chave in fonte:
                return fonte[chave]
    return None


def _to_decimal(value: Any, default: str = "0") -> Decimal:
    # Converte valores vindos da API (número/string) em Decimal padronizado.
    if value is None:
        value = default
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal(default)


def _media(valores: Sequence[Decimal]) -> Decimal:
    # Calcula média protegendo contra listas vazias.
    valores_validos = [valor for valor in valores if isinstance(valor, Decimal)]
    if not valores_validos:
        return Decimal("0")
    soma = sum(valores_validos)
    return soma / Decimal(len(valores_validos))


def _normalizar_probabilidade(valor: Decimal) -> Decimal:
    """Garante que o valor esteja na escala 0-100 e converte se vier de 0-1."""
    # Algumas APIs retornam confiança entre 0 e 1; outras entre 0 e 100.
    if valor <= 1:
        valor *= 100
    if valor < 0:
        return Decimal("0")
    if valor > 100:
        return Decimal("100")
    return valor.quantize(Decimal("0.01"))


def _parse_datetime(value: Any) -> datetime:
    # Aceita datetime pronto, timestamp numérico ou string ISO.
    if isinstance(value, datetime):
        return value
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str) and value.strip():
        normalizado = value.strip().replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalizado)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def _parse_emocao(value: Any) -> tuple[str, int | None, Decimal]:
    # Extrai nome/ID/intensidade da emoção predominante retornada pela IA.
    if value is None:
        return ("", None, Decimal("0"))
    if isinstance(value, str):
        return (value.strip(), None, Decimal("0"))
    if isinstance(value, Mapping):
        nome = str(
            value.get("nome")
            or value.get("name")
            or value.get("label")
            or value.get("descricao")
            or value.get("description")
            or ""
        ).strip()
        emocao_id = value.get("id") or value.get("emotionId") or value.get("idEmocao")
        intensidade = _to_decimal(value.get("intensidade") or value.get("intensity") or value.get("score"), "0")
        return (nome, int(emocao_id) if emocao_id is not None else None, intensidade)
    return ("", None, Decimal("0"))


def _parse_insights(value: Any) -> tuple[str, ...]:
    # Normaliza recomendações/insights para uma tupla de strings.
    if not value:
        return tuple()
    if isinstance(value, str):
        return tuple(linha.strip() for linha in value.split("\n") if linha.strip())
    if isinstance(value, Sequence):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return tuple()


def _extrair_score(scores: Mapping[str, Any] | None, *chaves: str) -> Decimal:
    if not scores:
        return Decimal("0")
    for chave in chaves:
        if chave in scores:
            return _to_decimal(scores[chave])
    return Decimal("0")


def _maior_score(scores: Mapping[str, Any] | None) -> Decimal:
    if not scores:
        return Decimal("0")
    valores = [_to_decimal(valor) for valor in scores.values()]
    return max(valores) if valores else Decimal("0")


def _percentual(valor: Decimal) -> Decimal:
    return _normalizar_probabilidade(valor)


def _insights_from_resumo(resumo: Mapping[str, Any] | None) -> tuple[str, ...]:
    if not resumo:
        return tuple()
    insights: list[str] = []
    for chave, bloco in resumo.items():
        if not isinstance(bloco, Mapping) or not bloco:
            continue
        try:
            item = max(bloco.items(), key=lambda par: _to_decimal(par[1]))
        except ValueError:
            continue
        nome_bloco = chave.replace("_", " ").title()
        insights.append(f"{nome_bloco}: {item[0]} ({item[1]})")
    return tuple(insights)
