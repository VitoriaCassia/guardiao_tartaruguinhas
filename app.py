# app.py - Guardião das Tartaruguinhas (versão final demonstrativa)

import streamlit as st
from PIL import Image
import os
import json

st.set_page_config(layout="wide")

# =============================== CONFIGURAR ESTILO GLOBAL ===============================
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #fefae0;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }
        h1, h2, h3, .stTextInput > label, .stSelectbox > label {
            font-size: 1.2rem;
        }
        .centered-text {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

DADOS_ARQUIVO = "ninhos.json"

# =============================== CARREGAR/SALVAR DADOS ===============================
def carregar_ninhos():
    if os.path.exists(DADOS_ARQUIVO):
        with open(DADOS_ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_ninhos(lista):
    with open(DADOS_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

# =============================== VERIFICAR IMAGEM ===============================
def carregar_imagem(caminho):
    if os.path.exists(caminho):
        st.image(caminho, width=533)
    else:
        st.warning(f"Imagem '{caminho}' não encontrada.")

# =============================== BOTÃO PDF FAKE ===============================
def mostrar_botao_pdf():
    st.button("Exportar PDF (em breve)")

# =============================== TELA CADASTRAR ===============================
def tela_cadastrar():
   
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        carregar_imagem("tela_cadastrar_marcada.png")
    with col2:
        st.markdown("<h2 class='centered-text'>Cadastrar novo ninho</h2>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.number_input("Qtde de ovos:", min_value=0, value=0, disabled=True)
        with col_b:
            st.number_input("Dias p/ eclosão:", min_value=0, value=0, disabled=True)


        regiao = st.selectbox("Região:", [""],disabled=True)
        status = st.selectbox("Status dos ovos:", [""], disabled=True)
        risco = st.selectbox("Nível de risco de alagamento:", [""], disabled=True)
        predadores = st.selectbox("Predadores por perto?:", [""], disabled=True)


        col_bot1, col_bot2 = st.columns(2)
        with col_bot1:
            st.button("Salvar ninho", disabled=True)
        with col_bot2:
            if st.button("Voltar"):
                st.session_state.tela = "menu"

# =============================== TELA RELATÓRIO ===============================
def tela_relatorio():
    ninhos = carregar_ninhos()
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        carregar_imagem("tela_relatorio_marcada.png")
    with col2:

        st.write("\n")
        st.markdown("<h2 class='centered-text'>Relatório completo dos ninhos</h2>", unsafe_allow_html=True)
        st.write("\n")
        
        for n in ninhos:
            st.write(f"Número do ninho: {n['id']} | {n['regiao']} | {n['ovos']} ovos | {n['status']} | {n['risco']} | {n['dias']} dias | Predadores: {n['predadores']}")
        col_pdf, col_voltar = st.columns(2)
       # with col_pdf:
         #   mostrar_botao_pdf()
        with col_voltar:
            if st.button("Voltar"):
                st.session_state.tela = "menu"

# =============================== TELA ESTATÍSTICA ===============================

def tela_estatistica():
    ninhos = carregar_ninhos()
    total = len(ninhos)
    media_ovos_estaveis = sum(n['ovos'] for n in ninhos if 'Estável' in n['risco']) / max(1, len([n for n in ninhos if 'Estável' in n['risco']]))
    prestes_eclodir = len([n for n in ninhos if n['dias'] <= 5])
    mais_risco = max(set(n['regiao'] for n in ninhos if 'Crítico' in n['risco']), default='N/A', key=lambda r: sum(1 for n in ninhos if n['regiao'] == r and 'Crítico' in n['risco']))
    predadores = len([n for n in ninhos if n['predadores'] == 'Sim'])
    danificados = len([n for n in ninhos if n['status'] == 'Danificado'])

    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        carregar_imagem("tela_estatistica_marcada.png")
    with col2:

        st.write("\n")
        st.markdown("<h2 class='centered-text'>Estatística de Monitoramento dos ninhos</h2>", unsafe_allow_html=True)
        st.write("\n")
        
        st.write(f"📌 Total de ninhos......................: {total}")
        st.write(f"🟢 Média de ovos em ninhos estáveis....: {media_ovos_estaveis:.1f}")
        st.write(f"🐣 Ninhos prestes a eclodir............: {prestes_eclodir}")
        st.write(f"📍 Região com mais risco crítico.......: {mais_risco}")
        st.write(f"🦎 Ninhos com predadores...............: {predadores}")
        st.write(f"⚠️ Ninhos danificados...................: {danificados}")
        col_pdf, col_voltar = st.columns(2)
      #  with col_pdf:
      #      mostrar_botao_pdf()
        with col_voltar:
            if st.button("Voltar"):
                st.session_state.tela = "menu"

# =============================== TELA SAIR ===============================
def tela_sair():
    st.markdown("""
            <div style='text-align: center; padding-top: 50px;'>
            <h2>👋 Parabéns! Missão concluída com sucesso!</h2>
            <p style='font-size: 25px;'>Obrigado por proteger nossas tartaruguinhas. Até logo!</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Sair"):
        st.stop()

# =============================== TELA INICIAL ===============================
def tela_inicial():
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        carregar_imagem("tela_inicial_marcada.png")
    with col2:

        st.write("\n")
        st.markdown("## Monitoramento Comunitário de Ninhos")
        st.write("\n")

        opcoes = {
            "Cadastrar novo ninho": "cadastrar",
            "Relatório de ninhos": "relatorio",
            "Estatísticas": "estatistica",
            "Sair do sistema": "sair"
        }
        for nome, tela in opcoes.items():
            if st.button(nome):
                for key in list(st.session_state.keys()):
                    if key != "tela":
                        del st.session_state[key]
                st.session_state.tela = tela

# =============================== FLUXO PRINCIPAL ===============================
if 'tela' not in st.session_state:
    st.session_state.tela = "menu"

if st.session_state.tela == "menu":
    tela_inicial()
elif st.session_state.tela == "cadastrar":
    tela_cadastrar()
elif st.session_state.tela == "relatorio":
    tela_relatorio()
elif st.session_state.tela == "estatistica":
    tela_estatistica()
elif st.session_state.tela == "sair":
    tela_sair()
