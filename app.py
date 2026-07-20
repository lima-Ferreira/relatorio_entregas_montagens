import streamlit as st
from PIL import Image
import os


from session import iniciar_sessao, limpar_dados

from componentes.cards import (
    cards_dashboard,
    cards_entregas,
    cards_montagens
)


from modulos.entregas import tela_entregas


try:
    from modulos.montagens import tela_montagens
except:

    tela_montagens=None



st.set_page_config(

    page_title="Gestão Empresarial",

    page_icon="🚚",

    layout="wide"

)



# inicia memória

iniciar_sessao()



# LOGO

logo="assets/Logo.bmp"


if os.path.exists(logo):

    st.sidebar.image(
        Image.open(logo),
        width=180
    )



st.sidebar.divider()



pagina = st.sidebar.radio(

    "Menu",

    [

        "🏠 Dashboard",

        "🚚 Entregas",

        "🔨 Montagens"

    ]

)



st.sidebar.divider()


if st.sidebar.button("🗑 Limpar Dados"):

    limpar_dados()

    st.success(
        "Dados limpos!"
    )



# ===================
# DASHBOARD
# ===================


if pagina=="🏠 Dashboard":


    st.title(
        "📊 Dashboard Geral"
    )


    cards_dashboard()



# ===================
# ENTREGAS
# ===================


elif pagina=="🚚 Entregas":


    st.title(
        "🚚 Controle de Entregas"
    )


    cards_entregas()


    st.divider()


    tela_entregas()



# ===================
# MONTAGENS
# ===================


elif pagina=="🔨 Montagens":


    st.title(
        "🔨 Controle de Montagens"
    )


    cards_montagens()


    st.divider()


    if tela_montagens:

        tela_montagens()    