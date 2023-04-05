#Codigo responsável por realizar a leitura do resumo dos orientadores
#E leitura do binário gerado pelo cplex para ver quais trablhos foram alocados
#Precisamos do caminho do arquivo json e do binario
import json

path_bin = "../src/binario14Alin.txt"
path_out_json = "relacao14.json"
path_projetos = "projetos2014.json"


#O arquivo bin está setado para orientadores x trabalhos
def read_bin(path_bin):

    arq = open(path_bin, 'r')
    data = arq.readlines()
    arq.close()
    
    return data


def read_projetos(path_projetos):

    with open(path_projetos) as file:
        data = json.load(file)
    
    return data

def main():
    data_bin = read_bin(path_bin) # Arquivo contendo os dados binários
    data_projetos = read_projetos(path_projetos) # Todos os 955 trabalhos alocados

     
    alocados_a_mesma_subarea = 0
    alocados_a_mesma_area = 0
    

    # Como a quantia de linhas de data_bin representa o indice do orientador
    # Entao podemos percorrer os seus valores e suas linhas e verificar se o orientador i
    # foi alocado de forma correta aqueles trabalhos 
    for i, line in enumerate(data_bin):
        line = line.rstrip()
        trabalhos = line.split()
        for trabalho in trabalhos:
            print(f'Professor area: {data_projetos[i]["Area:"]}')
            print(f'Projeto area: {data_projetos[int(trabalho)]["Area"]}')
            if data_projetos[i]["Area:"] == data_projetos[int(trabalho)]['Area:']:
                alocados_a_mesma_area += 1
            if data_projetos[i]["SubArea:"] == data_projetos[int(trabalho)]["SubArea:"]:
                alocados_a_mesma_subarea += 1
            

    print(alocados_a_mesma_area)
    print(alocados_a_mesma_subarea)
    

    

    return 0





















if __name__== '__main__':

    main()
