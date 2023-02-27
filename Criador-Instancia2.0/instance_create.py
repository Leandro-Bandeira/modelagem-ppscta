import json

# retorna os dados de similarity em formato de uma matriz quadrada
def open_similarity(path):

    arq = open(path, 'r')
    lines = arq.readlines()
    arq.close()
    
    similarity_data = list()
    for line in lines:
        line = line.rstrip()
        similarity_data.append(line.split())


    return similarity_data

#retorna uma lista contendo todos os nomes dos orientadore
def open_orientadores(path, len_projects, orientadores_list):

    orientadores_data = list()
    orientadores = list()
    with open(path) as file:
        orientadores_data = json.load(file)
        orientadores_list.append(orientadores_data)
        len_projects.append(len(orientadores_data))
        for data in orientadores_data:
            orientadores.append(data["Orientador:"])


    orientadores = list(set(orientadores))
    file.close()
    return orientadores




def main():
    path_similarity = "../SimilaridadesOrientadores/similarityOrientadores14.txt"
    path_orientadores = "resumoOrientadores/resumoOrientadores14.json"
    path_instance = "instance14.txt"
    orientadores_list = list() # Contém todos os dados dos orientadores
    similarity_data = open_similarity(path_similarity)
    len_projects = list()

    orientadores_data = open_orientadores(path_orientadores, len_projects, orientadores_list)
    orientadores_dic = orientadores_list[0] # Contém o dicionario dos orientadores
       
    arq = open(path_instance, 'w')
    
    line = str(len(orientadores_data)) + ' ' + str(len_projects[0]) + '\n'
    arq.write(line)


    for i in range(len(similarity_data)):
        
        for j in range(len(similarity_data[i])):
            #Se o nome do orientador for o mesmo 
            if orientadores_dic[i]["Orientador:"] == orientadores_dic[j]["Orientador:"]:
                similarity_data[i][j] = "-1"
            
            if j == len(similarity_data[i]) - 1:
                line = str(similarity_data[i][j]) + '\n'
            else:
                line = str(similarity_data[i][j]) + ' '
            arq.write(line)

    arq.close()
    return 0













if __name__== "__main__":
    main()