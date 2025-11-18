"""Fluxo de check-in emocional integrado com o modelo de IA."""

from __future__ import annotations

from datetime import datetime, timezone

from connect.connect import run_execute, run_query
from db_utils import proximo_id, registro_existe
from services.analise_emocional import EmotionReport, analisar_conversa
from utils import (
    OperacaoCancelada,
    deseja_voltar,
    limpar_tela,
    pausar,
    solicitar_confirmacao,
    solicitar_inteiro,
    solicitar_texto,
)


def realizar_checkin_emocional() -> None:
    # Orquestra o fluxo completo: captura usuário, envia texto à IA e persiste tudo no Oracle.
    """Permite que o colaborador descreva seu momento e registre a análise retornada pela IA."""
    try:
        limpar_tela()
        print("=== Check-in emocional com IA Neuron ===\n")
        print("Digite 'voltar' a qualquer momento para cancelar e retornar ao menu.\n")
        usuario_id = solicitar_inteiro("ID do colaborador")
        if not registro_existe("T_NRON_USUARIO", "ID_USUARIO", usuario_id):
            print("Usuário não encontrado.")
            return
        texto = _coletar_relato()
        if not texto:
            print("Nenhum relato informado, operação cancelada.")
            return
        print("\nEnviando relato para a API Neuron...")
        mensagens = [
            {
                "texto": texto,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]
        relatorio = analisar_conversa(mensagens)
        _mostrar_relatorio(relatorio)
        if not solicitar_confirmacao("\nDeseja salvar este check-in no banco de dados?"):
            print("Check-in descartado pelo usuário.")
            return
        emocao_id = _resolver_emocao_id(relatorio)
        if not emocao_id:
            print("Não foi possível associar a emoção identificada a uma categoria válida. Operação cancelada.")
            return
        registro_id = _criar_registro_emocao(emocao_id, relatorio)
        resposta_id = _persistir_resposta(usuario_id, texto, relatorio, registro_id)
        print(f"\nCheck-in registrado! Resposta #{resposta_id} vinculada ao registro emocional #{registro_id}.")
    except OperacaoCancelada:
        print("Operação cancelada pelo usuário.")
    except Exception as exc:
        print(f"Erro ao processar o check-in: {exc}")
    finally:
        pausar()


def _coletar_relato() -> str:
    # Lê múltiplas linhas até o usuário enviar Enter vazio e devolve o texto consolidado.
    print(
        "\nConte como está seu momento (use frases completas). "
        "Pressione Enter em branco para finalizar ou digite 'voltar' para cancelar.\n",
    )
    linhas: list[str] = []
    while True:
        linha = input("> ")
        if deseja_voltar(linha):
            raise OperacaoCancelada()
        if not linha.strip():
            break
        linhas.append(linha.strip())
    return "\n".join(linhas).strip()


def _mostrar_relatorio(relatorio: EmotionReport) -> None:
    # Exibe métricas retornadas pela IA para que o colaborador aprove ou não o salvamento.
    print("\n--- Relatório da IA ---")
    mensagem_principal = relatorio.mensagens[0] if relatorio.mensagens else None
    emocao = mensagem_principal.emocao if mensagem_principal else relatorio.emocao_nome
    sentimento = mensagem_principal.sentimento if mensagem_principal else None
    print(f"Emoção predominante: {emocao or 'indefinida'}")
    if sentimento:
        print(f"Sentimento predominante: {sentimento}")
    print(f"Intensidade: {relatorio.intensidade}")
    print(f"Motivação: {relatorio.motivacao}")
    print(f"Felicidade: {relatorio.felicidade}")
    print(f"Estresse: {relatorio.estresse}")
    print(f"Saúde mental: {relatorio.saude_mental}")
    print(f"Confiança do modelo: {relatorio.probabilidade}%")
    print(f"Modelo: {relatorio.modelo_versao} | Análise: {relatorio.data_analise.isoformat()}")
    if relatorio.resumo:
        print(f"\nResumo da IA:\n{relatorio.resumo}")
    if relatorio.mensagens:
        print("\nDetalhamento por mensagem:")
        for idx, mensagem in enumerate(relatorio.mensagens, start=1):
            referencia = mensagem.timestamp or mensagem.data
            referencia_txt = referencia.isoformat() if referencia else "Data não informada"
            print(
                f"  {idx}. {referencia_txt} | Emoção: {mensagem.emocao or 'n/d'} "
                f"| Sentimento: {mensagem.sentimento or 'n/d'}"
            )
    if relatorio.insights:
        print("\nRecomendações personalizadas:")
        for idx, insight in enumerate(relatorio.insights, 1):
            print(f"  {idx}. {insight}")


def _persistir_resposta(usuario_id: int, relato_texto: str, relatorio: EmotionReport, registro_id: int) -> int:
    # Grava em T_NRON_RESP_FORMULARIO todos os metadados do check-in e retorna o ID criado.
    resposta_id = proximo_id("T_NRON_RESP_FORMULARIO", "ID_RESPOSTA")
    agora = _normalizar_datetime(datetime.now(timezone.utc))
    observacao = relatorio.resumo or relato_texto
    if relatorio.insights:
        dicas = " ".join(relatorio.insights)
        observacao = f"{observacao} Recomendações: {dicas}"
    observacao = (observacao or "")[:250]
    run_execute(
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


def _criar_registro_emocao(emocao_id: int, relatorio: EmotionReport) -> int:
    # Cria o registro em T_NRON_REGIST_EMOCAO (intensidade + emoção predominante).
    registro_id = proximo_id("T_NRON_REGIST_EMOCAO", "ID_REGIST_EMOCAO")
    descricao_base = relatorio.resumo or f"Emoção predominante: {relatorio.emocao_nome}"
    descricao = (descricao_base or "")[:255]
    run_execute(
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


def _buscar_emocao_id_por_nome(nome: str) -> int | None:
    # Faz lookup da emoção via nome (case-insensitive) para evitar cadastro manual.
    if not nome:
        return None
    linhas = run_query(
        "SELECT ID_EMOCAO FROM T_NRON_EMOCAO WHERE UPPER(NM_EMOCAO) = UPPER(:nome)",
        {"nome": nome.strip()},
    )
    if not linhas:
        return None
    return int(linhas[0]["id_emocao"])


def _resolver_emocao_id(relatorio: EmotionReport) -> int | None:
    # Decide qual ID de emoção será usado, pedindo input manual se a IA retornar algo desconhecido.
    emocao_id = relatorio.emocao_id or _buscar_emocao_id_por_nome(relatorio.emocao_nome)
    if emocao_id:
        return emocao_id
    print(
        "\nA IA identificou uma emoção que não está cadastrada no banco.",
        "Você pode informar manualmente o ID de uma emoção existente.",
        sep="\n",
    )
    try:
        resposta = solicitar_texto("ID da emoção [Enter para cancelar]", obrigatorio=False)
    except OperacaoCancelada:
        return None
    if not resposta:
        return None
    try:
        emocao_id = int(resposta)
    except ValueError:
        print("Valor inválido.")
        return None
    if not registro_existe("T_NRON_EMOCAO", "ID_EMOCAO", emocao_id):
        print("Emoção não encontrada.")
        return None
    return emocao_id


def _normalizar_datetime(valor: datetime) -> datetime:
    """Remove timezone para compatibilidade com colunas DATE do Oracle."""
    if valor.tzinfo is None:
        return valor
    return valor.astimezone(timezone.utc).replace(tzinfo=None)


if __name__ == "__main__":  # pragma: no cover
    realizar_checkin_emocional()
