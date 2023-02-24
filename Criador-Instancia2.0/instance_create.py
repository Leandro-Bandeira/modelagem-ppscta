import json



def open_similarity(path):

    arq = open(path, 'r')
    linhas = arq.readlines()
    arq.close()
    return linhas

def open_orientadores(path, len_projects):

    orientadores_data = list()
    orientadores = list()
    with open(path) as file:
        orientadores_data = json.load(file)
        len_projects.append(len(orientadores_data))
        for data in orientadores_data:
            orientadores.append(data["Orientador:"])


    orientadores = list(set(orientadores))
    return orientadores




def main():
    path_similarity = "../SimilaridadesOrientadores/similarityOrientadores14.txt"
    path_orientadores = "resumoOrientadores/resumoOrientadores14.json"
    path_instance = "instance14.txt"
    similarity_data = open_similarity(path_similarity)
    len_projects = list()

    orientadores_data = open_orientadores(path_orientadores, len_projects)
    
    arq = open(path_instance, 'w')
    
    line = str(len(orientadores_data)) + ' ' + str(len_projects[0]) + '\n'
    arq.write(line)


    for similarity_line in similarity_data:
        arq.write(similarity_line)

    arq.close()
    return 0













if __name__== "__main__":
    main()