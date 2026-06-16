# Afiliados Claude CRO

Este repositório é um **Monorepo** que integra duas poderosas arquiteturas:

1. **Web Store (`/web-store`)**: Um frontend e painel de controle construído em Next.js para gerenciamento de links de produtos afiliados. Permite criar catálogos, processar links e gerenciar os produtos em MongoDB usando Prisma.
2. **AI Automation (`/ai-automation`)**: Motor de automação inteligente desenvolvido em Python (com base em CrewAI e OpenClaw). Projetado para realizar raspagem de dados, monitorar plataformas de afiliados e utilizar agentes de IA para gerar copys persuasivas que alimentam a loja.

## Estrutura do Projeto

```
afiliados-claude-cro/
├── web-store/           # Código-fonte da loja Next.js
├── ai-automation/       # Agentes de pesquisa, scripts de extração e prompts
└── README.md            # Esta documentação
```

## Como começar

### Subindo a loja web
```bash
cd web-store
npm install
npm run dev
```

### Rodando o motor de IA
```bash
cd ai-automation
# (As instruções de pip install dependerão dos scripts de agentes que configurarmos aqui)
```

## Próximos Passos
- Conectar os agentes Python à API do Next.js.
- Configurar rotinas de atualização diária dos produtos.
