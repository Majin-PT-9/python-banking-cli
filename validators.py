"""Funções de validação e conversão de dados introduzidos pelo utilizador."""

import re

import messages


def validate_account_number(number: str) -> bool:
    """
    Verifica se o número de conta tem exatamente 4 dígitos.

    Args:
        number (str): Número de conta a validar.

    Returns:
        bool: True se o formato for válido, False caso contrário.
    """
    return re.fullmatch(r"\d{4}", number) is not None


def validate_pin(pin: str) -> bool:
    """
    Verifica se o PIN tem exatamente 4 dígitos.

    Args:
        pin (str): PIN a validar.

    Returns:
        bool: True se o formato for válido, False caso contrário.
    """
    return re.fullmatch(r"\d{4}", pin) is not None



def validate_iban(iban: str) -> bool:
    """
    Verifica se o IBAN tem o formato português: PT50 seguido de 21 dígitos.

    Args:
        iban (str): IBAN a validar.

    Returns:
        bool: True se o formato for válido, False caso contrário.
    """
    return re.fullmatch(r"PT50\d{21}", iban) is not None


def validate_name(name: str) -> bool:
    """
    Verifica se o nome tem pelo menos nome e apelido, só com letras.

    Args:
        name (str): Nome a validar.

    Returns:
        bool: True se o formato for válido, False caso contrário.
    """
    return re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)+", name) is not None


def validate_amount(amount: float) -> bool:
    """
    Verifica se um valor monetário é positivo e tem no máximo 2 casas decimais.

    Args:
        amount (float): Valor a validar.

    Returns:
        bool: True se o valor for válido, False caso contrário.
    """
    return amount > 0 and round(amount, 2) == amount


def parse_amount(text: str) -> float:
    """
    Converte o texto introduzido pelo utilizador num valor monetário.

    Aceita o sinal negativo e tanto o ponto como a vírgula como separador decimal.
    Não verifica se o valor é positivo: essa validação é feita por validate_amount.

    Args:
        text (str): Texto a converter.

    Returns:
        float: Valor convertido.

    Raises:
        ValueError: Se o texto não representar um número (INVALID_NUMBER_TEXT).
    """
    formatted_value = text.strip().replace(",", ".")
    try:
        return float(formatted_value)
    except ValueError:
        raise ValueError(messages.INVALID_NUMBER_TEXT)
