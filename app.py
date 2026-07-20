import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================

st.set_page_config(
    page_title="Avaliação de Feedbacks",
    layout="wide"
)

st.title("Avaliação de Feedbacks Gerados por LLM")

# =====================
# CONEXÃO COM GOOGLE SHEETS
# =====================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

planilha = client.open_by_key(
    "1_uo0DrYh-VSguix163r5zsV9n5noG_ROwFN44RyG2ls"
)

worksheet = planilha.worksheet("Página1")

# =====================
# CARREGAMENTO DOS DADOS
# =====================

df = pd.read_csv("feedbacks_prompt_unico - Página1.csv")

# Filtra apenas respostas incorretas
df["status_is_correct"] = df["status_is_correct"].astype(str)
df = df[df["status_is_correct"] == "False"]

# Reorganiza os índices
df = df.reset_index(drop=True)

# =====================
# CONTROLE DO REGISTRO
# =====================

if "indice" not in st.session_state:
    st.session_state.indice = 0

# Caso todas as avaliações tenham terminado
if st.session_state.indice >= len(df):
    st.success("✅ Todas as avaliações foram concluídas!")
    st.stop()

linha = df.iloc[st.session_state.indice]

# =====================
# PROGRESSO
# =====================

st.write(f"### Feedback {st.session_state.indice + 1} de {len(df)}")

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

observacao = st.text_area("Observações")

# =====================
# BOTÃO SALVAR
# =====================

if st.button("Salvar"):

    st.write(type(linha["problem_id"]))
    st.write(type(linha["feedback"]))
    st.write(type(avaliacao))
    st.write(type(observacao))

    worksheet.append_row([
        linha["problem_id"],
        linha["feedback"],
        avaliacao,
        observacao,
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ])

    st.success("Avaliação salva com sucesso!")

    st.session_state.indice += 1

    st.rerun()