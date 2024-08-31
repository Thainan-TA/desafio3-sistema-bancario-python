# Sistema Bancário em Python
Este projeto implementa um sistema bancário simples em Python, permitindo a criação de clientes, contas correntes, e a realização de transações bancárias como depósitos, saques e consulta de extratos.

### Funcionalidades

1. **Criação de Clientes**

* Permite criar novos clientes com informações como nome, endereço e CPF.
* O CPF é validado para garantir que apenas números sejam inseridos.
2. **Criação de Contas Correntes**

* Cada cliente pode possuir uma ou mais contas correntes.
* As contas correntes são criadas com um número único, um saldo inicial e um limite de crédito.
* As contas são vinculadas ao cliente, permitindo que todas as transações sejam associadas ao respectivo titular.
3. **Transações Bancárias**

* Depósitos: Os clientes podem depositar valores em suas contas, aumentando o saldo.
* Saques: Os clientes podem realizar saques, diminuindo o saldo da conta. Há uma verificação para garantir que o saldo seja suficiente.
* Limite de Transações Diárias: O sistema impõe um limite de três transações por dia para cada conta, para segurança adicional.
4. **Consulta de Extratos**

* O extrato exibe todas as transações realizadas na conta, incluindo data, tipo de transação e valor.
* Exibe o saldo atual da conta ao final do extrato.
5. **Listagem de Contas**

* Exibe uma lista de todas as contas criadas, mostrando o número da conta, saldo e o nome do cliente associado.

### Estrutura do Código
**Classes Principais**

* Cliente: Representa um cliente do banco, que pode ser uma Pessoa Física.
* ContaCorrente: Representa uma conta corrente, incluindo saldo, limite de crédito e histórico de transações.
* Transacao (Abstract Base Class): Classe abstrata para operações bancárias. Possui duas subclasses:
    * Saque: Subclasse de Transacao que permite realizar saques na conta.
    * Deposito: Subclasse de Transacao que permite realizar depósitos na conta.
**Histórico de Transações**

* Historico: Mantém um registro de todas as transações realizadas em uma conta. Oferece métodos para gerar relatórios de transações e listar transações do dia.
**Iteradores**

* ContasIterador: Um iterador personalizado para iterar sobre a lista de contas, retornando informações sobre o número da conta, saldo e nome do cliente.
**Decoradores**

* log_transacao: Decorador que registra o início e o fim de cada transação para facilitar o monitoramento das operações realizadas.
### Validação e Segurança

* Validação de CPF: Garante que o CPF inserido contém apenas números.
* Limite de Transações Diárias: Impõe um limite de três transações por dia para proteger o cliente contra atividades fraudulentas.
### Como Executar

1. Certifique-se de ter o Python instalado em seu sistema.
2. Clone este repositório para o seu ambiente local.
3. Navegue até o diretório do projeto.
4. Execute o script main.py para iniciar o sistema bancário.

### Conclusões
Este modelo de sistema bancário ainda não está concluído, porém o objetivo futuramente é validar todos os pontos de segurança possíveis.