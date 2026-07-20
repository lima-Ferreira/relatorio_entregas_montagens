import streamlit as st


def iniciar_sessao():

    if "entregas" not in st.session_state:

        st.session_state.entregas = {
            "quantidade": 0,
            "valor": 0.0,
            "motoristas": 0,
            "ajudantes": 0,
            "dados": None
        }


    if "montagens" not in st.session_state:

        st.session_state.montagens = {
            "quantidade": 0,
            "valor": 0.0,
            "montadores": 0,
            "dados": None
        }



def limpar_dados():

    st.session_state.entregas = {
        "quantidade": 0,
        "valor": 0.0,
        "motoristas": 0,
        "ajudantes": 0,
        "dados": None
    }


    st.session_state.montagens = {
        "quantidade": 0,
        "valor": 0.0,
        "montadores": 0,
        "dados": None
    }