# Sistema de Hackathons

Aplicação web para gerenciamento de hackathons acadêmicos, desenvolvida em Python e Flask.

O sistema permite organizar hackathons, formar equipes, registrar projetos, realizar mentorias, avaliar projetos e consultar a classificação final. A aplicação possui autenticação e autorização por papéis, de modo que cada usuário executa apenas as ações compatíveis com sua função.

## Funcionalidades

### Organizador

- cadastrar hackathons;
- cadastrar contas de jurados e mentores;
- visualizar os colaboradores cadastrados;
- associar jurados e mentores aos hackathons que organiza.

### Participante

- criar uma conta pela própria aplicação;
- criar uma equipe e tornar-se automaticamente seu líder;
- adicionar participantes à equipe;
- registrar o projeto da equipe;
- consultar as mentorias registradas para as equipes das quais participa.

### Jurado

- acessar apenas projetos de hackathons aos quais foi associado;
- registrar uma avaliação com nota e comentário;
- avaliar cada projeto no máximo uma vez.

### Mentor

- acessar apenas equipes de hackathons aos quais foi associado;
- registrar comentários de mentoria para essas equipes.

### Consultas públicas

- consultar equipes por hackathon;
- consultar projetos por hackathon;
- consultar avaliações por hackathon e projeto;
- consultar a classificação dos projetos.

## Regras de negócio principais

- um participante pode pertencer a no máximo uma equipe por hackathon;
- cada hackathon possui um limite máximo de equipes;
- o criador da equipe torna-se seu líder e primeiro integrante;
- somente o líder pode adicionar participantes e registrar o projeto da equipe;
- cada equipe pode registrar apenas um projeto;
- somente jurados associados ao hackathon podem avaliar seus projetos;
- a nota de uma avaliação deve estar entre 0 e 10;
- um jurado pode avaliar cada projeto apenas uma vez;
- somente mentores associados ao hackathon podem registrar mentorias para suas equipes;
- somente participantes pertencentes a uma equipe podem consultar as mentorias registradas para ela;
- a classificação utiliza a média aritmética das avaliações;
- projetos sem avaliações não participam da classificação;
- projetos com a mesma média permanecem empatados.

## Arquitetura

A aplicação foi organizada em camadas para separar responsabilidades:

- `routes`: recebe requisições HTTP e coordena a interface;
- `services`: concentra regras de negócio e validações;
- `repositories`: realiza consultas e persistência no banco;
- `domain`: contém as entidades e tipos do domínio;
- `database`: gerencia a conexão e o schema SQLite;
- `auth`: contém os decorators de autenticação e autorização;
- `templates`: páginas HTML/Jinja;
- `static`: estilos da interface.

Fluxo principal:

```text
Interface / HTTP
      ↓
    Routes
      ↓
   Services
      ↓
Repositories
      ↓
    SQLite
```

Estrutura do projeto:

```text
app/
├── auth/
├── database/
├── domain/
├── repositories/
├── routes/
├── services/
├── static/
├── templates/
├── cli.py
├── config.py
└── __init__.py

docs/
tests/
run.py
requirements.txt
README.md
```

## Tecnologias

- Python 3.10+
- Flask
- Jinja2
- SQLite
- HTML
- CSS
- Werkzeug para hash e verificação de senhas
- `unittest` para testes automatizados

## Como executar

### 1. Criar o ambiente virtual

Na raiz do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Inicializar o banco

```bash
flask --app run init-db
```

O comando recria o banco em:

```text
instance/hackathons.sqlite3
```

> **Atenção:** `init-db` apaga os dados existentes e recria todas as tabelas.

### 4. Criar o primeiro organizador

Como o cadastro público cria apenas participantes, a primeira conta de organizador é criada pelo terminal:

```bash
flask --app run criar-organizador
```

O comando solicitará nome, e-mail e senha de forma interativa.

Também é possível informar os valores diretamente:

```bash
flask --app run criar-organizador \
  --nome "Pedro" \
  --email "pedro@exemplo.com" \
  --senha "uma-senha-segura"
```

### 5. Executar a aplicação

```bash
python run.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

## Autenticação e segurança

As senhas não são armazenadas em texto puro. O sistema utiliza as funções de hash do Werkzeug e mantém na sessão apenas o identificador do usuário autenticado.

O Flask utiliza uma `SECRET_KEY` para assinar a sessão e impedir sua adulteração. Neste projeto:

1. se a variável de ambiente `SECRET_KEY` estiver definida, ela é utilizada;
2. caso contrário, uma chave aleatória é criada automaticamente em `instance/.secret_key` na primeira execução e reutilizada localmente.

Como `instance/` é ignorado pelo Git, a chave local não é enviada ao repositório.

Em uma publicação real, recomenda-se definir explicitamente a variável de ambiente:

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

## Testes

A suíte automatizada utiliza `unittest` e um banco SQLite temporário, sem modificar o banco local da aplicação.

Execute:

```bash
python -m unittest discover -s tests -v
```

Os testes cobrem, entre outros pontos:

- fluxo integrado de usuários, hackathon, equipe, projeto, avaliação e mentoria;
- cálculo da classificação;
- autorização por papel;
- ownership da equipe;
- associação de jurados ao hackathon;
- obrigatoriedade do comentário da avaliação;
- comando de criação do organizador.

## Banco de dados

O modelo utiliza uma única entidade `Usuario`, diferenciada pelo papel:

```text
ORGANIZADOR
PARTICIPANTE
JURADO
MENTOR
```

As associações `hackathon_jurados` e `hackathon_mentores` determinam em quais hackathons cada colaborador pode atuar. Equipes possuem um líder e seus participantes são armazenados em uma relação N:N.

O banco SQLite e a chave local são arquivos de execução e não fazem parte do código-fonte versionado.

## Documentação

A pasta `docs/` contém artefatos produzidos durante a disciplina, incluindo DSS, contratos de operação e diagramas UML. Os diagramas podem ser atualizados separadamente para refletir integralmente a versão atual com autenticação e papéis de usuário.

## Origem do projeto

O sistema teve origem em um trabalho da disciplina de Engenharia de Software e foi posteriormente expandido para fins de estudo e portfólio, com autenticação, autorização por papéis, ownership das operações, testes automatizados e revisão da arquitetura e da interface.
