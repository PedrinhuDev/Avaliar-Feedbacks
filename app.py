import streamlit as st
import pandas as pd
import os
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

    nova_avaliacao = pd.DataFrame({
        "problem_id": [linha["problem_id"]],
        "feedback": [linha["feedback"]],
        "avaliacao": [avaliacao],
        "observacao": [observacao],
        "data_hora": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })

    if os.path.exists(arquivo_avaliacoes):

        nova_avaliacao.to_csv(
            arquivo_avaliacoes,
            mode="a",
            header=False,
            index=False
        )

    else:

        nova_avaliacao.to_csv(
            arquivo_avaliacoes,
            index=False
        )

    st.success("Avaliação salva com sucesso!")

    st.session_state.indice += 1

    st.rerun()