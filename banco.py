import psycopg2


class BancoNeon:

    def __init__(self, url_conexao):
        self.url_conexao = url_conexao

    def _conectar(self):
        """Abre uma nova conexão como o banco de dados"""

        conexao = psycopg2.connect(self.url_conexao)
        # Ativa o modo somento leitura ao banco: recusa INSERT, DELETE, DROP...
        conexao.set_session(readonly=True)

        return conexao

    def consultar(self, sql) -> list[dict]:
        """Executa um SELECT e devolve uma lista de dicionários"""

        with self._conectar() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(sql)
                colunas = [coluna[0] for coluna in (cursor.description or [])]
                linhas = cursor.fetchall()

                return [dict(zip(colunas, linha)) for linha in linhas]

    def listar_tabelas(self):
        """Retornar o nome de todas as tabelas do schema public do banco de dados"""

        sql = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
              """

        return [linha["table_name"] for linha in self.consultar(sql)]

    def descrever_tabela(self, tabela):
        """Retorna as colunas e os tipos de dados de uma tabela."""

        with self._conectar() as conexao:
            with conexao.cursor() as cursor:
                # O %s evita SQL Injection: o psycopg2 trata o valor com segurança
                cursor.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position
                    """,
                    (tabela,),
                )
                return [{"coluna": c, "tipo": t} for c, t in cursor.fetchall()]

    def esquema_completo(self):
        """Montar um texto com todas as tabelas e colunas (usado pelo GPT)"""

        texto = ""

        for tabela in self.listar_tabelas():
            colunas = self.descrever_tabela(tabela)
            lista = ", ".join(f"{c['coluna']} ({c['tipo']})" for c in colunas)
            texto += f"- {tabela}: {lista}\n"

        return texto
