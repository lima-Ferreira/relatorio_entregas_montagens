import json
import os
from datetime import datetime


ARQUIVO = "dados/indicadores.json"


def ler_indicadores():

    if not os.path.exists(ARQUIVO):

        return {
            "entregas": 0,
            "montagens": 0,
            "valor_entregas": 0,
            "valor_montagens": 0,
            "ultima_atualizacao": ""
        }


    with open(
        ARQUIVO,
        "r",
        encoding="utf-8"
    ) as arquivo:

        return json.load(arquivo)



def salvar_indicadores(dados):

    dados["ultima_atualizacao"] = (
        datetime.now()
        .strftime("%d/%m/%Y %H:%M")
    )


    os.makedirs(
        "dados",
        exist_ok=True
    )


    with open(
        ARQUIVO,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            dados,
            arquivo,
            indent=4,
            ensure_ascii=False
        )