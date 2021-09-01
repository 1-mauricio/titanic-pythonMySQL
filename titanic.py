import mysql.connector
from mysql.connector import errorcode

try:
    conexao = mysql.connector.connect(
        host='localhost', 
        user='root',
        database='titanic')

    cursor = conexao.cursor()

    arq_lido = open('Titanic.txt','r')

    continuar = True
    while continuar: 
        print("\n----------------------------------------------------")
        print("------------------------MENU------------------------")
        print("1 - Colocar os nomes de passageiros do titanic no MySQL")
        print("2 - Resetar o banco de dados")
        print("3 - Encontrar alguém por seu id")
        print("----------------------------------------------------")
        print("----------------------------------------------------")

        res = int(input(": "))
        while res>3 or res<0:
            print("A entrada não condiz com uma opção. Tente novamente")
            res = int(input(": "))

        if res == 1:
            with arq_lido:
                for linha in arq_lido:
                    pessoa = linha.split(",")        
                    sobrevivente = pessoa[1]
                    nome = pessoa[3]
                    sexo = pessoa[4]
                    idade = pessoa[5]
                    if nome != "Name":
                        query = ("INSERT INTO pessoas "
                                "(sobrevivente, nome, sexo, idade) "
                                f" VALUES ('{sobrevivente}' , '{nome}', '{sexo}', '{idade}')")
                        
                        cursor.execute(query)
                        conexao.commit()
                        if sobrevivente == "1":
                            survived = ("INSERT INTO sobreviventes "
                                    "(sobrevivente, nome, sexo, idade) "
                                    f" VALUES ('{sobrevivente}' , '{nome}', '{sexo}', '{idade}')")
                            
                            cursor.execute(survived)
                            conexao.commit()
        elif res == 2:
            apagar1 = "DELETE FROM pessoas WHERE id<10000"
            apagar2 = "DELETE FROM sobreviventes WHERE id<10000"
            reset1 = "ALTER TABLE pessoas AUTO_INCREMENT = 1"
            reset2 = "ALTER TABLE sobreviventes AUTO_INCREMENT = 1"
            
            cursor.execute(apagar1)
            cursor.execute(apagar2)
            cursor.execute(reset1)
            cursor.execute(reset2)
            conexao.commit()
        elif res == 3:
            fim = False
            while not fim:
                id_procura = int(input("\nDigite o id: "))
                if id_procura>714:
                    print("Existem 714 pessoas no banco de dados. Digite um id entre 1-714.")
                encontrar = f"SELECT * FROM pessoas WHERE id ={id_procura}"
                cursor.execute(encontrar)
                myresult = cursor.fetchall()
                for (id, sobrevivente, nome, sexo, idade) in myresult:
                    print(f"\nA pessoa correspondente ao id {id} é:")
                    print(f"{nome} de {idade} anos" )
                    if sobrevivente == "1":
                        print("Sobrevivente: Sim")
                    else:
                        print("Sobrevivente: Não")
                    if sexo == "male":
                        print("Sexo: Masculino")
                    else:
                        print("Sexo: Feminino")
                end = input("\nPesquisar mais alguém?(S/N): ")
                while end != "S" and end != "N":
                    end = input("Entrada inválida. Pesquisar mais alguém?(S/N): ")
                if end == "N":
                    fim = True
                
        cont = input("\nEncerrar o programa(S/N): ")
        while cont != "S" and cont != "N":
            cont = input("\nEncerrar o programa(S/N): ")
        if cont == "S":
            continuar = False
        
except FileNotFoundError:
    print("Arquivo/caminho não foi encontrado")

except PermissionError:
    print("Arquivo sem permissão") 

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Algo está errado com seu usename ou password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database não existe")
  else:
    print(err)

else: 
    print("O programa foi finalizado com sucesso.")
    conexao.close()