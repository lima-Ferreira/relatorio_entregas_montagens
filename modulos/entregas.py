import streamlit as st
import pandas as pd

from utils import ler_excel, limpar_texto, formatar_moeda

from exportador import gerar_excel_entregas


def encontrar_coluna_entregador(df):

    possibilidades = ["MOTORISTA", "ENTREGADOR"]

    for coluna in df.columns:

        nome = coluna.upper().strip()

        for item in possibilidades:

            if item in nome:
                return coluna

    return None


def tela_entregas():

    st.title("🚚 Controle de Entregas")

    st.write("Controle de entregas, motoristas e ajudantes.")

    valor_entrega = st.number_input(
        "Valor total da entrega (R$)",
        min_value=0.0,
        value=3.0,
        step=0.50,
        format="%.2f",
    )

    arquivo = st.file_uploader("Enviar Excel de Entregas", type=["xlsx", "xls", "csv"])

    if not arquivo:
        return

    df = ler_excel(arquivo)

    coluna_entregador = encontrar_coluna_entregador(df)

    coluna_ajudante = None

    for coluna in df.columns:

        if "AJUDANTE" in coluna.upper():

            coluna_ajudante = coluna
            break

    if not coluna_entregador:

        st.error("Não encontrei MOTORISTA ou ENTREGADOR.")

        st.write(df.columns.tolist())

        return

    if not coluna_ajudante:

        df["AJUDANTE"] = ""

        coluna_ajudante = "AJUDANTE"

    if st.button("Processar Entregas", type="primary"):

        entregadores = {}

        ajudantes = {}

        valor_dividido = round(valor_entrega / 2, 2)

        for _, linha in df.iterrows():

            entregador = limpar_texto(linha[coluna_entregador])

            ajudante = limpar_texto(linha[coluna_ajudante])

            if not entregador:

                continue

            if entregador not in entregadores:

                entregadores[entregador] = {"Quantidade": 0, "Valor": 0.0}

            entregadores[entregador]["Quantidade"] += 1

            entregadores[entregador]["Valor"] += valor_dividido

            if ajudante:

                if ajudante not in ajudantes:

                    ajudantes[ajudante] = {"Quantidade": 0, "Valor": 0.0}

                ajudantes[ajudante]["Quantidade"] += 1

                ajudantes[ajudante]["Valor"] += valor_dividido

        df_entregadores = pd.DataFrame(
            [
                {
                    "Entregador": nome,
                    "Quantidade Entregas": dados["Quantidade"],
                    "Total Receber": round(dados["Valor"], 2),
                }
                for nome, dados in entregadores.items()
            ]
        )

        df_ajudantes = pd.DataFrame(
            [
                {
                    "Ajudante": nome,
                    "Quantidade Entregas": dados["Quantidade"],
                    "Total Receber": round(dados["Valor"], 2),
                }
                for nome, dados in ajudantes.items()
            ]
        )

        # ============================
        # SALVAR NA SESSÃO
        # ============================

        st.session_state.entregas = {
            "quantidade": len(df),
            "valor": round(len(df) * valor_entrega, 2),
            "motoristas": len(df_entregadores),
            "ajudantes": len(df_ajudantes),
            "dados": {"entregadores": df_entregadores, "ajudantes": df_ajudantes},
        }

        st.success("Entregas processadas com sucesso!")

        st.divider()

        st.subheader("🚚 Fechamento dos Entregadores")

        visual_entregadores = df_entregadores.copy()

        if not visual_entregadores.empty:

            visual_entregadores["Total Receber"] = visual_entregadores[
                "Total Receber"
            ].apply(formatar_moeda)

        st.dataframe(visual_entregadores, use_container_width=True)

        st.subheader("👥 Fechamento dos Ajudantes")

        visual_ajudantes = df_ajudantes.copy()

        if not visual_ajudantes.empty:

            visual_ajudantes["Total Receber"] = visual_ajudantes["Total Receber"].apply(
                formatar_moeda
            )

        st.dataframe(visual_ajudantes, use_container_width=True)

        arquivo_excel = gerar_excel_entregas(df_entregadores, df_ajudantes)

        st.download_button(
            "📥 Baixar Relatório Excel",
            arquivo_excel,
            "relatorio_entregas.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
