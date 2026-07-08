import sqlite3
from datetime import date, datetime

DB_NAME = "pessoas.db"

#python -m venv .venv - Lembrar


def conectar():
	return sqlite3.connect(DB_NAME)


def criar_tabela():
	with conectar() as conexao:
		conexao.execute(
			"""
			CREATE TABLE IF NOT EXISTS pessoas (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				nome TEXT NOT NULL,
				data_nascimento TEXT NOT NULL,
				status_vida TEXT NOT NULL CHECK (status_vida IN ('viva', 'falecida')),
				data_morte TEXT
			)
			"""
		)


def calcular_idade(data_nascimento_texto):
	nascimento = datetime.strptime(data_nascimento_texto, "%Y-%m-%d").date()
	hoje = date.today()
	idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
	return idade


def ler_data(mensagem):
	while True:
		texto = input(mensagem).strip()
		try:
			datetime.strptime(texto, "%Y-%m-%d")
			return texto
		except ValueError:
			print("Data inválida. Use o formato YYYY-MM-DD.")


def adicionar_pessoa():
	nome = input("Nome: ").strip()
	if not nome:
		print("O nome não pode ficar vazio.")
		return

	data_nascimento = ler_data("Data de nascimento (YYYY-MM-DD): ")

	with conectar() as conexao:
		conexao.execute(
			"""
			INSERT INTO pessoas (nome, data_nascimento, status_vida, data_morte)
			VALUES (?, ?, 'viva', NULL)
			""",
			(nome, data_nascimento),
		)

	print("Pessoa adicionada com sucesso.")


def remover_pessoa():
	try:
		pessoa_id = int(input("ID da pessoa para remover: "))
	except ValueError:
		print("ID inválido.")
		return

	with conectar() as conexao:
		cursor = conexao.execute("DELETE FROM pessoas WHERE id = ?", (pessoa_id,))

	if cursor.rowcount == 0:
		print("Nenhuma pessoa encontrada com esse ID.")
	else:
		print("Pessoa removida com sucesso.")


def listar_pessoas():
	with conectar() as conexao:
		cursor = conexao.execute(
			"""
			SELECT id, nome, data_nascimento, status_vida, data_morte
			FROM pessoas
			ORDER BY id
			"""
		)
		pessoas = cursor.fetchall()

	if not pessoas:
		print("Nenhuma pessoa cadastrada.")
		return

	print("\nPessoas cadastradas:")
	for pessoa in pessoas:
		idade = calcular_idade(pessoa[2])
		data_morte = pessoa[4] if pessoa[4] else "-"
		print(
			f"ID: {pessoa[0]} | Nome: {pessoa[1]} | Nascimento: {pessoa[2]} | "
			f"Idade: {idade} | Status: {pessoa[3]} | Morte: {data_morte}"
		)


def marcar_falecimento():
	try:
		pessoa_id = int(input("ID da pessoa falecida: "))
	except ValueError:
		print("ID inválido.")
		return

	data_morte = ler_data("Data da morte (YYYY-MM-DD): ")

	with conectar() as conexao:
		cursor = conexao.execute(
			"""
			UPDATE pessoas
			SET status_vida = 'falecida', data_morte = ?
			WHERE id = ?
			""",
			(data_morte, pessoa_id),
		)

	if cursor.rowcount == 0:
		print("Nenhuma pessoa encontrada com esse ID.")
	else:
		print("Pessoa marcada como falecida.")


def menu():
	criar_tabela()

	while True:
		print("\n menu")
		print("1 - adicionar pessoa")
		print("2 - remover pessoa")
		print("3 - listar pessoas")
		print("4 - marcar falecimento")
		print("0 - sair")

		opcao = input("Escolha uma opção: ").strip()

		if opcao == "1":
			adicionar_pessoa()
		elif opcao == "2":
			remover_pessoa()
		elif opcao == "3":
			listar_pessoas()
		elif opcao == "4":
			marcar_falecimento()
		elif opcao == "0":
			print("Saindo...")
			break
		else:
			print("Opção inválida.")


if __name__ == "__main__":
	menu()