# Chef Marius V2

Aplicacao de receitas com IA generativa usando `Streamlit`, `LangChain` e `Groq`, com exportacao automatica de receitas em PDF e opcao de distribuicao desktop no Windows, gerando um '.exe' para ser executado em qualquer computador com windows.

## Resumo

O `Chef Marius V2` permite que o usuario envie perguntas culinarias em linguagem natural e receba respostas estruturadas (ingredientes, processo e referencias). A resposta pode ser salva como PDF em disco para consulta posterior.

A solucao tambem inclui empacotamento para executavel Windows com `PyInstaller` e inicializacao em janela desktop com `pywebview`.

## Principais capacidades

- Interface simples em `Streamlit` para interacao com LLM.
- Integracao com modelo `openai/gpt-oss-20b` via Groq.
- Historico de conversa em sessao (`st.session_state`).
- Geracao de PDF com `ReportLab`.
- Persistencia local de saida em `ReceitasGravadas/`.
- Build para distribuicao desktop sem necessidade de abrir navegador manualmente.

## Arquitetura do projeto

- `chefMariusV2.py`
Responsavel pela interface Streamlit, chamada ao modelo, gerenciamento de historico e geracao de PDF.

- `launcher.py`
Inicializa o servidor Streamlit e abre a aplicacao em janela desktop (`pywebview`), com fallback para navegador.

- `build_exe.py`
Script de empacotamento com `PyInstaller` no modo `--onedir`, incluindo assets e imports necessarios.

- `build_exe.bat`
Atalho para build no Windows.

- `ReceitasGravadas/`
Diretorio de saida dos arquivos PDF gerados pelo app.

## Requisitos

- Sistema operacional: Windows
- Python: 3.10 ou superior
- Chave de API Groq valida (ir em https://groq.com, registrar-se e criar uma groq api key grátis em https://console.groq.com/keys)

Dependencias principais:
- `streamlit`
- `langchain-core`
- `langchain-groq`
- `langchain-community`
- `groq`
- `reportlab`
- `requests`
- `pywebview`
- `pyinstaller`

## Instalacao

Na raiz do projeto (`C:\chefMariusV2`), execute:

```bash
pip install streamlit langchain-core langchain-groq langchain-community groq reportlab requests pywebview pyinstaller
```

## Execucao em desenvolvimento

```bash
streamlit run chefMariusV2.py
```

Fluxo recomendado:
1. Inicie a aplicacao.
2. Informe a `GROQ API Key` na barra lateral.
3. Digite a pergunta culinaria.
4. Clique em `Enviar`.
5. Consulte o PDF em `ReceitasGravadas/`.

## Build para executavel Windows

Opcao 1:

```bat
build_exe.bat
```

Opcao 2:

```bash
python build_exe.py
```

Saida esperada no modo atual (`--onedir`):
- `dist/chefMariusV2/chefMariusV2.exe`

Para distribuicao, copie a pasta inteira `dist/chefMariusV2/`.

## Comportamento de runtime no executavel

- O launcher sobe o Streamlit localmente na porta configurada (padrao `8501`).
- A aplicacao abre em janela desktop via `pywebview`.
- Diretorios de configuracao/cache do Streamlit sao criados ao lado do `.exe`.
- Em caso de falha no `pywebview`, ha fallback para navegador padrao.

## Persistencia de dados

Arquivos PDF sao gerados com timestamp para evitar sobrescrita:
- Padrao de nome: `<pergunta>_<YYYYMMDD_HHMM>.pdf`
- Pasta de saida: `ReceitasGravadas/`

## Troubleshooting rapido

- App nao responde apos iniciar:
Verifique se a porta `8501` esta livre ou ajuste `STREAMLIT_SERVER_PORT`.

- Erro de autenticacao no modelo:
Confirme se a `GROQ API Key` foi informada corretamente na interface.

- Build falha no PyInstaller:
Confirme instalacao de `pyinstaller` e execute o build na raiz do projeto.

- Executavel abre e fecha imediatamente:
Rode o `.exe` via terminal para capturar logs e validar dependencias locais.
