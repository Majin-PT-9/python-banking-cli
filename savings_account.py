import messages
from account import Account


class SavingsAccount(Account):
    """Conta poupança: cada levantamento tem uma comissão fixa."""

    WITHDRAWAL_FEE = 1.0

    def account_type(self) -> str:
        """
        Devolve a designação do tipo de conta.

        Returns:
            str: messages.ACCOUNT_TYPE_SAVINGS ('Conta poupança').
        """
        return messages.ACCOUNT_TYPE_SAVINGS


    def withdraw(self, amount: float) -> None:
        """
        Levanta um valor e cobra a comissão de levantamento.

        Valida pela mesma ordem da classe base (valor, múltiplo de 10) e só
        depois os fundos, que têm de cobrir o valor mais a comissão. Regista
        dois movimentos: o levantamento e a comissão (MOVEMENT_FEE, com a
        descrição MOVEMENT_FEE_DESCRIPTION).

        Args:
            amount (float): Valor a levantar, múltiplo de 10.

        Raises:
            ValueError: Se o valor for inválido (INVALID_AMOUNT), não for múltiplo
                de 10 (INVALID_WITHDRAWAL_MULTIPLE) ou os fundos não cobrirem o
                valor e a comissão (INSUFFICIENT_FUNDS_WITH_FEE).
        """
        self._validate_withdrawal(amount)

        if amount + self.WITHDRAWAL_FEE > self._available_funds():
            raise ValueError(messages.INSUFFICIENT_FUNDS_WITH_FEE)

        super().withdraw(amount)
        self._debit(self.WITHDRAWAL_FEE, messages.MOVEMENT_FEE, messages.MOVEMENT_FEE_DESCRIPTION)