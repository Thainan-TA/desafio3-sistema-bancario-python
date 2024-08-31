from datetime import datetime, timezone
from abc import ABC, abstractmethod


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now(timezone.utc).date()
        return [t for t in self._transacoes if datetime.strptime(t["data"], "%d-%m-%Y %H:%M:%S").date() == data_atual]


class ContasIterador:
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._contas):
            conta = self._contas[self._index]
            self._index += 1
            return {
                "numero": conta.numero,
                "saldo": conta.saldo,
                "cliente": conta.cliente.nome
            }
        raise StopIteration


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 3:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return
        
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, endereco, cpf):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente, saldo=0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo
        self.historico = Historico()

    def __str__(self):
        return f"Conta {self.numero} - Saldo: R$ {self.saldo:.2f}"


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, saldo=0, limite=500):
        super().__init__(numero, cliente, saldo)
        self.limite = limite


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass
    

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
    
    def registrar(self, conta):
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            print(f"\n### Saque de R$ {self.valor:.2f} realizado com sucesso! ###")
        else:
            print("Saldo insuficiente.")


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        print(f"\n### Depósito de R$ {self.valor:.2f} realizado com sucesso! ###")


def validar_cpf(cpf):
    if not cpf.isdigit():
        print("\n@@@ CPF inválido! Digite apenas números. @@@")
        return False
    return True


def menu():
    print("\n=== MENU ===")
    print("1. Criar Cliente")
    print("2. Criar Conta")
    print("3. Depositar")
    print("4. Sacar")
    print("5. Exibir Extrato")
    print("6. Listar Contas")
    print("7. Sair")
    return input("Escolha uma opção: ")


def filtrar_cliente(cpf, clientes):
    for cliente in clientes:
        if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
            return cliente
    return None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas! @@@")
        return None
    return cliente.contas[0]


def log_transacao(func):
    def wrapper(*args, **kwargs):
        print(f"\n### Iniciando transação: {func.__name__} ###")
        resultado = func(*args, **kwargs)
        print(f"### Finalizando transação: {func.__name__} ###\n")
        return resultado
    return wrapper


@log_transacao
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        return
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor para depósito: "))
    deposito = Deposito(valor)
    cliente.realizar_transacao(conta, deposito)


@log_transacao
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        return
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor para saque: "))
    saque = Saque(valor)
    cliente.realizar_transacao(conta, saque)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        return
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n==================EXTRATO==================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==============================================")

@log_transacao
def criar_cliente(clientes):
    nome = input("Informe o nome do cliente: ")
    endereco = input("Informe o endereço do cliente: ")
    cpf = input("Informe o CPF do cliente: ")
    
    if not validar_cpf(cpf):
        return

    cliente = PessoaFisica(nome, endereco, cpf)
    clientes.append(cliente)
    print(f"\n### Cliente {nome} criado com sucesso! ###")


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    if not validar_cpf(cpf):
        return
    
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    nova_conta = ContaCorrente(numero_conta, cliente)
    cliente.adicionar_conta(nova_conta)
    contas.append(nova_conta)
    print(f"\n### Conta {numero_conta} criada com sucesso! ###")


def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta encontrada! @@@")
        return

    for conta in contas:
        print(f"Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}, Cliente: {conta.cliente.nome}")


def main():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == '1':
            criar_cliente(clientes)
        elif opcao == '2':
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1
        elif opcao == '3':
            depositar(clientes)
        elif opcao == '4':
            sacar(clientes)
        elif opcao == '5':
            exibir_extrato(clientes)
        elif opcao  == '6':
            listar_contas(contas)
        elif opcao  == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
