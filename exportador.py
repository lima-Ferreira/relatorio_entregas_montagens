import pandas as pd
import io


def gerar_excel_abas(abras):
    """
    Recebe um dicionário contendo:
    
    {
        "Nome da Aba": dataframe
    }

    e devolve um arquivo Excel pronto para download.
    """

    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        for nome_aba, dataframe in abras.items():

            dataframe.to_excel(
                writer,
                sheet_name=nome_aba[:31],
                index=False
            )

    buffer.seek(0)

    return buffer



def gerar_excel_montagens(
        df_equipes,
        df_individual,
        df_detalhado
):
    """
    Excel específico das montagens.

    Abas:
    - Produção das equipes
    - Fechamento individual
    - Detalhamento
    """

    abas = {

        "Produção Equipes": df_equipes,

        "Fechamento": df_individual,

        "Detalhamento": df_detalhado

    }

    return gerar_excel_abas(abas)



def gerar_excel_entregas(
        df_motoristas,
        df_ajudantes
):
    """
    Excel específico das entregas.
    """

    abas = {

        "Motoristas": df_motoristas,

        "Ajudantes": df_ajudantes

    }

    return gerar_excel_abas(abas)