import json


def open_similarity(path_similarity):

    data = dict()

    with open(path_similarity) as file:
        data = json.load(file)
    file.close()

    return data


def open_projects(path_projects):
    data = dict()
    with open(path_projects) as file:
        data = json.load(file)
    file.close()

    return data


def main():
    path_similarity = "../SimilaridadesOrientadores/similarityOrientadores14Alin.json"
    path_projetcs = "projetos2014.json"

    # Abrindo arquivos de json e armazenandos seus dicionários
    projetcs_data = open_projects(path_projetcs)
    similarity_dic = open_similarity(path_similarity) 













if __name__ == "__main__":
    main()
