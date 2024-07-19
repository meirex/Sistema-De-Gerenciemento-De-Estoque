import sqlite3

class Gestao:
    def __init__(self, banco):
        self.conn = sqlite3.connect(banco)
        self.add_tabela_estoque()

    def add_tabela_estoque(self):
        cursor = self.conn.cursor()
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS estoque (
               id INTEGER PRIMARY KEY,
               produto TEXT,
               quantidade INTEGER
           )
        ''')
        self.conn.commit()

    def add_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO estoque (produto, quantidade) VALUES (?, ?)", (produto, quantidade))
        self.conn.commit()

    def drop_produto(self, produto, quantidade):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto=?", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            estoque_atual = resultado[0]
            if estoque_atual >= quantidade:
                cursor.execute("UPDATE estoque SET quantidade=? WHERE produto=?",
                               (estoque_atual - quantidade, produto))
                self.conn.commit()
            else:
                print(f"Quantidade insuficiente de {produto} em estoque.")
        else:
            return 0

    def consultar_estoque(self, produto):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT quantidade FROM estoque WHERE produto=?", (produto,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return 0

    def listar_produto(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT produto FROM estoque")
        produtos = cursor.fetchall()
        return [produto[0] for produto in produtos]


if __name__ == "__main__":
    sistema = Gestao("estoque.database")

    while True:
        print("GERENCIAMENTO DE ESTOQUE:")
        print("1. Adicionar produto")
        print("2. Remover produto")
        print("3. Consultar estoque")
        print("4. Listar produtos")
        print("5. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            produto = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a quantidade: "))
            sistema.add_produto(produto, quantidade)
            print(f"Produto {produto} adicionado com sucesso!")

        elif opcao == "2":
            produto = input("Digite o nome do produto: ")
            quantidade = int(input("Digite a quantidade a ser removida: "))
            sistema.drop_produto(produto, quantidade)
            print(f"{quantidade} unidades de {produto} removidas com sucesso!")

        elif opcao == "3":
            produto = input("Digite o nome do produto: ")
            estoque = sistema.consultar_estoque(produto)
            print(f"Quantidade de {produto} em estoque: {estoque}")

        elif opcao == "4":
            produtos_em_estoque = sistema.listar_produto()
            print(f"Produtos em estoque: {produtos_em_estoque}")

        elif opcao == "5":
            print("VALEU")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")