"""Fluxo de check-in emocional com análise local."""

from __future__ import annotations

from datetime import datetime, timezone

from connect.connect import verificar_conexao_oracle
from services.analise_emocional import AnaliseEmocionalError, EmotionReport, analisar_conversa
from services.checkin_service import (
    buscar_emocao_id_por_nome,
    listar_emocoes,
    salvar_checkin,
    usuario_existe,
)
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
    # Orquestra o fluxo completo: captura usuário, executa a análise local e persiste tudo no Oracle.
    """Permite que o colaborador descreva seu momento e registre a análise retornada pela heurística local."""
    try:
        verificar_conexao_oracle()
        limpar_tela()
        print("=== Check-in emocional ===\n")
        print("Digite 'voltar' a qualquer momento para cancelar e retornar ao menu.\n")
        usuario_id = solicitar_inteiro("ID do colaborador")
        if not usuario_existe(usuario_id):
            print("Usuário não encontrado.")
            return
        texto = _coletar_relato()
        if not texto:
            print("Nenhum relato informado, operação cancelada.")
            return
        print("\nProcessando relato com a análise emocional local...")
        mensagens = [
            {
                "texto": texto,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]
        try:
            relatorio = analisar_conversa(mensagens)
        except AnaliseEmocionalError as exc:
            print(f"\nNão foi possível analisar o relato: {exc}")
            return
        _mostrar_relatorio(relatorio)
        if not solicitar_confirmacao("\nDeseja salvar este check-in no banco de dados?"):
            print("Check-in descartado pelo usuário.")
            return
        emocao_id = _resolver_emocao_id(relatorio)
        if not emocao_id:
            print("Não foi possível associar a emoção identificada a uma categoria válida. Operação cancelada.")
            return
        registro_id, resposta_id = salvar_checkin(usuario_id, texto, relatorio, emocao_id)
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
        "Pressione Enter em branco para finalizar (nada será salvo) ou digite 'voltar' para cancelar.\n",
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
    # Exibe métricas retornadas pela heurística local para que o colaborador aprove ou não o salvamento.
    print("\n--- Relatório da análise emocional ---")
    emocao = relatorio.emocao_nome or "indefinida"
    print(f"Emoção predominante: {emocao}")
    if relatorio.emocoes_secundarias:
        print("Emoções secundárias:")
        for nome, score in relatorio.emocoes_secundarias:
            print(f"  - {nome}: {score}% de relevância")
    if relatorio.sentimentos_distribuicao:
        principal_sent = max(relatorio.sentimentos_distribuicao.items(), key=lambda item: item[1])[0]
        print(f"Sentimento predominante: {principal_sent}")
    print(
        f"Motivação: {relatorio.motivacao}% | Felicidade: {relatorio.felicidade}% | "
        f"Estresse: {relatorio.estresse}% | Saúde mental: {relatorio.saude_mental}%"
    )
    print(f"Intensidade do relato: {relatorio.intensidade}% | Confiança da análise: {relatorio.probabilidade}%")
    print(f"Motor: {relatorio.modelo_versao} | Análise: {relatorio.data_analise.isoformat()}")
    if relatorio.resumo:
        print(f"\nResumo da análise:\n{relatorio.resumo}")
    if relatorio.mensagens:
        print("\nDetalhamento por mensagem:")
        for idx, mensagem in enumerate(relatorio.mensagens, start=1):
            referencia = mensagem.timestamp or mensagem.data
            referencia_txt = referencia.isoformat() if referencia else "Data não informada"
            sec_emocoes = ", ".join(f"{k}: {v}%" for k, v in mensagem.emocao_scores.items())
            print(
                f"  {idx}. {referencia_txt} | Emoção principal: {mensagem.emocao or 'n/d'} "
                f"| Sentimento: {mensagem.sentimento or 'n/d'}"
            )
            if sec_emocoes:
                print(f"     Distribuição de emoções: {sec_emocoes}")
    if relatorio.insights:
        print("\nRecomendações personalizadas:")
        for idx, insight in enumerate(relatorio.insights, 1):
            print(f"  {idx}. {insight}")


def _resolver_emocao_id(relatorio: EmotionReport) -> int | None:
    # Decide qual ID de emoção será usado, pedindo input manual se a análise retornar algo desconhecido.
    emocao_id = relatorio.emocao_id or buscar_emocao_id_por_nome(relatorio.emocao_nome)
    if emocao_id:
        return emocao_id
    print(
        "\nA análise identificou uma emoção que não está cadastrada no banco.",
        "Você pode informar manualmente o ID de uma emoção existente. Registros recentes:",
        sep="\n",
    )
    _listar_emocoes_disponiveis()
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
    if not any(int(linha["id_emocao"]) == emocao_id for linha in listar_emocoes()):
        print("Emoção não encontrada.")
        return None
    return emocao_id


def _listar_emocoes_disponiveis() -> None:
    linhas = listar_emocoes()
    if not linhas:
        print("Nenhuma emoção cadastrada.")
        return
    for linha in linhas:
        print(f"  {linha['id_emocao']:>3} | {linha['nm_emocao']}")


if __name__ == "__main__":  # pragma: no cover
    realizar_checkin_emocional()
