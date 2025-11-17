"""Utilitários simples de CLI."""

from __future__ import annotations

import os
import platform
from decimal import Decimal
from typing import Sequence

_VOLTAR_KEYWORDS = {"0", "voltar", "sair", "exit", "quit", "retornar", "cancelar", "back"}


class OperacaoCancelada(Exception):
    """Exceção utilizada quando o usuário solicita voltar/cancelar."""


def limpar_tela() -> None:
    """Limpa o terminal de forma cross-platform."""
    comando = "cls" if platform.system() == "Windows" else "clear"
    os.system(comando)


def pausar(mensagem: str = "Pressione Enter para continuar...") -> None:
    """Pausa a execução até o usuário confirmar."""
    input(f"\n{mensagem}")


def titulo(texto: str) -> None:
    """Imprime um título padronizado para seções do menu."""
    barra = "-" * max(len(texto) + 10, 32)
    print(f"{barra}\n{texto.upper():^{len(barra)}}\n{barra}")


def confirmar_acao(msg: str = "Confirmar operação? (S/N): ") -> bool:
    """Solicita confirmação explícita (S/N) e só aceita respostas válidas."""
    while True:
        resposta = input(msg).strip().lower()
        if resposta in {"s", "sim"}:
            return True
        if resposta in {"n", "nao", "não"}:
            return False
        print("Por favor, responda com S ou N.")


def solicitar_confirmacao(pergunta: str) -> bool:
    """Compatibilidade com chamadas antigas de confirmação."""
    return confirmar_acao(f"{pergunta} (S/N): ")


def deseja_voltar(valor: str) -> bool:
    """Identifica se o usuário digitou um comando de retorno."""
    return valor.strip().lower() in _VOLTAR_KEYWORDS


def input_opcao(mensagem: str, opcoes_validas: Sequence[str]) -> str:
    """Solicita uma opção e garante que esteja no conjunto permitido."""
    normalizadas = {opcao.strip().lower(): opcao for opcao in opcoes_validas}
    while True:
        escolha = input(mensagem).strip()
        if deseja_voltar(escolha) and "0" in opcoes_validas:
            return "0"
        chave = escolha.lower()
        if chave in normalizadas:
            return normalizadas[chave]
        print("Opção inválida. Tente novamente.")


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
