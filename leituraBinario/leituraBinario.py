"""Codigo responsável por ler o arquivo binario gerado pelo txt"""
import json


def read_projetos(path_projetos):
    
    with open(path_projetos) as file:
        data = json.load(file)
    
    return data


def read_orien(path_orien):
    
    with open(path_orien) as file:
        data = json.load(file)
    return data


def read_bin(path_bin):
    
    data = list()
    with open(path_bin) as file:
        data = file.readlines()
    return data

def main():
    path_projetos = "../DadosTrabalhos/projetos2014.json"
    path_orien = "../Criador-Instancia2.0/modeloChico/orientadores14.json"
    path_bin = "../src/binario14.txt"
    
    data_projetos = read_projetos(path_projetos)
    data_orien = read_orien(path_orien)
    data_bin = read_bin(path_bin)

    alocados_area = 0
    alocados_subArea = 0

    for i, line in enumerate(data_bin):
        trabalhos = line.lstrip().rstrip().split()
        for trabalho in trabalhos:
            if data_orien[i]["Area"] == data_projetos[int(trabalho)]["Area:"]:
                alocados_area += 1
            elif data_orien[i]["SubArea"] == data_projetos[int(trabalho)]["SubArea:"]:
                alocados_subArea += 1


    print(alocados_subArea)
    print(alocados_area)


if __name__ == "__main__":
    main()
