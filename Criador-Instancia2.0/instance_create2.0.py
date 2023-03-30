import json


def open_similarity(path_similarity):

    data = dict()

    with open(path_similarity) as file:
        data = json.load(file)
    return data



def main():
    path_similarity = "../SimilaridadesOrientadores/similarityOrientadores14Alin.json"


    similarity_dic = open_similarity(path_similarity) 












if __name__ == "__main__":
    main()
