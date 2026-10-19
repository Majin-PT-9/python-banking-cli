"""
Mensagens fixas e designações usadas pelo programa.

Este ficheiro é fornecido completo e não pode ser alterado.
As mensagens que incluem valores (saldos, nomes, números de conta) não estão
aqui: são escritas com f-strings no próprio código, como indicado no enunciado.
"""

# Designações dos tipos de conta
ACCOUNT_TYPE_BASE = "Conta"
ACCOUNT_TYPE_CHECKING = "Conta à ordem"
ACCOUNT_TYPE_SAVINGS = "Conta poupança"

# Tipos e descrições de movimentos
MOVEMENT_DEPOSIT = "Depósito"
MOVEMENT_DEPOSIT_DESCRIPTION = "Depósito em numerário"
MOVEMENT_WITHDRAWAL = "Levantamento"
MOVEMENT_WITHDRAWAL_DESCRIPTION = "Levantamento ATM"
MOVEMENT_TRANSFER_OUT = "Transferência enviada"
MOVEMENT_TRANSFER_IN = "Transferência recebida"
MOVEMENT_FEE = "Comissão"
MOVEMENT_FEE_DESCRIPTION = "Comissão de levantamento"

# Erros de validação de dados da conta (ValueError)
INVALID_ACCOUNT_NUMBER = "O número da conta tem de ter 4 dígitos."
INVALID_HOLDER = "O nome do titular tem de ter nome e apelido, só com letras."
INVALID_PIN = "O PIN tem de ter 4 dígitos."
INVALID_IBAN = "IBAN inválido."
INVALID_INITIAL_BALANCE = (
    "O saldo inicial tem de ser zero ou positivo, com o máximo de 2 casas decimais."
)

# Erros de operações (ValueError)
INVALID_NUMBER_TEXT = "Valor inválido. Introduza um número."
INVALID_AMOUNT = "O valor tem de ser positivo e ter no máximo 2 casas decimais."
INVALID_WITHDRAWAL_MULTIPLE = "O valor do levantamento tem de ser múltiplo de 10 €."
INSUFFICIENT_FUNDS = "Saldo insuficiente."
INSUFFICIENT_FUNDS_WITH_FEE = "Saldo insuficiente para o levantamento e a comissão."
DESTINATION_NOT_FOUND = "IBAN de destino não encontrado."
SAME_ACCOUNT_TRANSFER = "Não é possível transferir para a própria conta."
INVALID_ACCOUNT_TYPE = "Tipo de conta inválido."
ACCOUNT_HAS_BALANCE = "Só é possível eliminar contas com saldo zero."
ACCOUNT_NOT_BLOCKED = "A conta não está bloqueada."

# Autenticação
ACCOUNT_NOT_FOUND = "Conta não encontrada."
ACCOUNT_BLOCKED = "Conta bloqueada. Contacte o administrador."
WRONG_PIN = "PIN incorreto."
ACCOUNT_NOW_BLOCKED = "PIN incorreto. A conta foi bloqueada."
WRONG_ADMIN_PIN = "PIN de administrador incorreto."

# Confirmações e mensagens gerais
NO_MOVEMENTS = "Ainda não existem movimentos."
ACCOUNT_REMOVED = "Conta eliminada."
ACCOUNT_UNBLOCKED = "Conta desbloqueada."
SESSION_ENDED = "Sessão terminada."
INVALID_OPTION = "Opção inválida."
GOODBYE = "Obrigado por utilizar o nosso multibanco."

# Prefixo das mensagens de erro mostradas ao utilizador
ERROR_PREFIX = "Erro: "
