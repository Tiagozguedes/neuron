# Neuron – Inteligência Emocional Corporativa

Plataforma em Python que conecta colaboradores a uma IA de análise emocional, oferecendo insights de bem-estar para líderes e RH com anonimização e foco em cultura saudável.

## Visão geral do projeto
Neuron nasceu da necessidade das empresas brasileiras de medir e cuidar da saúde emocional sem violar privacidade. O sistema funciona como um console administrativo para o time de RH/People Analytics cadastrar usuários, departamentos e emoções, executar consultas e disparar check-ins guiados por IA. Cada relato enviado pela CLI é interpretado localmente por regras heurísticas simples e salvo no Oracle para alimentar dashboards corporativos.

## Onde o Neuron se encaixa na empresa
- **Colaboradores** registram sentimentos no check-in guiado e recebem recomendações personalizadas.
- **Gestores e RH** acompanham indicadores agregados gerados pelas consultas e priorizam ações preventivas.
- **Time Neuron** mantém a governança e garante aderência à LGPD, já que nenhum dado individual é exposto fora do workflow autorizado.

### Por que ele é importante
- Reduz absenteísmo e turnover ao sinalizar aumentos de estresse antes de crises.
- Apoia programas ESG e políticas de bem-estar com evidências objetivas.
- Simboliza transparência e ética: o colaborador controla seus dados e tudo é logado em banco corporativo.

## Funcionalidades principais
- Menu único com CRUDs para usuários, departamentos, acessos, emoções, categorias, registros emocionais e respostas de formulário.
- Fluxo de check-in emocional (opção 8) que coleta texto, aplica uma análise emocional local e grava as métricas retornadas.
- Módulo de consultas (opção 9) com exportação automática em `exports/<consulta>-<timestamp>.json`.
- Integração com Oracle Database (persistência) e motor de análise emocional local (sem dependências externas).

## Requisitos para rodar
- Python 3.12+ e `pip`.
- Oracle Database acessível (por exemplo `oracle.fiap.com.br:1521/orcl`) e credenciais válidas.
- Dependências Python: `oracledb`, `python-dotenv` (instaladas via `pip install -r requirements.txt`).

## Preparando o ambiente
1. Clone o repositório e crie um virtualenv (opcional, mas recomendado):
   ```bash
   git clone https://github.com/Tiagozguedes/neuron.git
   cd neuron
   python -m venv .venv
   source .venv/bin/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Configure as variáveis no `.env` (use `.env.example` como referência) ou exporte manualmente:
   ```bash
   export ORACLE_USER=<usuario>
   export ORACLE_PASSWORD=<senha>
   export ORACLE_HOST=oracle.fiap.com.br
   export ORACLE_PORT=1521
   export ORACLE_SERVICE=orcl
   ```
   > **Windows:** `setx NOME_VARIAVEL valor` grava permanentemente. Para sessões temporárias use `set NOME=valor` (CMD) ou `$env:NOME="valor"` (PowerShell).

## Análise emocional local
- A CLI utiliza `src/services/analise_emocional_local.py`, que agora possui perfis configuráveis para 15 emoções (Feliz, Esperançoso, Sereno, Cansado, Estressado, Ansioso etc.), cada uma com vocabulário, expressões e pesos específicos. Um mesmo texto pode ativar múltiplas emoções simultaneamente (por exemplo “cansado porém esperançoso” gera duas contribuições).
- O módulo `src/services/analise_emocional.py` transforma o resultado bruto em um `EmotionReport` completo, consolidando distribuição de emoções/sentimentos e calculando métricas numéricas (motivação, felicidade, estresse, energia e saúde mental) em escala 0–100.
- Tudo roda offline e continua simples de ajustar: basta editar as palavras-chave dos perfis ou os pesos-base definidos nos serviços para calibrar o comportamento aos termos usados pela empresa.

## Executando
### 1. Menu administrativo (CRUD + relatórios)
```bash
PYTHONPATH=src python -m menu          # Linux/macOS
set PYTHONPATH=src & python -m menu    # CMD
$env:PYTHONPATH="src"; python -m menu # PowerShell
```
A CLI mostra todas as opções numeradas. Cada entrada do CRUD valida os dados e descreve claramente o que será armazenado (por exemplo, o status do usuário pede “A=Ativo ou I=Inativo”).
- Os relatórios agregados agora contam com:
  - tendência temporal de motivação/felicidade/estresse (dias, semanas ou meses);
  - ranking de emoções por período com filtro opcional por departamento;
  - ranking de estresse por departamento com salvamento em JSON direto na pasta `exports/`.
- Em qualquer menu ou formulário você pode digitar `voltar` (`sair`, `0`, `cancelar`, `exit` também funcionam) para cancelar imediatamente o fluxo atual e retornar ao nível anterior.

### 2. Fluxo de check-in emocional
```bash
PYTHONPATH=src python -m actors.checkins
```
1. Informe o ID do colaborador já cadastrado.
2. Escreva o relato emocional (múltiplas linhas).
3. O CLI roda a análise emocional local, exibe o relatório simplificado (emoção + métricas derivadas) e, ao confirmar, grava os dados em `T_NRON_RESP_FORMULARIO` e `T_NRON_REGIST_EMOCAO`.

## Estrutura dos módulos
| Pasta/Arquivo | Papel no projeto |
| --- | --- |
| `src/menu.py` | Loop principal com as nove opções do sistema. |
| `src/actors/usuarios.py` | CRUD de colaboradores, com validação explícita de status (Ativo/Inativo). |
| `src/actors/departamentos.py` | Cadastro de áreas/departamentos corporativos. |
| `src/actors/acessos.py` | Perfis de acesso (Funcionário, Gestor, RH etc.). |
| `src/actors/emocoes.py` e `categorias_emocao.py` | Tabelas de emoções e categorias que sustentam os relatórios. |
| `src/actors/registros_emocao.py` e `respostas_formulario.py` | Histórico das leituras emocionais e dos formulários preenchidos. |
| `src/actors/checkins.py` | Orquestra o check-in, aplica a análise local e persiste no Oracle. |
| `src/services/analise_emocional.py` | Normaliza o resultado da heurística e gera métricas consolidadas. |
| `src/services/analise_emocional_local.py` | Perfis e pesos da análise emocional local. |
| `src/services/relatorios.py` | Camada de serviços para os relatórios agregados (tendência temporal, ranking de emoções etc.). |
| `src/services/checkin_service.py` | Responsável por persistir respostas/emoções no Oracle com transações. |
| `src/connect/connect.py` | Wrapper de conexão com Oracle (usa variáveis de ambiente carregadas via `python-dotenv`). |

## Observações finais
- Scripts SQL para criar/dropar tabelas estão em `sql/` caso precise provisionar o banco do zero.
- O projeto roda inteiramente em modo console para facilitar demonstrações rápidas em sala ou apresentações para RH.
- Sinta-se à vontade para adaptar os textos do menu para a cultura da empresa contratante ou integrar novos relatórios a partir das consultas existentes.
