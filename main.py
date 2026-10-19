import sys
import messages
from account import Account
from bank import Bank
from checking_account import CheckingAccount
from data import load_initial_data
from savings_account import SavingsAccount
from validators import parse_amount

ADMIN_PIN = "9999"


def main() -> None:
    """
    Carrega os dados iniciais e apresenta o menu inicial.

    """
    bank = Bank("Banco ATEC")
    load_initial_data(bank)

    while True:
        print()
        print("=== Multibanco ===")
        print("1. Entrar como cliente")
        print("2. Entrar como administrador")
        print("3. Sair")

        opcao = input().strip()

        if opcao == "1":
            client_session(bank)
        elif opcao == "2":
            admin_session(bank)
        elif opcao == "3":
            print(messages.GOODBYE)
            sys.exit(0)
        else:
            print(messages.INVALID_OPTION)

#region Client          
def client_session(bank: Bank) -> None:
    """
    Autentica o cliente e, se tiver sucesso, mostra o menu de cliente.

    Args:
        bank (Bank): Banco onde procurar a conta.
    """
    
    account = login(bank)
    if account is None:
        return
        
    while True:
        print("1. Consultar saldo")
        print(f"2. {messages.MOVEMENT_WITHDRAWAL}")
        print(f"3. {messages.MOVEMENT_DEPOSIT}")
        print("4. Transferência")
        print("5. Últimos 10 movimentos")
        print("6. Terminar sessão")
        
        option = read_option(["1", "2", "3", "4", "5", "6"])
        
        match option:
            case "1":
                print(f"Saldo disponível: {account.balance:.2f} €")
            case "2":
                withdraw_menu(account)
            case "3":
                deposit_menu(account)
            case "4":
                transfer_menu(bank, account)
            case "5":
                show_last_movements(account)
            case "6":
                print(messages.SESSION_ENDED)
                return
            
def login(bank: Bank) -> Account | None:
    """
    Pede o número de conta e o PIN, e autentica o cliente.

    Args:
        bank (Bank): Banco onde procurar a conta.
    
    Returns:
        Account | None: A conta autenticada, ou None se o login falhar.
    """
    number = input("Insira o número de conta: \n").strip()
    account = bank.find_account(number)
    
    if account is None:
        print(messages.ACCOUNT_NOT_FOUND)
        return None
    if account.is_blocked:
        print(messages.ACCOUNT_BLOCKED)
        return None
    
    while True:
        pin = input("Insira o código PIN: \n").strip()
        if account.check_pin(pin):
            print(f"Bem-vindo(a), {account.holder}.")
            return account
        else:
            if account.is_blocked:
                print(messages.ACCOUNT_NOW_BLOCKED)
                return None
            else:
                print(messages.WRONG_PIN)
            
def withdraw_menu(account: Account) -> None:
    """Mostra o menu de levantamento e processa a operação.

    Args:
        account (Account): Conta do cliente.
    """
    amount = input("Introduza o valor a levantar (multiplos de 10) \n")
    try:
        parsed_amount = parse_amount(amount)
        account.withdraw(parsed_amount)
        print(f"Levantamento efetuado. Saldo: {account.balance:.2f} €")
    except ValueError as e:
            print(messages.ERROR_PREFIX + str(e))

def deposit_menu(account: Account) -> None:
    """Mostra o menu de depósito e processa a operação.

    Args:
        account (Account): Conta do cliente.
    """
    
    amount = input("Introduza o valor a depositar (multiplos de 10) \n")
    try:
        parsed_amount = parse_amount(amount)
        account.deposit(parsed_amount)
        print(f"Depósito efetuado. Saldo: {account.balance:.2f} €")
    except ValueError as e:
        print(messages.ERROR_PREFIX + str(e))

def transfer_menu(bank: Bank, account: Account) -> None:
    """Mostra o menu de transferência e processa a operação.
    Args:
        bank (Bank): Banco onde procurar a conta de destino.
        account (Account): Conta do cliente.
    """
    
    destination_iban = input("Introduza o IBAN de destino: \n").strip().upper()
    amount = input("Introduza o valor a transferir: \n")
    
    try:
        parsed_amount = parse_amount(amount)
        bank.transfer(account, destination_iban, parsed_amount)
        print(f"Transferência efetuada. Saldo: {account.balance:.2f} €")
    except ValueError as e:
        print(messages.ERROR_PREFIX + str(e))
        
def show_last_movements(account: Account) -> None:
    """Mostra os últimos 10 movimentos da conta.
    Args:
        account (Account): Conta do cliente.
    """
    
    movements = account.get_last_movements(10)
    if not movements:
        print(messages.NO_MOVEMENTS)
        return
    for movement in movements:
        print(movement)   
            

#endregion

#region Admin
def admin_session(bank: Bank) -> None:
    """
    Pede o PIN de administrador e, se estiver certo, mostra o menu de
    administrador.

    Args:
        bank (Bank): Banco a administrar.
    """
    pin = input("Insira o PIN de administrador: \n").strip()
    if pin != ADMIN_PIN:
        print(messages.WRONG_ADMIN_PIN)
        return
        
    while True:
        print("1. Criar conta")
        print("2. Listar Contas")
        print("3. Eliminar conta")
        print("4. Desbloquear conta")
        print("5. Terminar sessão")
        
        option = read_option(["1", "2", "3", "4", "5"])
        
        match option:
            case "1":
                create_account(bank)
            case "2":
                list_accounts(bank)
            case "3":
                remove_account(bank)
            case "4":
                unblock_account(bank)
            case "5":
                print(messages.SESSION_ENDED)
                return

def create_account(bank: Bank) -> None:
    """
    Cria uma nova conta no banco.

    Args:
        bank (Bank): Banco onde a conta é criada.
    """
    print("Escolha o tipo de conta:")
    print("1. Conta à ordem")
    print("2. Conta poupança")
    
    account_type_option = input().strip()
    
    try:
        if account_type_option == "1":
            account_type = CheckingAccount
        elif account_type_option == "2":
            account_type = SavingsAccount
        else:
            raise ValueError(messages.INVALID_ACCOUNT_TYPE)
    except ValueError as e:
        print(messages.ERROR_PREFIX + str(e))
        return
    
    holder = input("Introduza o nome do titular: \n").strip()
    pin = input("Introduza o PIN (4 dígitos): \n").strip()
    initial_balance_input = input("Introduza o saldo inicial: \n").strip()
    
    try:
        number = bank.next_account_number()
        iban = bank.generate_iban(number)
        initial_balance = parse_amount(initial_balance_input)
        
        new_account = account_type(number, holder, pin, iban, initial_balance)
        bank.add_account(new_account)
        
        print(f"Conta criada: {new_account.number} | {new_account.account_type()} | {new_account.holder} | {new_account.balance:.2f} €")
        print(f"IBAN: {new_account.iban}")
        
    except ValueError as e:
        print(messages.ERROR_PREFIX + str(e))            

def list_accounts(bank: Bank) -> None:
    """
    Lista todas as contas do banco.

    Args:
        bank (Bank): Banco cujas contas são listadas.
    """
    accounts = bank.list_accounts()
    if not accounts:
        print("Não existem contas.")
        return
    for account in accounts:
        print(f"{account.number} | {account.account_type()} | {account.holder} | {account.balance:.2f} €")
        
def remove_account(bank: Bank) -> None:
    """
    Elimina uma conta do banco.

    Args:
        bank (Bank): Banco onde a conta é eliminada.
    """
    number = input("Introduza o número da conta a eliminar: \n").strip()
    try:
        bank.remove_account(number)
        print(messages.ACCOUNT_REMOVED)
    except ValueError as e:
        print(messages.ERROR_PREFIX + str(e))
        
def unblock_account(bank: Bank) -> None:
    """
    Desbloqueia uma conta bloqueada.

    Args:
        bank (Bank): Banco onde a conta é desbloqueada.
    """
    number = input("Introduza o número da conta a desbloquear: \n").strip()
    try:
        bank.unblock_account(number)
        print(messages.ACCOUNT_UNBLOCKED)
    except ValueError as e:
        print(messages.ERROR_PREFIX + str(e))
#endregion

#region General Functions
def read_option(valid_options: list[str]) -> str:
    """
    Lê a opção escolhida pelo utilizador e verifica se é válida.

    Args:
        valid_options (list[str]): Opções válidas (por exemplo, ["1", "2", "3"]).

    Returns:
        str: A opção escolhida, ou "" se não for uma das válidas.
    """
    option = input().strip()
    if option not in valid_options:
        print(messages.INVALID_OPTION)
        return ""
    return option

#endregion

if __name__ == "__main__":
    main()
