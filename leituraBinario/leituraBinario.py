"""Codigo responsável por ler o arquivo binario gerado pelo txt"""
import json


def read_projetos(path_projetos):
    """Função responsável por ler todos os projetos""" 
    with open(path_projetos) as file:
        data = json.load(file)
    
    return data


def read_orien(path_orien):
    """Funcao responsável por ler o json dos orientadores"""
    with open(path_orien) as file:
        data = json.load(file)
    return data


def read_bin(path_bin):
    """Funcao responsável por ler o binario do modelo"""
    data = list()
    with open(path_bin) as file:
        data = file.readlines()
    return data


def main():
    path_projetos = "../DadosTrabalhos/projetos2014.json"
    path_orien = "../Criador-Instancia2.0/modeloChico/orientadores14.json"
    path_bin = "../src/binario14.txt"
    
    ### Todos os dados para ver o resultado do modelo ###
    data_projetos = read_projetos(path_projetos)
    data_orien = read_orien(path_orien)
    data_bin = read_bin(path_bin)

    alocados_area = 0
    alocados_subArea = 0
    alocados_nenhuma_area = 0
    alocados_mesmo_trabalho = 0

    for i, line in enumerate(data_bin):
        trabalhos = line.lstrip().rstrip().split()
        alocado_conhecido = False
        for trabalho in trabalhos:
            
            if data_orien[i]["Nome"] == data_projetos[(int(trabalho))]["Orientador:"]:
                alocados_mesmo_trabalho += 1
                print(f'Orientador alocado ao mesmo trabalho: {data_orien[i]["Nome"]}, indice do trabalho que foi alocado {int(trabalho)}')
                #a = input()
            if data_orien[i]["Area"] == data_projetos[int(trabalho)]["Area:"]:
                alocados_area += 1
                alocado_conhecido = True
                
            if data_orien[i]["SubArea"] == data_projetos[int(trabalho)]["SubArea:"]:
                alocados_subArea += 1
                alocado_conhecido = True
                
        if not alocado_conhecido:
            alocados_nenhuma_area += 1

            


    print(f'Alocados a sub_area: {alocados_subArea}')
    print(f'Alocados a area: {alocados_area}')
    print(f'Alocados a nenhuma area conhecida: {alocados_nenhuma_area}')
    print(f'Alocados ao mesmo trabalho: {alocados_mesmo_trabalho}')

if __name__ == "__main__":
    main()
