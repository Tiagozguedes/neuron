# Juntos Pela Saúde – Neuron

> Plataforma SaaS B2B de inteligência emocional corporativa que combina IA ética, privacidade por design e gamificação de bem-estar para apoiar colaboradores e líderes na construção de culturas organizacionais saudáveis.

## Índice
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Modelo de Negócio](#modelo-de-negócio)
3. [Produto e Tecnologia](#produto-e-tecnologia)
4. [Histórias, Requisitos e Regras](#histórias-requisitos-e-regras)
5. [Mercado e Vantagem Competitiva](#mercado-e-vantagem-competitiva)
6. [Plano de Investimento e ROI](#plano-de-investimento-e-roi)
7. [SLA e Suporte](#sla-e-suporte)
8. [Autores](#autores)

---

## Sobre o Projeto
**Neuron** nasce do aumento expressivo de burnout, ansiedade e estresse corporativo no Brasil. Muitas empresas carecem de ferramentas empáticas, éticas e transparentes para acompanhar o bem-estar emocional. A iniciativa transforma o monitoramento em um programa voluntário de autocuidado, onde:

- Colaboradores realizam check-ins, recebem recomendações personalizadas e recompensas.
- Empresas acessam indicadores agregados e anonimizados para orientar decisões de clima.
- O Time Neuron atua como terceira parte ética garantindo conformidade com LGPD/GDPR.

### Oportunidade
- OMS coloca o Brasil entre os países com maior ocorrência de transtornos relacionados ao trabalho.
- Falta de soluções que unam tecnologia de ponta, privacidade e retorno claro para o funcionário.
- Demanda crescente por iniciativas ESG e cultura de empatia.

---

## Modelo de Negócio

### SaaS B2B Recorrente
- **Plano Essencial** (até 300 colaboradores) – dashboards agregados, check-ins básicos, análises preditivas e alertas inteligentes. Valor sugerido: R$ 1.900/mês.
- **Plano Premium** (até 500 colaboradores) – tudo do Essencial + suporte humano (psicólogos/consultores), workshops, trilhas de autocuidado e relatórios guiados. Valor sugerido: R$ 4.500/mês.
- Cada colaborador possui área gratuita para acompanhar seu Mood Index, recomendações e recompensas.

### Relacionamento Multinível
| Perfil | Responsabilidades e acessos |
| --- | --- |
| **Empresa (RH / People Analytics)** | Administra a conta, define consentimento, vê apenas dados agregados. |
| **Gestor** | Recebe insights de clima da equipe e sugestões de microações. |
| **Colaborador** | Dono dos dados, opt-in/opt-out, acompanha histórico e benefícios. |
| **Time Neuron Premium** | Interpreta métricas anonimizadas e conduz intervenções humanas. |

### Inovação
- **Tecnológica**: IA emocional (valência, arousal), microsserviços Quarkus + React, dados anonimizados, AES-256 + SHA-512, OAuth2/SSO, integração com blockchain/Web3 para hashes imutáveis.
- **Ética**: privacidade by design, consentimento explícito, relatórios apenas para grupos ≥5 pessoas.
- **Social**: gamificação, tokenização de engajamento, selo Neuron de Cultura Saudável.
- **Mercado**: IA interpretativa aliada a especialistas humanos, foco em impacto real.

---

## Produto e Tecnologia

### Arquitetura
- **Back-end**: Java + Quarkus, APIs RESTful, JPA/Hibernate, Oracle Database com triggers, procedures e logs de consentimento.
- **Front-end**: React.js, prototipado no Figma (UX Writing + acessibilidade WCAG 2.1).
- **Segurança**: AES-256, SHA-512, OAuth 2.0/SSO, LGPD/GDPR compliance, blockchain para registros de consentimento/tokenização.
- **Infraestrutura**: Deploy contínuo via Render com CI/CD integrado ao GitHub, escalabilidade horizontal, monitoramento 24/7, backups automatizados.
- **Ferramentas Ágeis**: Trello + Scrum para gestão de sprint (backlog da sprint 1 prioriza fluxo do colaborador e coleta ética).

> **Links Operacionais**: inserir link do pitch e do board do Trello quando disponíveis.

### Preparação do ambiente local
1. **Requisitos**  
   - Python 3.12+ instalado (testado no Ubuntu 24.04).  
   - Acesso a um Oracle Database (ex.: `oracle.fiap.com.br:1521/orcl`).  
   - Git e um terminal com acesso a `bash`/PowerShell.
2. **Dependências de sistema (Linux)**  
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-venv
   ```
3. **Clonar o repositório e criar o virtualenv**  
   ```bash
   git clone https://github.com/Tiagozguedes/neuron.git
   cd neuron
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **Configurar o `.env`**  
   Copie o arquivo de exemplo e preencha com suas credenciais:
   ```bash
   cp .env.example .env
   # edite o .env com ORACLE_USER, ORACLE_PASSWORD, etc.
   ```
   O projeto já carrega automaticamente esse arquivo ao iniciar (via `python-dotenv`); certifique-se de que `.env` continue fora do Git.
5. **Variáveis de ambiente (alternativa ao `.env`)**  
   Se preferir, defina manualmente as variáveis no terminal:
   ```bash
   export ORACLE_USER=<seu_usuario>
   export ORACLE_PASSWORD=<sua_senha>
   export ORACLE_HOST=<host_oracle>
   export ORACLE_PORT=1521
   export ORACLE_SERVICE=<service_name>    # ou export ORACLE_SID=<sid>
   export NEURON_API_ENDPOINT=https://sua-api/api/v1/analises-emocionais
   export NEURON_API_KEY=<token_se_necessario>
   ```
   > **PowerShell (Windows):**
   > ```
   > setx ORACLE_USER <seu_usuario>
   > setx ORACLE_PASSWORD <sua_senha>
   > setx ORACLE_HOST <host_oracle>
   > setx ORACLE_PORT 1521
   > setx ORACLE_SERVICE <service_name>
   > ```

### Menu interativo (CRUD + relatórios)
Todo o fluxo exigido na disciplina pode ser executado por um único menu interativo. Após ativar o virtualenv, rode:

```bash
PYTHONPATH=src .venv/bin/python -m menu
```

O terminal exibirá opções claras para cada CRUD (usuários, departamentos, acessos, emoções, categorias, registros e respostas), reaproveitando as validações e tratamentos de exceção já presentes em `src/actors`. A opção **8** integra o check-in emocional com IA, enquanto a opção **9** abre o módulo de consultas/relatórios.

- Cada consulta acessa o Oracle com parâmetros preparados e traz indicadores relevantes (distribuição de colaboradores, ranking de emoções e panorama de bem-estar).
- Ao final de cada consulta o usuário decide se deseja exportar o resultado para JSON; os arquivos são salvos automaticamente na pasta `exports/` com timestamp, facilitando o envio das evidências da entrega.
- Todo o menu segue a mesma experiência de entrada validada + tratamento de erros (`try/except`) descrita no enunciado, centralizando a navegação em um loop `while` simples de entender.

### Fluxo de check-in com IA (CLI Python)
Para alinhar a prova de conceito com o modelo de negócio descrito acima, a pasta `src/actors` ganhou um fluxo interativo que permite que o colaborador descreva suas emoções em texto, envie o relato para a API de IA da Neuron e, em seguida, armazene o relatório no Oracle.

1. **Configuração**:
   - Configure as credenciais do banco Oracle via `ORACLE_USER`, `ORACLE_PASSWORD` e `ORACLE_DSN`.
   - Informe o endpoint da IA com `NEURON_API_ENDPOINT` (ex.: `https://neuron-api.onrender.com/api/v1/analises-emocionais`).
   - Se necessário, defina `NEURON_API_KEY` e ajuste o timeout (`NEURON_API_TIMEOUT`, padrão 15 s).
   - Instale as dependências: `pip install oracledb requests`.
2. **Execução**:
   - Rode `python -m actors.checkins`.
   - Informe o ID do colaborador já cadastrado em `T_NRON_USUARIO`, escreva o texto do check-in e confirme o envio.
3. **Resultado**:
   - O terminal exibe o relatório retornado pela IA (emoção predominante, métricas, recomendações).
   - Ao confirmar, cria-se uma linha em `T_NRON_RESP_FORMULARIO` e, quando possível, um vínculo com `T_NRON_REGIST_EMOCAO`, sustentando os dashboards e KPIs previstos no produto.

### Scripts de banco (Oracle)
- Utilize `sql/criar.sql` para provisionar o schema atualizado (tabelas, constraints e comentários).  
- Para resetar o ambiente de desenvolvimento, execute `sql/apagar.sql`, que derruba as tabelas na ordem correta.  
- Ambos os arquivos foram extraídos/adaptados do Oracle SQL Developer Data Modeler e refletem exatamente a estrutura esperada pelos CRUDs deste repositório.
- Preferir rodá-los via SQL Developer/SQL*Plus. Alternativamente, você pode executar ambos com Python após exportar as variáveis `ORACLE_*`:
  ```bash
  PYTHONPATH=src .venv/bin/python - <<'PY'
  from pathlib import Path
  from connect.connect import run_execute
  for arquivo in ('sql/apagar.sql','sql/criar.sql'):
      blocos = [linha for linha in Path(arquivo).read_text().split(';') if linha.strip()]
      for bloco in blocos:
          run_execute(bloco, {})
  PY
  ```

---

## Histórias, Requisitos e Regras

### Histórias de Usuário (3W)
1. **Colaborador** – realizar check-ins diários para receber recomendações de autocuidado.
2. **Gestor** – visualizar indicadores agregados para agir preventivamente.
3. **RH** – gerar relatórios anonimizados e acompanhar evolução emocional.
4. **Administrador** – configurar políticas de consentimento e segurança.
5. **Especialista Neuron** – interpretar padrões e propor workshops/intervenções humanas.

### Requisitos Funcionais
- Autenticação corporativa e integração com Slack/Teams/Notion.
- Check-ins emocionais diários em interface intuitiva.
- Recomendações automáticas baseadas nos dados de humor do usuário.
- Painéis agregados para gestor, RH e Time Neuron (sem dados individuais).
- Opt-out, exclusão de dados e registro auditável de consentimentos.
- Alertas de IA para aumentos coletivos de estresse.

### Requisitos Não Funcionais
- Latência < 3s e disponibilidade ≥ 99%.
- Criptografia em repouso e em trânsito, conformidade LGPD/GDPR.
- Acessibilidade WCAG 2.1 e escalabilidade horizontal.
- Backups automáticos, logs imutáveis e monitoramento contínuo.
- Código seguindo boas práticas (clean code + Git Flow).

### Regras de Negócio
- Relatórios apenas para grupos ≥3 pessoas; nenhum gestor ou RH vê dados individuais.
- Coletas sensíveis (facial/texto) exigem consentimento explícito.
- Colaborador pode excluir histórico a qualquer momento; anonimização após 12 meses.
- IA trabalha com dados agregados; não utilizada para avaliação individual.
- Empresas com bem-estar >80% recebem o Selo Neuron; intervenções humanas somente por gestores/RH autorizados.

---

## Mercado e Vantagem Competitiva

### Segmentos-alvo
- Tecnologia & inovação, saúde & educação, serviços financeiros, indústria & varejo.
- Público direto: RH, People Analytics e lideranças; público indireto: colaboradores participantes.

### Concorrência
| Player | Foco | Limitações |
| --- | --- | --- |
| Unmind | Conteúdo e trilhas de autocuidado | Não utiliza IA emocional anonimizadora. |
| Wellbees | Gamificação de hábitos | Não coleta contexto emocional. |
| Wellbeing.ai | Sensores biométricos + IA | Alto custo e pouca escalabilidade. |
| Emotion Logic | Análise de voz para call centers | Nicho restrito e monomodal. |

**Diferenciais Neuron**: IA ética + anonimização, engajamento com recompensas, integração com ferramentas de trabalho, custo acessível, selo ESG, atuação combinada entre IA e especialistas humanos.

---

## Plano de Investimento e ROI

### Premissas
- Hora técnica média: R$ 80; ~10h/mês por cliente.
- Infraestrutura (Render + Oracle Cloud): R$ 300/mês.
- Margem administrativa: 25% sobre o custo total.

### Retorno Estimado
- Redução de absenteísmo em 10% e turnover em 8%; aumento de engajamento em 12%.
- Exemplo (Plano Essencial, 200 colaboradores):
  - Custo: R$ 1.900/mês.
  - Economia: R$ 4.000/mês.
  - ROI ≈ 110% ao mês (payback < 1 mês).

---

## SLA e Suporte

- Disponibilidade: 99% mensal; manutenção planejada aos domingos das 02h às 06h.
- Suporte: resposta em até 4h úteis, resolução em até 24h (incidentes não críticos).
- Backups diários com retenção de 30 dias; logs auditáveis; monitoramento contínuo.
- Indisponibilidade >1% gera desconto proporcional; interrupções >4h resultam em crédito de 10%; reincidências permitem rescisão sem multa.
- Canais de atendimento: e-mail, chat interno, painel de tickets e chatbot/FAQ com escalonamento automático.

---

## Autores
- Anna Clara Russo Luca — RM 561928
- Gabriel Duarte Maciel — RM 565754
- Tiago Guedes da Costa — RM 564731

Turma 1TDSPW • Curso: Análise e Desenvolvimento de Sistemas.

---

> Juntos pela saúde emocional corporativa: tecnologia, ética e impacto social caminham juntos na Neuron.
