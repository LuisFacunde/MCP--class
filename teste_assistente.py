import os
from dotenv import load_dotenv
from assistente import AssistenteGPT
import teste_banco as bd

load_dotenv(".env")

gpt = AssistenteGPT(os.getenv("GPT"))

sql = gpt.gerar_sql(
    "Qual é a média do valor para mulheres, homens e total?",
    bd.banco.esquema_completo(),
)
print(sql)

dados = bd.banco.consultar(sql)

print(
    gpt.explicar_resultado(
        "Qual é a média do valor para mulheres, homens e total?", dados
    )
)
