# Chef Marius V2

Aplicação de geração de receitas com IA generativa usando `Streamlit`, `LangChain` e `Groq`, com exportação automática de receitas em PDF e opção de distribuição desktop no Windows, gerando um '.exe', para ser executado em qualquer computador com windows.

## Resumo

O `Chef Marius V2` permite que o usuário envie perguntas culinárias em linguagem natural e receba respostas estruturadas (ingredientes, processo e referências). A resposta é salva como PDF em disco para consulta posterior.

A solução também inclui empacotamento para executável Windows com `PyInstaller` e inicialização em janela desktop com `pywebview`.

## Principais capacidades

- Interface simples em `Streamlit` para interação com LLM.
- Integração com modelo `openai/gpt-oss-20b` via Groq.
- Histórico de conversa em sessão (`st.session_state`).
- Geração de PDF com `ReportLab`.
- Persistência local de saída em `ReceitasGravadas/`.
- Build para distribuição desktop e sem a necessidade de abrir navegador manualmente.

## Arquitetura do projeto

- `chefMariusV2.py`
Responsável pela interface Streamlit, chamada ao modelo, gerenciamento de histórico e geração de PDF.

- `launcher.py`
Inicializa o servidor Streamlit e abre a aplicação em janela desktop (`pywebview`), com fallback para navegador.

- `build_exe.py`
Script de empacotamento com `PyInstaller` no modo `--onedir`, incluindo assets e imports necessários.

- `build_exe.bat`
Atalho para build no Windows.

- `ReceitasGravadas/`
Diretório de saída dos arquivos PDF gerados pelo app.

## Requisitos

- Sistema operacional: Windows
- Python: 3.10 ou superior
- Chave de API Groq válida (ir em https://groq.com, registrar-se e criar uma groq api key grátis em https://console.groq.com/keys)

Dependências principais:
- `streamlit`
- `langchain-core`
- `langchain-groq`
- `langchain-community`
- `groq`
- `reportlab`
- `requests`
- `pywebview`
- `pyinstaller`

## Instalação

Na raiz do projeto (`C:\chefMariusV2`), execute:

```bash
pip install streamlit langchain-core langchain-groq langchain-community groq reportlab requests pywebview pyinstaller
```

## Execução em desenvolvimento

```bash
streamlit run chefMariusV2.py
```

Fluxo recomendado:
1. Inicie a aplicação.
2. Informe a `GROQ API Key` na barra lateral.
3. Digite a pergunta culinária.
4. Clique em `Enviar`.
5. Consulte o PDF em `ReceitasGravadas/`.

## Build para executável Windows

Opção 1:

```bat
build_exe.bat
```

Opção 2:

```bash
python build_exe.py
```

Saída esperada no modo atual (`--onedir`):
- `dist/chefMariusV2/chefMariusV2.exe`

Para distribuição, copie a pasta inteira `dist/chefMariusV2/`.

## Comportamento de runtime no executável

- O launcher sobe o Streamlit localmente na porta configurada (padrao `8501`).
- A aplicação abre em janela desktop via `pywebview`.
- Diretórios de configuração/cache do Streamlit são criados ao lado do `.exe`.
- Em caso de falha no `pywebview`, há fallback para navegador padrão.

## Persistência de dados

Arquivos PDF são gerados com timestamp para evitar sobrescrita:
- Padrão de nome: `<pergunta>_<YYYYMMDD_HHMM>.pdf`
- Pasta de saída: `ReceitasGravadas/`

## Troubleshooting rápido

- App não responde após iniciar:
Verifique se a porta `8501` está livre ou ajuste `STREAMLIT_SERVER_PORT`.

- Erro de autenticação no modelo:
Confirme se a `GROQ API Key` foi informada corretamente na interface.

- Build falha no PyInstaller:
Confirme instalação de `pyinstaller` e execute o build na raíz do projeto.

- Executável abre e fecha imediatamente:
Rode o `.exe` via terminal para capturar logs e validar dependências locais.
