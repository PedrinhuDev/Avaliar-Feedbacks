import streamlit as st
import pandas as pd
#import gspread
#from google.oauth2.service_account import Credentials

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================

st.set_page_config(
    page_title="Avaliação de Feedbacks",
    layout="wide"
)

st.title("Avaliação de Feedbacks Gerados por LLM")

# =====================
# CARREGAMENTO DOS DADOS
# =====================

sheet_id = "1sNv3ZqjwnKBWtMCfLrTtSdPqAWm0-lVFqG2dOapN2uU"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

df = pd.read_csv("feedbacks_prompt_unico - Página1.csv")

# =====================
# SELEÇÃO DO REGISTRO
# =====================

indice = st.number_input(
    "Selecione o registro",
    min_value=0,
    max_value=len(df)-1,
    value=0
)

linha = df.iloc[indice]

# =====================
# QUESTÃO
# =====================

st.subheader("Questão")

st.write(linha["problem"])

# =====================
# RESPOSTA DO ESTUDANTE
# =====================

st.subheader("Resposta do Estudante")

st.code(
    linha["solution"],
    language="python"
)

# =====================
# FEEDBACK DO LLM
# =====================

st.subheader("Feedback Gerado")

st.write(linha["feedback"])

# =====================
# AVALIAÇÃO
# =====================

st.subheader("Avaliação do Professor")

avaliacao = st.radio(
    "O feedback está correto?",
    [
        "Correto",
        "Parcialmente correto",
        "Incorreto"
    ]
)

observacao = st.text_area(
    "Observações"
)

st.button("Salvar")