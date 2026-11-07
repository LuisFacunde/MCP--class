import os
from dotenv import load_dotenv
from fastmcp import FastMCP
from assistente import AssistenteGPT
from banco import BancoNeon

load_dotenv(".env")

gpt = AssistenteGPT(os.getenv("GPT"))
banco = BancoNeon(os.getenv("NEON"))
mcp = FastMCP("Assistente de Banco de Dados")


@mcp.tool
def listar_tabelas() -> list[str]:
    """Lista todas as tabelas existentes no banco de dados"""
    return banco.listar_tabelas()


@mcp.tool
def descrever_tabela(tabela: str) -> list[dict]:
    """Retorna as colunas e os tipos de dados de uma tabela"""
    return banco.descrever_tabela(tabela)


@mcp.tool
def gerar_sql(pergunta: str) -> str:
    """Transforma uma pergunta em português em um comando SELECT."""
    return gpt.gerar_sql(pergunta, banco.esquema_completo())


@mcp.tool
def executar_select(sql: str) -> list[dict]:
    """Executa um comando SELECT no banco e devolve as linhas."""
    return banco.consultar(sql)


@mcp.tool
def perguntar_ao_banco(pergunta: str) -> dict:
    """Responde uma pergunta em português: o GPT gera o SQL, o banco executa e o GPT explica."""
    sql = gpt.gerar_sql(pergunta, banco.esquema_completo())
    dados = banco.consultar(sql)
    resposta = gpt.explicar_resultado(pergunta, dados)
    return {"sql": sql, "dados": dados, "resposta": resposta}


if __name__ == "__main__":
    mcp.run()  # padrão: transporte stdio
