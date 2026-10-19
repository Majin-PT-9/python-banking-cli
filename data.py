from bank import Bank
from checking_account import CheckingAccount
from savings_account import SavingsAccount


def load_initial_data(bank: Bank) -> None:
    """
    Cria as contas iniciais e o seu histórico.

    Args:
        bank (Bank): Banco onde as contas são criadas.
    """
    joao = CheckingAccount(
        "1001", "João Silva", "1234",
        "PT50000000000000000001001", 1000.0,
    )
    maria = SavingsAccount(
        "1002", "Maria Costa", "4321",
        "PT50000000000000000001002", 2500.0,
    )
    pedro = CheckingAccount(
        "1003", "Pedro Santos", "5678",
        "PT50000000000000000001003", 500.0,
    )

    for account in [joao, maria, pedro]:
        bank.add_account(account)

    # Histórico de João Silva: 11 movimentos
    joao.deposit(200.0)
    joao.withdraw(50.0)
    joao.deposit(75.5)
    joao.withdraw(20.0)
    bank.transfer(joao, pedro.iban, 100.0)
    joao.deposit(30.0)
    joao.withdraw(40.0)
    joao.deposit(15.25)
    joao.withdraw(10.0)
    joao.deposit(60.0)
    joao.withdraw(30.0)

    # Histórico de Maria Costa: levantamento com comissão
    maria.withdraw(50.0)
