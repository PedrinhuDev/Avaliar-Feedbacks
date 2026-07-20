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

st.components.v1.html(
    """
    <script>
        window.parent.scrollTo(0, 0);
    </script>
    """,
    height=0
)

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
# AVALIAÇÕES JÁ REALIZADAS
# =====================

avaliacoes = worksheet.get_all_records()

quantidade_avaliacoes = len(avaliacoes)

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
    st.session_state.indice = quantidade_avaliacoes

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

with st.form(key=f"form_{st.session_state.indice}"):

    avaliacao = st.radio(
        "O feedback está correto?",
        [
            "Correto",
            "Parcialmente correto",
            "Incorreto"
        ],
        key=f"avaliacao_{st.session_state.indice}"
    )

    observacao = st.text_area(
        "Observações",
        key=f"observacao_{st.session_state.indice}"
    )

    salvar = st.form_submit_button("Salvar")

if salvar:

    worksheet.append_row([
        st.session_state.indice,
        int(linha["problem_id"]),
        str(linha["feedback"]),
        str(avaliacao),
        str(observacao),
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ])

    st.session_state.indice += 1

    st.rerun()
