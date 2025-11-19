"""Regras heurísticas de análise emocional executadas localmente."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Sequence

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _normalizar(texto: str) -> str:
    # Remove acentos e converte para minúsculas para facilitar comparações lexicais.
    decomposed = unicodedata.normalize("NFD", texto.lower())
    sem_acentos = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return sem_acentos


def _normalizar_lista(palavras: Iterable[str]) -> tuple[str, ...]:
    retorno: list[str] = []
    for palavra in palavras:
        normalizada = _normalizar(palavra)
        if normalizada:
            retorno.append(normalizada)
    return tuple(retorno)


@dataclass(frozen=True)
class EmotionProfile:
    """Agrupa palavras-chave, sentimentos e pesos para cada emoção."""

    nome: str
    sentimento: str
    palavras: tuple[str, ...]
    expressoes: tuple[str, ...] = ()
    peso_palavra: float = 1.0
    peso_expressao: float = 1.5
    pesos_personalizados: Mapping[str, float] = field(default_factory=dict)
    felicidade_base: int = 55
    motivacao_base: int = 55
    estresse_base: int = 45
    energia_base: int = 55

    def __post_init__(self) -> None:
        object.__setattr__(self, "palavras", _normalizar_lista(self.palavras))
        object.__setattr__(self, "expressoes", tuple(_normalizar(frase) for frase in self.expressoes))
        pesos_norm: dict[str, float] = {}
        for chave, peso in (self.pesos_personalizados or {}).items():
            normalizada = _normalizar(chave)
            if normalizada:
                pesos_norm[normalizada] = peso
        object.__setattr__(self, "pesos_personalizados", pesos_norm)

    def peso_para_palavra(self, token: str) -> float:
        return self.pesos_personalizados.get(token, self.peso_palavra)


EMOTION_PROFILES: tuple[EmotionProfile, ...] = (
    EmotionProfile(
        nome="Feliz",
        sentimento="positivo",
        palavras=(
            "feliz",
            "felicidade",
            "contente",
            "radiante",
            "alegre",
            "satisfeito",
            "satisfeita",
            "grato",
            "grata",
            "agradecido",
            "positivo",
            "motivador",
            "animado",
            "animada",
            "entusiasmado",
            "entusiasmada",
        ),
        expressoes=("me sinto bem", "estou bem", "muito feliz", "me sinto otimo", "dia excelente"),
        felicidade_base=92,
        motivacao_base=85,
        estresse_base=20,
        energia_base=80,
    ),
    EmotionProfile(
        nome="Esperançoso",
        sentimento="positivo",
        palavras=("esperanca", "esperancoso", "confiante", "confiante", "acreditando", "otimista"),
        expressoes=("vejo melhorias", "acredito que vai dar certo", "estou confiante"),
        felicidade_base=85,
        motivacao_base=80,
        estresse_base=30,
        energia_base=75,
    ),
    EmotionProfile(
        nome="Sereno",
        sentimento="positivo",
        palavras=("calmo", "calma", "sereno", "relaxado", "tranquilo", "paz", "equilibrado"),
        expressoes=("mente tranquila", "em paz", "manter a calma"),
        felicidade_base=78,
        motivacao_base=62,
        estresse_base=25,
        energia_base=65,
    ),
    EmotionProfile(
        nome="Motivado",
        sentimento="positivo",
        palavras=("motivado", "motivado", "determinado", "focado", "produtivo", "engajado", "inspirado"),
        expressoes=("cheio de energia", "pronto para o desafio", "querendo entregar mais"),
        felicidade_base=80,
        motivacao_base=90,
        estresse_base=30,
        energia_base=82,
    ),
    EmotionProfile(
        nome="Orgulhoso",
        sentimento="positivo",
        palavras=("orgulho", "orgulhoso", "orgulhosa", "reconhecimento", "conquista"),
        expressoes=("fui reconhecido", "meta atingida", "resultado excelente"),
        felicidade_base=88,
        motivacao_base=82,
        estresse_base=28,
        energia_base=76,
    ),
    EmotionProfile(
        nome="Grato",
        sentimento="positivo",
        palavras=("grato", "grata", "agradecido", "agradecida", "abençoado", "valorizado"),
        expressoes=("agradeco", "sou grato"),
        felicidade_base=86,
        motivacao_base=74,
        estresse_base=25,
        energia_base=70,
    ),
    EmotionProfile(
        nome="Triste",
        sentimento="negativo",
        palavras=(
            "triste",
            "tristeza",
            "abatido",
            "desanimado",
            "chorando",
            "deprimido",
            "mal",
            "pessimo",
            "pesado",
        ),
        expressoes=("nao estou bem", "dia dificil", "bateu tristeza", "sem vontade"),
        peso_palavra=1.2,
        felicidade_base=25,
        motivacao_base=35,
        estresse_base=65,
        energia_base=30,
    ),
    EmotionProfile(
        nome="Cansado",
        sentimento="negativo",
        palavras=("cansado", "cansada", "exausto", "exausta", "fadiga", "sono", "desgastado", "esgotado"),
        expressoes=("sem energia", "preciso descansar", "trabalhei demais"),
        peso_palavra=1.3,
        felicidade_base=35,
        motivacao_base=40,
        estresse_base=70,
        energia_base=20,
    ),
    EmotionProfile(
        nome="Estressado",
        sentimento="negativo",
        palavras=("estresse", "estressado", "estressada", "pressao", "correria", "tensao", "sobrecarregado"),
        expressoes=("muito estresse", "prazos apertados", "sem descanso"),
        peso_palavra=1.4,
        felicidade_base=30,
        motivacao_base=45,
        estresse_base=85,
        energia_base=25,
    ),
    EmotionProfile(
        nome="Irritado",
        sentimento="negativo",
        palavras=("raiva", "irritado", "irritada", "irritante", "bravo", "brava", "furioso", "furiosa", "odio"),
        expressoes=("perdi a paciencia", "explodi", "sem paciencia"),
        peso_palavra=1.4,
        felicidade_base=28,
        motivacao_base=38,
        estresse_base=88,
        energia_base=35,
    ),
    EmotionProfile(
        nome="Ansioso",
        sentimento="negativo",
        palavras=("ansioso", "ansiosa", "inquieto", "preocupado", "preocupada", "apreensivo", "nervoso"),
        expressoes=("ansiedade alta", "borboletas no estomago", "muita pressa"),
        felicidade_base=40,
        motivacao_base=50,
        estresse_base=80,
        energia_base=55,
    ),
    EmotionProfile(
        nome="Apreensivo",
        sentimento="negativo",
        palavras=("medo", "temor", "receio", "inseguro", "insegura", "duvida", "desconfiado"),
        expressoes=("nao sei o que vai ocorrer", "preocupacoes futuras"),
        felicidade_base=42,
        motivacao_base=48,
        estresse_base=78,
        energia_base=52,
    ),
    EmotionProfile(
        nome="Frustrado",
        sentimento="negativo",
        palavras=("frustrado", "frustrada", "desapontado", "decepcionado", "insucesso", "travei", "bloqueado"),
        expressoes=("resultado abaixo", "nada funciona", "nada da certo"),
        peso_palavra=1.2,
        felicidade_base=33,
        motivacao_base=40,
        estresse_base=82,
        energia_base=45,
    ),
    EmotionProfile(
        nome="Aliviado",
        sentimento="positivo",
        palavras=("aliviado", "aliviada", "ufa", "resolvido", "respiro", "acalmei"),
        expressoes=("tirou um peso", "menos preocupado agora"),
        felicidade_base=70,
        motivacao_base=60,
        estresse_base=35,
        energia_base=60,
    ),
    EmotionProfile(
        nome="Inspirado",
        sentimento="positivo",
        palavras=("inspirado", "inspirada", "criativo", "criativa", "ideias", "inovador", "motivador"),
        expressoes=("tive uma ideia", "momento criativo"),
        felicidade_base=82,
        motivacao_base=88,
        estresse_base=32,
        energia_base=78,
    ),
)

_PROFILE_LOOKUP = {perfil.nome.lower(): perfil for perfil in EMOTION_PROFILES}

_SENTIMENTO_KEYWORDS = {
    "positivo": (
        "feliz",
        "otimo",
        "bom",
        "maravilhoso",
        "animado",
        "satisfeito",
        "grato",
        "leve",
        "tranquilo",
        "sereno",
        "motivado",
        "confiante",
        "esperanca",
        "firme",
        "animador",
    ),
    "negativo": (
        "triste",
        "mal",
        "raiva",
        "irritado",
        "frustrado",
        "cansado",
        "exausto",
        "deprimido",
        "ansioso",
        "preocupado",
        "angustiado",
        "estressado",
        "horrivel",
        "pessimo",
        "ruim",
        "sobrecarregado",
        "desanimado",
    ),
}

_SENTIMENTO_KEYWORDS_NORMALIZADOS = {
    rotulo: set(_normalizar_lista(palavras)) for rotulo, palavras in _SENTIMENTO_KEYWORDS.items()
}


def analisar_texto_local(texto: str) -> Dict[str, object]:
    """Aplica a heurística local baseada em perfis e pesos configuráveis."""
    texto = texto or ""
    normalizado = _normalizar(texto)
    tokens = _tokenizar(normalizado)
    contagem_tokens = Counter(tokens)
    emocao_scores = _calcular_scores_emocionais(contagem_tokens, normalizado)
    if not emocao_scores:
        emocao = "Neutro"
    else:
        emocao = max(emocao_scores, key=emocao_scores.get)
    sentimento_scores = _consolidar_sentimentos(tokens, emocao_scores)
    sentimento = _selecionar_principal(sentimento_scores) or "neutro"
    return {
        "emocao": emocao,
        "sentimento": sentimento,
        "emocao_scores": emocao_scores,
        "sentimento_scores": sentimento_scores,
    }


def _calcular_scores_emocionais(contagem_tokens: Counter[str], texto_normalizado: str) -> Dict[str, float]:
    """Soma pesos de palavras e expressões para cada perfil conhecido."""
    scores: dict[str, float] = {}
    for perfil in EMOTION_PROFILES:
        score = 0.0
        for token, ocorrencias in contagem_tokens.items():
            if token in perfil.palavras:
                score += perfil.peso_para_palavra(token) * ocorrencias
        for expressao in perfil.expressoes:
            if expressao and expressao in texto_normalizado:
                score += perfil.peso_expressao
        if score > 0:
            scores[perfil.nome] = round(score, 4)
    return _normalizar_scores(scores)


def _consolidar_sentimentos(tokens: Sequence[str], emocao_scores: Mapping[str, float]) -> Dict[str, float]:
    """Combina sentimento detectado direto do texto + contribuição das emoções."""
    contagem: Counter[str] = Counter()
    for token in tokens:
        for rotulo, palavras in _SENTIMENTO_KEYWORDS_NORMALIZADOS.items():
            if token in palavras:
                contagem[rotulo] += 1
    for emocao, percentual in emocao_scores.items():
        perfil = _PROFILE_LOOKUP.get(emocao.lower())
        if not perfil or percentual <= 0:
            continue
        contagem[perfil.sentimento] += percentual / 25  # peso moderado da emoção na decisão final.
    return _normalizar_counter(contagem)


def _selecionar_principal(scores: Mapping[str, float]) -> str | None:
    if not scores:
        return None
    return max(scores.items(), key=lambda item: item[1])[0]


def _normalizar_scores(scores: Mapping[str, float]) -> Dict[str, float]:
    total = sum(scores.values())
    if not total:
        return {}
    return {chave: round((valor / total) * 100, 2) for chave, valor in scores.items()}


def _normalizar_counter(contagem: Counter[str]) -> Dict[str, float]:
    total = sum(contagem.values())
    if not total:
        return {}
    return {chave: round((valor / total) * 100, 2) for chave, valor in contagem.items()}


def _tokenizar(texto: str) -> tuple[str, ...]:
    if not texto:
        return tuple()
    return tuple(_TOKEN_RE.findall(texto))
