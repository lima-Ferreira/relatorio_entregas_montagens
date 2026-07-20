import pandas as pd
import io


def limpar_texto(valor):
    """
    Padroniza nomes de pessoas.
    """
    if pd.isna(valor):
        return ""

    valor = str(valor).strip().upper()

    valores_invalidos = [
        "",
        "NAN",
        "NONE",
        "NULL",
        "0",
        "0.0",
        "-"
    ]

    if valor in valores_invalidos:
        return ""

    return valor


def limpar_colunas(df):
    """
    Padroniza nomes das colunas do Excel.
    """
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


def ler_excel(uploaded_file):
    """
    Faz leitura inteligente do arquivo enviado.
    Aceita xlsx, xls, csv.
    """

    conteudo = uploaded_file.read()

    extensao = uploaded_file.name.lower()


    if extensao.endswith(".csv"):
        df = pd.read_csv(
            io.BytesIO(conteudo),
            sep=None,
            engine="python"
        )

    else:
        df = pd.read_excel(
            io.BytesIO(conteudo)
        )


    return limpar_colunas(df)



def encontrar_coluna(df, palavra):
    """
    Procura uma coluna pelo nome aproximado.

    Ex:
    encontrar_coluna(df,'MOTORISTA')

    encontra:
    MOTORISTA ENTREGA
    MOTORISTA
    NOME MOTORISTA
    """

    palavra = palavra.upper()

    for coluna in df.columns:

        if palavra in coluna:
            return coluna

    return None



def criar_dataframe_excel(dados):
    """
    Cria arquivo Excel na memória.
    Usado nos downloads.
    """

    buffer = io.BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        for nome_aba, tabela in dados.items():

            tabela.to_excel(
                writer,
                sheet_name=nome_aba,
                index=False
            )


    buffer.seek(0)

    return buffer



def formatar_moeda(valor):
    """
    Formatação padrão brasileira.
    """

    return f"R$ {valor:,.2f}".replace(
        ",",
        "X"
    ).replace(
        ".",
        ","
    ).replace(
        "X",
        "."
    )