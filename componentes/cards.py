import streamlit as st



def cards_dashboard():

    entrega = st.session_state.entregas
    montagem = st.session_state.montagens


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "🚚 Entregas",
            entrega["quantidade"]
        )


    with c2:

        st.metric(
            "🔨 Montagens",
            montagem["quantidade"]
        )


    with c3:

        st.metric(
            "💰 Valor Entregas",
            f'R$ {entrega["valor"]:,.2f}'
        )


    with c4:

        st.metric(
            "💰 Valor Montagens",
            f'R$ {montagem["valor"]:,.2f}'
        )





def cards_entregas():

    dados = st.session_state.entregas


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "🚚 Entregas realizadas",
            dados["quantidade"]
        )


    with c2:

        st.metric(
            "👨‍✈️ Motoristas",
            dados["motoristas"]
        )


    with c3:

        st.metric(
            "👥 Ajudantes",
            dados["ajudantes"]
        )


    with c4:

        st.metric(
            "💰 Total",
            f'R$ {dados["valor"]:,.2f}'
        )





def cards_montagens():

    dados = st.session_state.montagens


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "🔨 Montagens",
            dados["quantidade"]
        )


    with c2:

        st.metric(
            "👷 Montadores",
            dados["montadores"]
        )


    with c3:

        st.metric(
            "💰 Total",
            f'R$ {dados["valor"]:,.2f}'
        )