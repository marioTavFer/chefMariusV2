# IA Generativa, LLM Para 'Receitas do Chef Marius' - Python com LangChain
# referencia: Data Science Academy (curso python - AI, Cap.14)
#
# based on a lesson(about LLM,SLM,RAG) from DataScienceAcademy.com.br
# I am using GROQ, (LLM), LangChain, 'openai/gpt-oss-20b', 
# Streamlit (web frontend), reportlab to recipes, 
# and a builder/launcher to create an exe to run 'ChefMarius' on any notebook
#


import os
import sys
import re
import logging
import warnings
from io import BytesIO
from datetime import datetime

import streamlit as st

# ReportLab

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
#
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# LangChain
# criação de prompts

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# mensagens usadas no contexto da conversa
from langchain_core.messages import SystemMessage, HumanMessage
# conector ChatGroq
from langchain_groq import ChatGroq
# callbacks pelo streamlit
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# avoid warnings and loggers from Streamlit
# Suprimir warnings inofensivos e loggers do Streamlit

warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")
logging.getLogger('streamlit.runtime.scriptrunner_utils.script_run_context').setLevel(logging.ERROR)
logging.getLogger('streamlit').setLevel(logging.ERROR)

# create local files and it is ready to work with pyinstaller to deploy anywhere (with .exe)
# cria pasta para arquivos locais salvos
# Funciona tanto com .py quanto com .exe (PyInstaller)

if getattr(sys, 'frozen', False):
    # Executando como .exe (PyInstaller)
    # _MEIPASS é para recursos read-only (fonts, assets)
    base_dir = sys._MEIPASS
    # Para salvar arquivos, usar o diretório do executável (não o temp _MEIPASS)
    exe_dir = os.path.dirname(sys.executable)
else:
    # Executando como script Python
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe_dir = base_dir

# SAVE_DIR usa exe_dir para que os arquivos persistam após fechar o app

SAVE_DIR = os.path.join(exe_dir, "ReceitasGravadas")
os.makedirs(SAVE_DIR, exist_ok=True)

# cria timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M")


# Define as configurações iniciais da página do Streamlit (título, ícone e layout)

st.set_page_config(page_title = "Receitas", page_icon = "🍷", layout = "wide")

# Cria a barra lateral do app com elementos de configuração

with st.sidebar:
    st.header("Config")
    api_key = st.text_input("Digite sua GROQ API Key e Enter", type = "password")
    st.divider()
    st.subheader("Instruções")
    st.write("1) Informe sua API_KEY no campo acima.\n2) Digite sua pergunta ou dúvida.\n3) Clique em Enviar.")

# emogi: https://getemoji.com/#activities
# Show Titles / Exibe os títulos principais e subtítulo do app

st.title("Test-drive de receitas com IA V2.0.MLTF")
st.title("👩🏼‍🍳 Chef Marius's Recipes")

# Groq + LangChain - LLM para Consultoria
# shows the defined model - # Exibe o modelo utilizado

st.caption("Modelo: openai/gpt-oss-20b via Groq + LangChain")

# minha api_key para testes
# api_key = ""

# check if API_KEY from Groq is available
# Verifica se a chave de API foi informada; se não, interrompe a execução

if not api_key:
    st.warning("Informe a GROQ API Key na barra lateral para começar.")
    st.stop()

# Armazena a chave informada na variável de ambiente para uso pela API Groq

os.environ["GROQ_API_KEY"] = api_key

# Inicializa o modelo de linguagem via ChatGroq com parâmetros de temperatura e limite de tokens

dsa_llm = ChatGroq(model = "openai/gpt-oss-20b", temperature = 0.2, max_tokens = 1024)

# Define o prompt base com orientações de escrita, apresentação e referências.
# also ready to adapt to the english version

system_block = """ Você é um cozinheiro profissional que escreve de forma objetiva e clara. Apresente as receitas de cozinha, com ingredientes, quantidades e formas de preparo.
Verifique as informações com consultas em várias origens, apresentando no mínimo 5 referências. Estruture a resposta com: tabela de ingredientes, tabela dos processos a executar com descrição do processo, quantidades e tempo. """

system_block2 = """ You are a professional cook who writes objectively and clearly. Present the cooking recipes, with ingredients, quantities, and preparation methods.
Verify the information by consulting various sources, presenting at least 5 references. Structure the answer with: a table of ingredients, a table of the processes to be executed with a description of the process, quantities, and time. """

# Cria o template de prompt para conversas, incluindo o bloco de sistema e o histórico

dsa_prompt = ChatPromptTemplate.from_messages(
    [
        # Define a mensagem de sistema com as instruções do assistente
        SystemMessage(content = system_block),
        
        # Placeholder para armazenar o histórico da conversa
        MessagesPlaceholder(variable_name = "history"),
        
        # Define a mensagem humana padrão com formatação da pergunta
        ("human", "Pergunta: {pergunta}\nResponda de forma sucinta, técnica e didática.")
    ]
)

# ReportLab - create the pdf of the recipe/grava arquivo PDF da receita
    # function to generate a pdf with the cooking recipe or other docs with tables

def cria_pdf (pdf_path, content):
    try:
        # Create PDF with the response
        doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=36, bottomMargin=36, leftMargin=72, rightMargin=72)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Arquivo do Chef Consultor - IA", styles['Heading2']))
        story.append(Spacer(1, 6))

        # Parse content for multiple tables and text
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            # Collect text until table
            text_lines = []
            while i < len(lines) and not lines[i].strip().startswith('|'):
                text_lines.append(lines[i])
                i += 1
            if text_lines:
                text = '\n'.join(text_lines).strip()
                if text:
                    text_html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
                    text_html = text_html.replace('\n', '<br/>')
                    story.append(Paragraph(text_html, styles['Normal']))
                    story.append(Spacer(1, 6))

            if i < len(lines) and lines[i].strip().startswith('|'):
                # Parse table
                header = [Paragraph(re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', cell.strip()), styles['Normal']) for cell in lines[i].split('|')[1:-1]]
                i += 1
                # Skip separator if present
                if i < len(lines) and all('---' in cell for cell in lines[i].split('|')[1:-1]):
                    i += 1
                rows = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    cells = [re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', cell.strip()) for cell in lines[i].split('|')[1:-1]]
                    if len(cells) == len(header):
                        rows.append(cells)
                    i += 1
                if rows:
                    data = [header] + [[Paragraph(cell, styles['Normal']) for cell in row] for row in rows]
                    table = Table(data, colWidths=[100, 200, 150])
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0,0), (-1,0), 10),
                        ('BOTTOMPADDING', (0,0), (-1,0), 6),
                        ('BACKGROUND', (0,1), (-1,-1), colors.white),
                        ('GRID', (0,0), (-1,-1), 1, colors.black),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 1), (-1, -1), 8),
                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ('LEFTPADDING', (0,0), (-1,-1), 3),
                        ('RIGHTPADDING', (0,0), (-1,-1), 3),
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 6))
        doc.build(story)
        st.info(f"Consulta gravada em: `{SAVE_DIR}`")
    except Exception as e:
        print(f"Error creating PDF: {e}") 

# Streamlit - Formulário de Pergunta e Processamento da Resposta
# start historical data from conversation
# Inicializa o histórico da conversa, caso ainda não exista na sessão

if "history" not in st.session_state:
    st.session_state.history = []

# form to send the question
# Streamlit - Cria um formulário para envio da pergunta

with st.form("form"):
    
    # Campo de texto para digitar a pergunta 
    pergunta = st.text_area("Pergunta", height = 120, placeholder = "Digite sua dúvida sobre culinária aqui...")
    
    # Botão para enviar o formulário
    enviado = st.form_submit_button("Enviar")

# Executa o processamento quando o botão "Enviar" for clicado

if enviado:
    
    # generate messages with log data. Gera as mensagens com base no histórico e na nova pergunta
    msgs = dsa_prompt.invoke({"history": st.session_state.history, "pergunta": pergunta})
    
    # Invoca o modelo de linguagem para gerar a resposta
    resp = dsa_llm.invoke(msgs.to_messages())
    
    # update historical data from session. Atualiza o histórico da sessão com a pergunta e a resposta do modelo
    st.session_state.history.extend(
        [
            HumanMessage(content = f"Pergunta: {pergunta}"), resp
        ]
    )
  
    # show the title "Answer"
    st.markdown("### Resposta")
    
    # show the answer
    st.write(resp.content)

    # save locally
    # first see the len() of the question to limit the name of the file
    max_len_filename = 70
    if len(pergunta) > max_len_filename:
        pergunta_lim = pergunta[:max_len_filename]
    else:
        pergunta_lim = pergunta
        
    content = resp.content
    pdf_path = os.path.join(SAVE_DIR, f"{pergunta_lim}_{timestamp}.pdf")
    cria_pdf (pdf_path, content)
 



