import messages
from account import Account
from validators import validate_iban


class Bank:
    """Banco: tem um conjunto de contas, indexadas pelo número."""

    def __init__(self, name: str) -> None:
        """
        Inicializa o banco sem contas.

        Args:
            name (str): Nome do banco.
        """
        self.name = name
        self.__accounts: dict[str, Account] = {}

    def add_account(self, account: Account) -> None:
        """
        Acrescenta uma conta ao banco.

        Args:
            account (Account): Conta a acrescentar.

        Raises:
            ValueError: Se já existir uma conta com o mesmo número ou IBAN
                (mensagens com f-string, ver enunciado).
        """
        if account.number in self.__accounts:
            raise ValueError(f"Já existe uma conta com o número {account.number}.")

        if any(acc.iban == account.iban for acc in self.__accounts.values()):
            raise ValueError(f"Já existe uma conta com o IBAN {account.iban}.")

        self.__accounts[account.number] = account

    def find_account(self, number: str) -> Account | None:
        """
        Procura uma conta pelo número.

        Args:
            number (str): Número da conta.

        Returns:
            Account | None: A conta encontrada, ou None.
        """
        return self.__accounts.get(number)

    def find_by_iban(self, iban: str) -> Account | None:
        """
        Procura uma conta pelo IBAN.

        Args:
            iban (str): IBAN da conta.

        Returns:
            Account | None: A conta encontrada, ou None.
        """
        
        for account in self.__accounts.values():
            if account.iban == iban:
                return account
        return None

    def list_accounts(self) -> list[Account]:
        """
        Devolve todas as contas, ordenadas pelo número.

        Returns:
            list[Account]: Lista de contas.
        """
        return sorted(self.__accounts.values(), key=lambda acc: acc.number)

    def next_account_number(self) -> str:
        """
        Calcula o número da próxima conta a criar.

        Returns:
            str: Número seguinte ao maior existente, com 4 dígitos, ou '1001'
                se o banco ainda não tiver contas.
        """
        if not self.__accounts:
            return "1001"
        max_number = max(int(acc.number) for acc in self.__accounts.values())
        return str(max_number + 1).zfill(4)

    def generate_iban(self, number: str) -> str:
        """
        Gera o IBAN de uma conta a partir do seu número.

        Args:
            number (str): Número da conta.

        Returns:
            str: IBAN no formato PT50 seguido de 21 dígitos.
        """
        iban = f"PT50{number.zfill(21)}"
        validate_iban(iban)
        return iban

    def remove_account(self, number: str) -> None:
        """
        Elimina uma conta, desde que tenha saldo zero.

        Args:
            number (str): Número da conta.

        Raises:
            ValueError: Se a conta não existir (ACCOUNT_NOT_FOUND) ou o saldo
                não for zero (ACCOUNT_HAS_BALANCE).
        """
        account = self.find_account(number)
        if account is None:
            raise ValueError(messages.ACCOUNT_NOT_FOUND)
        if account.balance != 0:
            raise ValueError(messages.ACCOUNT_HAS_BALANCE)
        del self.__accounts[number]

    def unblock_account(self, number: str) -> None:
        """
        Desbloqueia uma conta.

        Args:
            number (str): Número da conta.

        Raises:
            ValueError: Se a conta não existir (ACCOUNT_NOT_FOUND) ou não estiver
                bloqueada (ACCOUNT_NOT_BLOCKED).
        """
        account = self.find_account(number)
        if account is None:
            raise ValueError(messages.ACCOUNT_NOT_FOUND)
        if not account.is_blocked:
            raise ValueError(messages.ACCOUNT_NOT_BLOCKED)
        account.unblock()

    def transfer(self, origin: Account, destination_iban: str, amount: float) -> None:
        """
        Transfere um valor entre duas contas do banco.

        A saída na origem é feita antes da entrada no destino: se a saída
        falhar, nenhuma das contas é alterada.

        Args:
            origin (Account): Conta de origem.
            destination_iban (str): IBAN da conta de destino.
            amount (float): Valor a transferir.

        Raises:
            ValueError: Pela ordem: IBAN com formato inválido (INVALID_IBAN),
                destino inexistente (DESTINATION_NOT_FOUND), destino igual à
                origem (SAME_ACCOUNT_TRANSFER) e, por fim, os erros de
                transfer_out (valor ou fundos).
        """
        if not validate_iban(destination_iban):
            raise ValueError(messages.INVALID_IBAN)

        destination = self.find_by_iban(destination_iban)
        if destination is None:
            raise ValueError(messages.DESTINATION_NOT_FOUND)

        if origin.iban == destination.iban:
            raise ValueError(messages.SAME_ACCOUNT_TRANSFER)

        origin.transfer_out(amount, destination.iban)
        destination.transfer_in(amount, origin.iban)
