import os
from dotenv import load_dotenv
from banco import BancoNeon

load_dotenv(".env")

banco = BancoNeon(os.getenv("NEON"))
# print(banco.listar_tabelas())
