"""Utilitários simples de CLI."""

from __future__ import annotations

import os
import platform
from decimal import Decimal

_VOLTAR_KEYWORDS = {"0", "voltar", "sair", "exit", "quit", "retornar", "cancelar", "back"}


class OperacaoCancelada(Exception):
    """Exceção utilizada quando o usuário solicita voltar/cancelar."""


def limpar_tela() -> None:
    """Limpa o terminal de forma cross-platform."""
    # Cada CLI chama antes de exibir menus para evitar poluição visual.
    comando = "cls" if platform.system() == "Windows" else "clear"
    os.system(comando)


def pausar(mensagem: str = "Pressione Enter para continuar...") -> None:
    """Pausa a execução até o usuário confirmar."""
    # Garante que o usuário leia mensagens antes de voltar ao menu.
    input(f"\n{mensagem}")


def solicitar_confirmacao(pergunta: str) -> bool:
    """Solicita confirmação simples (s/n)."""
    # Padrão para operações destrutivas, evitando exclusões acidentais.
    resposta = input(f"{pergunta} (s/n): ").strip().lower()
    return resposta == "s"


def deseja_voltar(valor: str) -> bool:
    """Identifica se o usuário digitou um comando de retorno."""
    return valor.strip().lower() in _VOLTAR_KEYWORDS


def _prompt(mensagem: str) -> str:
    mensagem = mensagem.strip()
    sufixo = " (digite 'voltar' para cancelar)"
    if mensagem.endswith(":"):
        mensagem = mensagem[:-1]
    return f"{mensagem}{sufixo}: "


def solicitar_texto(mensagem: str, padrao: str | None = None, obrigatorio: bool = True) -> str:
    """Solicita texto com a instrução explícita de que 'voltar' cancela a operação."""
    while True:
        resposta = input(_prompt(mensagem)).strip()
        if deseja_voltar(resposta):
            raise OperacaoCancelada()
        if not resposta and padrao is not None:
            return padrao
        if resposta or not obrigatorio or padrao is not None:
            return resposta
        print("Campo obrigatório. Informe um valor ou digite 'voltar' para retornar.")


def solicitar_inteiro(mensagem: str, padrao: int | None = None) -> int:
    """Solicita um número inteiro, permitindo cancelar com 'voltar'."""
    while True:
        resposta = input(_prompt(mensagem)).strip()
        if deseja_voltar(resposta):
            raise OperacaoCancelada()
        if not resposta and padrao is not None:
            return padrao
        if not resposta:
            print("Informe um número válido ou digite 'voltar'.")
            continue
        try:
            return int(resposta)
        except ValueError:
            print("Informe um número válido ou digite 'voltar'.")


def solicitar_decimal(mensagem: str, padrao: Decimal | None = None) -> Decimal:
    """Solicita um número decimal aceitando vírgula ou ponto."""
    while True:
        resposta = input(_prompt(mensagem)).strip()
        if deseja_voltar(resposta):
            raise OperacaoCancelada()
        if not resposta and padrao is not None:
            return padrao
        if not resposta:
            print("Informe um número válido ou digite 'voltar'.")
            continue
        try:
            normalizado = resposta.replace(",", ".")
            return Decimal(normalizado)
        except Exception:
            print("Não foi possível interpretar o número informado. Tente novamente ou digite 'voltar'.")
