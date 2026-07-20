import streamlit as st
import pandas as pd

from utils import (
    ler_excel,
    limpar_texto,
    encontrar_coluna,
    formatar_moeda
)

from exportador import gerar_excel_montagens



def tela_montagens():

    st.markdown(
        "Faça o upload da planilha para calcular produção e gratificações."
    )


    valor_montagem = st.number_input(
        "Valor da montagem (R$)",
        min_value=0.0,
        value=3.0,
        step=0.50
    )


    arquivo = st.file_uploader(
        "Enviar Excel de Montagens",
        type=["xlsx","xls","csv"]
    )


    if arquivo:


        df = ler_excel(arquivo)


        coluna_m1 = encontrar_coluna(
            df,
            "MONTADOR 1"
        )


        coluna_m2 = encontrar_coluna(
            df,
            "MONTADOR 2"
        )



        if not coluna_m1:

            st.error(
                "Não encontrei MONTADOR 1"
            )

            return



        if not coluna_m2:

            df["MONTADOR 2"] = ""

            coluna_m2 = "MONTADOR 2"



        if st.button(
            "Processar Montagens",
            type="primary"
        ):


            equipes = {}

            individuais = {}

            detalhes = {}



            for _, linha in df.iterrows():


                m1 = limpar_texto(
                    linha[coluna_m1]
                )


                m2 = limpar_texto(
                    linha[coluna_m2]
                )


                if not m1:
                    continue



                if not m2:


                    equipe = f"{m1} (SOZINHO)"

                    valor = valor_montagem


                    individuais.setdefault(
                        m1,
                        {
                            "Solo":0,
                            "Dupla":0,
                            "Valor":0
                        }
                    )


                    individuais[m1]["Solo"] += 1

                    individuais[m1]["Valor"] += valor



                else:


                    nomes = sorted(
                        [
                            m1,
                            m2
                        ]
                    )


                    equipe = (
                        nomes[0]
                        +
                        " + "
                        +
                        nomes[1]
                    )


                    valor = valor_montagem / 2



                    for nome in nomes:


                        individuais.setdefault(
                            nome,
                            {
                                "Solo":0,
                                "Dupla":0,
                                "Valor":0
                            }
                        )


                        individuais[nome]["Dupla"] += 1

                        individuais[nome]["Valor"] += valor



                equipes.setdefault(

                    equipe,

                    {
                        "Equipe":equipe,
                        "Quantidade":0,
                        "Valor Total":0

                    }

                )


                equipes[equipe]["Quantidade"] += 1

                equipes[equipe]["Valor Total"] += valor_montagem




            df_equipes = pd.DataFrame(
                equipes.values()
            )



            df_individual = pd.DataFrame(

                [

                    {

                        "Montador":nome,

                        "Montagens Sozinho":dados["Solo"],

                        "Montagens Dupla":dados["Dupla"],

                        "Total Montagens":
                            dados["Solo"]
                            +
                            dados["Dupla"],

                        "Total Receber":
                            dados["Valor"]

                    }


                    for nome,dados in individuais.items()

                ]

            )



            # ==========================
            # SALVAR NA SESSÃO
            # ==========================


            st.session_state.montagens = {


                "quantidade":
                    len(df),


                "valor":
                    df_individual["Total Receber"].sum(),


                "montadores":
                    len(df_individual),



                "dados":{

                    "equipes":df_equipes,

                    "individual":df_individual

                }

            }



            st.success(
                "Montagens processadas!"
            )



            st.subheader(
                "📋 Produção por Equipe"
            )


            tabela = df_equipes.copy()


            tabela["Valor Total"] = (
                tabela["Valor Total"]
                .apply(formatar_moeda)
            )


            st.dataframe(
                tabela,
                use_container_width=True
            )



            st.subheader(
                "💰 Fechamento Individual"
            )


            tabela2=df_individual.copy()


            tabela2["Total Receber"] = (
                tabela2["Total Receber"]
                .apply(formatar_moeda)
            )


            st.dataframe(
                tabela2,
                use_container_width=True
            )



            arquivo_excel = gerar_excel_montagens(

                df_equipes,

                df_individual,

                df_individual

            )


            st.download_button(

                "📥 Baixar Relatório Excel",

                arquivo_excel,

                "relatorio_montagens.xlsx"

            )