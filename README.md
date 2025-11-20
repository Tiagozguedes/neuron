# Neuron – Inteligência Emocional Corporativa

CLI em Python para registrar emoções, analisar relatos de colaboradores e gerar relatórios para RH/gestão, com dados salvos em Oracle.

## Resumo e propósito
Empresas precisam acompanhar o bem-estar emocional de forma contínua, mas os sinais costumam ficar dispersos e sem padronização, o que impede ação preventiva sem violar privacidade. O Neuron é um console administrativo em Python que centraliza cadastros, check-ins emocionais e consultas agregadas. Ele dá visibilidade segura ao bem-estar dos colaboradores: cada relato é analisado localmente (offline), convertido em métricas e armazenado no Oracle. Os CRUDs mantêm dados consistentes; o fluxo de check-in coleta o relato, aplica a análise emocional e grava registros; e os módulos de consulta geram indicadores (com exportação JSON) que podem alimentar dashboards corporativos sem expor dados individuais.

## O que o projeto entrega
- CRUDs de usuários, acessos, departamentos, emoções, categorias, registros emocionais e respostas de formulário.
- Check-in emocional guiado: coleta relato, roda análise local (offline) e armazena métricas.
- Relatórios prontos com exportação em JSON (`exports/<consulta>_<timestamp>.json`).

## Pré-requisitos
- Python 3.12+
- Oracle disponível (ex.: `oracle.fiap.com.br:1521/orcl`)
- Dependências: `pip install -r requirements.txt`

Variáveis de ambiente (via `.env` ou export):
```
ORACLE_USER=<usuario>
ORACLE_PASSWORD=<senha>
ORACLE_HOST=oracle.fiap.com.br
ORACLE_PORT=1521
ORACLE_SERVICE=orcl
```

## Como usar
### Menu administrativo (CRUD + relatórios)
```
PYTHONPATH=src python -m menu          # Linux/macOS
set PYTHONPATH=src & python -m menu    # CMD
$env:PYTHONPATH="src"; python -m menu  # PowerShell
```
Navegue pelas opções numeradas; use `voltar` ou `0` para cancelar qualquer fluxo.

### Check-in emocional
```
PYTHONPATH=src python -m actors.checkins
```
1) Informe o ID do colaborador.  
2) Digite o relato (múltiplas linhas).  
3) Revise o relatório (emoção predominante, distribuição, motivação/felicidade/estresse/saúde mental) e confirme o salvamento.

## Análise emocional local
- Perfis configuráveis em `src/services/analise_emocional_local.py` (~15 emoções com vocabulário/expressões/pesos). Um texto pode acionar várias emoções.
- `src/services/analise_emocional.py` gera `EmotionReport` com métricas 0–100 (motivação, felicidade, estresse, energia, saúde mental) e insights.
- Tudo roda offline; ajuste palavras-chave e pesos conforme a cultura da empresa.

## Consultas e exportação
Módulo `src/actors/consultas.py` (menu “Relatórios e Consultas”) chama `src/services/relatorios.py` e permite exportar cada resultado:
- Ranking de emoções mais registradas.
- Colaboradores por departamento (ativos/inativos).
- Médias de motivação/felicidade/estresse/saúde mental por departamento.
- Tendência temporal (dia/semana/mês) das métricas.
- Emoções predominantes por período (com filtro opcional por departamento).
- Ranking de estresse por departamento (com mínimo de check-ins para preservar privacidade).

## Mapa rápido dos arquivos
- `src/menu.py`: entrada principal e menus.
- `src/actors/*.py`: CRUDs, consultas e fluxo de check-in.
- `src/services/*.py`: análise emocional, persistência transacional e relatórios.
- `src/connect/connect.py` e `src/db_utils.py`: conexão Oracle e helpers SQL.
- `sql/`: criação/carga de tabelas.
- `exports/`: JSONs gerados (há um exemplo na pasta).

## Notas finais
- Todos os fluxos validam entradas e suportam cancelamento (`voltar`/`0`).
- Projeto 100% console para demos rápidas; textos podem ser adaptados à cultura da empresa.
