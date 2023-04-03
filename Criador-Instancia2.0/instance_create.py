import json

# retorna os dados de similarity em formato de uma matriz quadrada


def open_similarity(path):

    similarity_data = list()

    with open(path) as file:
        similarity_data = json.load(file)
    file.close()
    return similarity_data

# retorna uma lista contendo todos os nomes dos orientadore


def open_orientadores(path):

    projetos_data = list()
    with open(path) as file:
        projetos_data = json.load(file)
        
    file.close()
    return projetos_data



def main():
    path_similarity = "../DadosTrabalhos/similarityOrientadores14Alin.json"
    path_orientadores = "../DadosTrabalhos/projetos2014.json"
    path_instance = "instance14Alin.txt"
    
    similarity_data = open_similarity(path_similarity) # Contém os dados de similaridade
    
    projetos_data = open_orientadores(path_orientadores)
    
    orientadores_data = list() # Contém todos os orientadores exclusivamente

    for projeto in projetos_data:
        if projeto["Orientador:"] not in orientadores_data:
            orientadores_data.append(projeto["Orientador:"])
    

    # Abre o arquivo para armazenar a quantia de orientadores x projetos
    arq = open(path_instance, 'w')

    line = str(len(orientadores_data)) + ' ' + str(len(projetos_data)) + '\n'
    arq.write(line)

    # Criação da instancia para inviablizar pesos para trabalhos do mesmo orientador, caso forem o mesmo, temos -1 como peso
    # Além disso, precisamos criar uma matriz orientadores X Trabalhos, contendo suas similaridades, vamos analisar qual a melhor matriz similaridade de determinado orientador
    # E usá-la como o peso para o algoritmo, muito importante perceber que os indices dos dois ARQUIVOS estão equiparados, ou seja a similaridade do projeto 0 equivale ao projeto 0.

    orientadores_visitados = list()
    i = 0
    
    
    
    # A ideia agora é achar a partir de similarity_data o trabalho que possui maiores similaridades
    # Achado o trabalho do orientador com maiores similaridades, vamos utilizar um padrão dependendo da similaridade
    # e indicar que aquelas similaridades são daquele indice que representa o trabalho dele
    while (i < len(projetos_data)):
        
        if projetos_data[i]['Orientador:'] not in orientadores_visitados:
            orientadores_visitados.append(projetos_data[i]['Orientador:'])
            media = 0
            # Se tivermos situação em que ele só tiver um projeto, então ele não entra no segundo for, como os indices estão iguais, da similaridade e do projeto, a similaridade de indice 0 representa as similaridades do mesmo projeto 0
            indice_maior_media = i 
            maior_media = -1

            #Acha a melhor linha de similaridade do orientador anterior
            for similarity in similarity_data:
                indice = similarity["indice"]
                data_similarity = similarity["similaridade"].rstrip().lstrip().split()
                
                # Se encontrarmos o mesmo orientador, daquele fixdo em i na minha similaridade
                if projetos_data[indice]["Orientador:"] == projetos_data[i]["Orientador:"]:
                    
                    for value in data_similarity:
                        media += float(value)
                    media /= len(data_similarity)

                    if media > maior_media:
                        maior_media = media
                        indice_maior_media = indice
            

            # Pegamos entãoo a similaridade de maior indice daquele orientador
            avg_similarity = similarity_data[indice_maior_media]["similaridade"].rstrip().lstrip().split()
            for j, similarity in enumerate(avg_similarity):
                # Se o orientador da linha for o mesmo da coluna, então -1 para indicar que o trabalho é inviável
                # Cso ele não for inviável, vamos normalizar as similaridades
                similarity = 0
                if projetos_data[indice_maior_media]["Orientador:"] == projetos_data[j]["Orientador:"]:
                    similarity = "-1"
                else:
                    if float(similarity) > 0.3:
                        similarity = "100"
                    elif float(similarity) >= 0.1 and float(similarity) <= 0.3:
                        similarity = "10"
                    else:
                        similarity = "1"
                
                if j == len(avg_similarity) - 1:

                    line = similarity + '\n'
                else:
                    line = similarity + ' '
                arq.write(line)
    
        i += 1
        
        
              

    
    arq.close()         

        


    
    return 0













if __name__== "__main__":
    main()