"""Utilitários simples de CLI."""

from __future__ import annotations

import os
import platform


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
