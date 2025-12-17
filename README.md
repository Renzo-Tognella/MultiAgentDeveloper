# MultiAgent Developer

Sistema de processamento de cards de backlog usando múltiplos agentes de IA especializados.

## Arquitetura

Projeto estruturado seguindo **Clean Architecture** e **Clean Code**:

```
MultiAgentDeveloper/
├── main.py                     # Entry point
├── requirements.txt
│
├── core/                       # Domínio e orquestração
│   ├── config.py              # Configuração centralizada
│   ├── entities.py            # Entidades de domínio
│   ├── exceptions.py          # Exceções customizadas
│   ├── parsers.py             # Parsers (Strategy pattern)
│   ├── slack.py               # Integração Slack (Human-in-the-loop)
│   └── orchestrator.py        # Orquestrador (DI + Factory)
│
├── frameworks/                 # Agentes por tecnologia
│   ├── base.py                # Classes abstratas (DRY)
│   ├── react/                 # React JS
│   ├── rails/                 # Ruby on Rails
│   ├── apex/                  # Salesforce Apex
│   └── frontend/              # HTML/CSS/JS
│
├── tools/                      # Ferramentas dos agentes
│   ├── analyzer.py            # Análise de codebase
│   ├── filesystem.py          # Operações de arquivo
│   └── human_input.py         # Ferramenta de input do usuário
│
└── sample_cards/               # Exemplos de cards
```

## Princípios Aplicados

- **Single Responsibility**: Cada classe tem uma responsabilidade
- **Open/Closed**: Extensível para novos frameworks sem modificar código existente
- **Dependency Inversion**: Injeção de dependências no orchestrator
- **Strategy Pattern**: Parsers intercambiáveis para diferentes formatos
- **Factory Pattern**: Criação de crews especializados
- **Template Method**: Classes base para agents e tasks

## Requisitos

- Python 3.10+ (recomendado 3.11)
- OpenAI API Key

## Instalação

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env`:

```env
# OpenAI (obrigatório)
OPENAI_API_KEY=sua_chave

# Slack (opcional - human-in-the-loop)
SLACK_ENABLED=true
SLACK_BOT_TOKEN=xoxb-seu-token
SLACK_CHANNEL=C0123456789
SLACK_POLL_INTERVAL=5
SLACK_TIMEOUT=300

# Geral
LOG_LEVEL=INFO
VERBOSE_AGENTS=false
```

## Integração Slack (Human-in-the-loop)

Os agentes podem fazer perguntas ao usuário durante o desenvolvimento via Slack.

### Como Funciona

1. Agente identifica que precisa de clarificação
2. Usa a ferramenta `Ask User Question` para enviar pergunta ao Slack
3. Sistema aguarda resposta do usuário (com timeout configurável)
4. Resposta é retornada ao agente que continua o trabalho

### Configuração do Slack Bot

1. Acesse [api.slack.com/apps](https://api.slack.com/apps)
2. Crie um novo app e adicione ao workspace
3. Em **OAuth & Permissions**, adicione os scopes:
   - `chat:write`
   - `channels:history`
   - `groups:history`
4. Instale o app e copie o **Bot User OAuth Token**
5. Adicione o bot ao canal desejado

### Modo Console (sem Slack)

Se `SLACK_ENABLED=false` ou não configurado, o sistema usa input via console:

```
❓ Agent Question: Qual banco de dados você prefere?
📝 Your answer: PostgreSQL
```

## Uso

```bash
python main.py
```

O sistema aceita cards em formato JSON, Markdown ou texto plano.

## Frameworks Suportados

| Framework | Tecnologias |
|-----------|-------------|
| React | JSX, Hooks, Context API |
| Rails | Ruby, Active Record, RSpec |
| Apex | Salesforce, SOQL, LWC |
| Frontend | HTML5, CSS3, ES6+ |

## Estrutura de um Card

```markdown
# Título da Feature

## Description
Descrição detalhada...

## Acceptance Criteria
- Critério 1
- Critério 2

Priority: High
Story Points: 5
```
