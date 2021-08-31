import mysql.connector

try:
    conexao = mysql.connector.connect(
        host='localhost', 
        user='root',
        database='titanic')

    print("Conexão bem sucedida")

    cursor = conexao.cursor()

    arq_lido = open('Titanic.txt','r')
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


except FileNotFoundError:
    print("Arquivo/caminho não foi encontrado")

except PermissionError:
    print("Arquivo sem permissão") 

except:
    print("Erro inesperado")

else: 
    print("O programa foi finalizado com sucesso.")