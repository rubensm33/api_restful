#### *Objetivo*

O objetivo deste desafio é criar uma *API RESTful* para uma plataforma de compra e venda de ações. A API deverá ser capaz de gerenciar o cadastro de usuários, realizar operações de compra e venda de ações, consultar o portfólio e transações do usuário, e exibir informações detalhadas sobre as ações disponíveis no mercado.

#### *Requisitos Funcionais*

Você deve implementar os seguintes casos de uso em uma API:

1. *Cadastro de Usuário*
    
    - O usuário pode se cadastrar fornecendo *nome, **e-mail, **senha* (com validação de força) e *dados bancários* (dados fictícios são suficientes).
    - O sistema deve enviar um e-mail de verificação para validar o e-mail fornecido.
    - A senha deve ser *hash* antes de ser armazenada, e *não deve ser armazenada em texto claro*.
2. *Login de Usuário*
    
    - O usuário pode fazer login com *e-mail* e *senha*.
    - Após o login, a API deve gerar um *token JWT* que será utilizado para autenticação em futuras requisições.
3. *Listagem de Ações para Compra*
    
    - O usuário pode consultar uma lista de ações disponíveis para compra, que deve incluir informações como: *nome da ação, **preço atual, **volume de negociação* e *variação percentual*.
    - O preço das ações pode ser fornecido de forma estática ou você pode simular uma atualização em tempo real utilizando valores fictícios.
4. *Listagem de Ações no Portfólio do Usuário*
    
    - O usuário pode consultar as *ações que possui em seu portfólio, com a quantidade e o **preço médio de aquisição*.
    - O sistema deve garantir que o usuário só consiga vender as ações que ele realmente possui.
5. *Listagem de Papéis Disponíveis para Venda*
    
    - O usuário pode consultar as ações que ele possui e que estão *disponíveis para venda*, com detalhes sobre o preço de mercado atual.
6. *Histórico de Transações*
    
    - O usuário pode consultar todas as suas transações (compra e venda de ações), com *tipo de operação, **quantidade de ações, **preço unitário* e *data da transação*.
