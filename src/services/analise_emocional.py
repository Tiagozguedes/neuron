"""Cliente HTTP para a API de análise emocional da Neuron."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Mapping, Sequence

from dotenv import load_dotenv

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover
    requests = None  # type: ignore[assignment]

load_dotenv()  # garante que .env seja carregado ao importar o módulo

DEFAULT_BASE_URL = "https://neuron-ai-v1yi.onrender.com"
DEFAULT_ANALISE_PATH = "/conversas/analisar"
DEFAULT_TIMEOUT = 15

_SCORE_KEY_MAP = {
    "joy": "alegria",
    "happiness": "felicidade",
    "positive": "positivo",
    "negativo": "negativo",
    "negative": "negativo",
    "alegria": "alegria",
    "felicidade": "felicidade",
    "positivo": "positivo",
    "stress": "estresse",
    "estresse": "estresse",
}


class AnaliseIAError(RuntimeError):
    """Erro amigável emitido quando a API de IA não responde como esperado."""


@dataclass(slots=True)
class MensagemAnalise:
    """Representa cada mensagem retornada pela IA normalizada para português."""

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
    probabilidade: Decimal
    modelo_versao: str
    data_analise: datetime
    emocao_nome: str
    emocao_id: int | None
    intensidade: Decimal
    insights: tuple[str, ...]


@dataclass(slots=True)
class ApiConfig:
    """Dados provenientes das variáveis de ambiente."""

    url: str
    timeout: int
    api_key: str | None


def analisar_conversa(mensagens: Sequence[Mapping[str, Any]]) -> EmotionReport:
    """Envia uma conversa (lista de mensagens) para a IA e retorna o relatório normalizado."""
    if requests is None:  # pragma: no cover - proteção para ambientes sem dependências
        raise RuntimeError("Dependência 'requests' ausente. Instale-a com 'pip install requests'.")
    payload = _build_payload(mensagens)
    config = _api_config()
    resposta = _executar_chamada(config, payload)
    return _interpretar_resposta(resposta)


def analisar_texto(texto: str, usuario_id: int | None = None) -> EmotionReport:
    """Compatibilidade retroativa: envia apenas um texto para análise."""
    _ = usuario_id  # mantido para não quebrar chamadas legadas
    mensagem = {"texto": texto, "timestamp": datetime.now(timezone.utc)}
    return analisar_conversa([mensagem])


def _build_payload(mensagens: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not mensagens:
        raise ValueError("Forneça pelo menos uma mensagem para a análise emocional.")
    corpo: list[dict[str, Any]] = []
    for item in mensagens:
        texto = str(item.get("texto") or item.get("text") or "").strip()
        if not texto:
            raise ValueError("Cada mensagem enviada à IA precisa ter o campo 'texto'.")
        timestamp = _normalizar_timestamp(item.get("timestamp"))
        corpo.append({"texto": texto, "timestamp": timestamp})
    return {"mensagens": corpo}


def _normalizar_timestamp(valor: Any) -> str | None:
    if valor is None or valor == "":
        return None
    if isinstance(valor, datetime):
        return valor.astimezone(timezone.utc).isoformat()
    return str(valor)


def _api_config() -> ApiConfig:
    base_url = (os.getenv("NEURON_API_BASE_URL") or DEFAULT_BASE_URL).strip()
    if not base_url:
        base_url = DEFAULT_BASE_URL
    base_url = base_url.rstrip("/")

    analise_path = (os.getenv("NEURON_API_ANALISE_PATH") or DEFAULT_ANALISE_PATH).strip()
    analise_path = analise_path or DEFAULT_ANALISE_PATH
    analise_path = analise_path if analise_path.startswith("/") else f"/{analise_path}"

    timeout_raw = os.getenv("NEURON_API_TIMEOUT") or str(DEFAULT_TIMEOUT)
    try:
        timeout = max(1, int(timeout_raw))
    except ValueError:
        timeout = DEFAULT_TIMEOUT

    api_key = (os.getenv("NEURON_API_KEY") or "").strip() or None
    return ApiConfig(url=f"{base_url}{analise_path}", timeout=timeout, api_key=api_key)


def _build_headers(api_key: str | None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers


def _executar_chamada(config: ApiConfig, payload: Mapping[str, Any]) -> Mapping[str, Any]:
    headers = _build_headers(config.api_key)
    try:
        resposta = requests.post(  # type: ignore[call-arg]
            config.url,
            json=payload,
            headers=headers,
            timeout=config.timeout,
        )
        resposta.raise_for_status()
    except requests.exceptions.Timeout as exc:  # pragma: no cover - depende da rede
        raise AnaliseIAError("A análise demorou demais. Tente novamente em alguns minutos.") from exc
    except requests.exceptions.ConnectionError as exc:  # pragma: no cover
        raise AnaliseIAError(
            "Não foi possível conectar à API de IA. Verifique sua internet ou se o serviço está no ar.",
        ) from exc
    except requests.exceptions.HTTPError as exc:  # pragma: no cover
        status = getattr(getattr(exc, "response", None), "status_code", "desconhecido")
        detalhe = _extrair_mensagem_erro(getattr(exc, "response", None))
        raise AnaliseIAError(f"A API de IA retornou {status}: {detalhe}") from exc
    except requests.exceptions.RequestException as exc:  # pragma: no cover
        raise AnaliseIAError(f"Erro inesperado ao chamar a API de IA: {exc}") from exc

    try:
        data = resposta.json()
    except ValueError as exc:  # pragma: no cover
        raise AnaliseIAError(
            "A resposta da API não está no formato esperado. Entre em contato com o time Neuron.",
        ) from exc
    if not isinstance(data, Mapping):
        raise AnaliseIAError(
            "A resposta da API não está no formato esperado. Entre em contato com o time Neuron.",
        )
    return data


def _extrair_mensagem_erro(resposta: Any) -> str:
    if resposta is None:
        return "sem detalhes retornados"
    try:
        corpo = resposta.json()
    except Exception:  # pragma: no cover - apenas fallback
        corpo = None
    if isinstance(corpo, Mapping):
        for chave in ("erro", "mensagem", "error", "message", "detail"):
            valor = corpo.get(chave)
            if isinstance(valor, str) and valor.strip():
                return valor.strip()
    texto = getattr(resposta, "text", "") or ""
    return texto.strip() or "sem mensagem adicional"


def _interpretar_resposta(payload: Mapping[str, Any]) -> EmotionReport:
    mensagens = tuple(_normalizar_mensagem(item) for item in _coletar_mensagens(payload))
    resumo_raw = payload.get("resumo") or payload.get("summary")
    resumo_detalhado = resumo_raw if isinstance(resumo_raw, Mapping) else None
    resumo = _resumo_para_texto(resumo_raw, mensagens)
    insights = _insights_from_resumo(resumo_detalhado)

    referencia = mensagens[0] if mensagens else None
    sentimento_scores = referencia.sentimento_scores if referencia else {}
    emocao_scores = referencia.emocao_scores if referencia else {}

    motivacao = _percentual(_obter_score(sentimento_scores, ("positivo", "positive")))
    felicidade = _percentual(_obter_score(emocao_scores, ("felicidade", "alegria", "joy", "happiness")))
    if felicidade == Decimal("0"):
        felicidade = motivacao
    estresse = _percentual(_obter_score(sentimento_scores, ("estresse", "stress", "negativo", "negative")))
    saude_mental = _media([motivacao, felicidade])
    intensidade = _percentual(_maior_score(emocao_scores))
    probabilidade = max(motivacao, felicidade, estresse, saude_mental, intensidade, Decimal("0"))

    emocao_nome = referencia.emocao if referencia else ""
    modelo = str(
        payload.get("modelo")
        or payload.get("modelo_versao")
        or payload.get("model")
        or payload.get("modelVersion")
        or "Neuron-AI"
    )
    data_analise = (
        referencia.timestamp
        or referencia.data
        if referencia
        else _parse_datetime(payload.get("data") or payload.get("timestamp"))
    )

    return EmotionReport(
        mensagens=mensagens,
        resumo=resumo,
        resumo_detalhado=resumo_detalhado,
        motivacao=motivacao,
        felicidade=felicidade,
        estresse=estresse,
        saude_mental=saude_mental,
        probabilidade=probabilidade,
        modelo_versao=modelo,
        data_analise=data_analise,
        emocao_nome=emocao_nome or "",
        emocao_id=None,
        intensidade=intensidade,
        insights=insights,
    )


def _coletar_mensagens(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    bruto = payload.get("mensagens")
    if not isinstance(bruto, Sequence):
        bruto = payload.get("messages") or ()
    return [item for item in bruto if isinstance(item, Mapping)]


def _normalizar_mensagem(item: Mapping[str, Any]) -> MensagemAnalise:
    texto = str(item.get("texto") or item.get("text") or "").strip()
    timestamp = _parse_datetime(item.get("timestamp"))
    data_relato = _parse_datetime(item.get("data") or item.get("date"))
    emocao = _normalizar_string(item.get("emocao") or item.get("emotion"))
    sentimento = _normalizar_string(item.get("sentimento") or item.get("sentiment"))
    emocao_scores = _normalizar_scores(item.get("emocao_scores") or item.get("emotion_scores"))
    sentimento_scores = _normalizar_scores(item.get("sentimento_scores") or item.get("sentiment_scores"))
    sentimento_fonte = _normalizar_string(item.get("sentimento_fonte") or item.get("sentiment_source"))
    return MensagemAnalise(
        texto=texto,
        timestamp=timestamp,
        data=data_relato,
        emocao=emocao,
        sentimento=sentimento,
        emocao_scores=emocao_scores,
        sentimento_scores=sentimento_scores,
        sentimento_fonte=sentimento_fonte,
    )


def _normalizar_scores(valor: Any) -> dict[str, Decimal]:
    if not isinstance(valor, Mapping):
        return {}
    normalizado: dict[str, Decimal] = {}
    for chave, score in valor.items():
        chave_norm = _normalizar_nome_score(str(chave))
        normalizado[chave_norm] = _to_decimal(score)
    return normalizado


def _normalizar_nome_score(chave: str) -> str:
    chave_limpa = chave.strip().lower().replace(" ", "_").replace("-", "_")
    if chave_limpa.endswith("_score"):
        chave_limpa = chave_limpa[: -len("_score")]
    return _SCORE_KEY_MAP.get(chave_limpa, chave_limpa)


def _normalizar_string(valor: Any) -> str | None:
    if isinstance(valor, str):
        texto = valor.strip()
        return texto or None
    return None


def _resumo_para_texto(resumo_raw: Any, mensagens: Sequence[MensagemAnalise]) -> str:
    if isinstance(resumo_raw, str) and resumo_raw.strip():
        return resumo_raw.strip()
    if isinstance(resumo_raw, Mapping):
        texto = resumo_raw.get("texto") or resumo_raw.get("text")
        if isinstance(texto, str) and texto.strip():
            return texto.strip()
    if not mensagens:
        return ""
    partes: list[str] = []
    if mensagens[0].emocao:
        partes.append(f"Emoção: {mensagens[0].emocao}")
    if mensagens[0].sentimento:
        partes.append(f"Sentimento: {mensagens[0].sentimento}")
    return " | ".join(partes)


def _obter_score(scores: Mapping[str, Decimal], aliases: Sequence[str]) -> Decimal:
    for alias in aliases:
        chave = _normalizar_nome_score(alias)
        if chave in scores:
            return scores[chave]
    return Decimal("0")


def _to_decimal(valor: Any, default: str = "0") -> Decimal:
    if valor is None:
        valor = default
    if isinstance(valor, Decimal):
        return valor
    try:
        return Decimal(str(valor))
    except Exception:
        return Decimal(default)


def _media(valores: Sequence[Decimal]) -> Decimal:
    validos = [valor for valor in valores if isinstance(valor, Decimal)]
    if not validos:
        return Decimal("0")
    return sum(validos) / Decimal(len(validos))


def _maior_score(scores: Mapping[str, Decimal]) -> Decimal:
    if not scores:
        return Decimal("0")
    return max(scores.values())


def _percentual(valor: Decimal) -> Decimal:
    if valor <= 1:
        valor *= 100
    if valor < 0:
        return Decimal("0")
    if valor > 100:
        return Decimal("100")
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
