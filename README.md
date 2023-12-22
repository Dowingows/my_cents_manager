# My Cents Manager

Este é um projeto Django desenvolvido para a gestão de finanças pessoais, permitindo o acompanhamento de despesas e receitas. Com esta aplicação, os usuários podem registrar suas transações financeiras, categorizá-las e visualizar relatórios para uma melhor compreensão de seus hábitos de gastos e recebimentos.

# Funcionalidades Principais


- Registro de Despesas e Receitas: Cadastre suas despesas e receitas de forma fácil e rápida.
Associe cada transação a uma categoria para uma organização eficiente.
Gestão de Categorias:

- Crie e gerencie categorias personalizadas para organizar suas transações.

- Relatórios Financeiros: Visualize relatórios detalhados para entender seu fluxo de caixa.
Analise suas despesas e receitas ao longo do tempo.

# Instalação

1. Clone o repositório
```bash
git clone https://github.com/Dowingows/my_cents_manager
```

2. Instale as Dependências usando Poetry:

```bash
cd my_cents_manager
poetry install
```

3. Aplique as migrações

```bash
poetry run python manage.py migrate
```

4. Crie um super usuário

```bash
poetry run python manage.py createsuperuser

```

5. Execute o servidor de desenvolvimento

```
poetry run python manage.py runserver
```

# Comandos úteis do projeto

- Linting:
```bash
poetry run task lint
```

- Formatação:
```bash
poetry run task format
```
- Executar Testes:

```bash
poetry run task test
```
