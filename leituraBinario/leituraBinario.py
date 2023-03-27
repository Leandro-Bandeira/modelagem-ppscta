#Codigo responsável por realizar a leitura do resumo dos orientadores
#E leitura do binário gerado pelo cplex para ver quais trablhos foram alocados
#Precisamos do caminho do arquivo json e do binario
import json

path_bin = "../src/binario14.txt"
path_orien = "../Criador-Instancia2.0/resumoOrientadores/resumoOrientadores14.json"
path_out_json = "relacao14.json"
path_chico = "projetos2014.json"

def read_orien(path_orien):

    with open(path_orien) as file:
        data = json.load(file)
    
    return data

#O arquivo bin está setado para orientadores x trabalhos
def read_bin(path_bin):

    arq = open(path_bin, 'r')
    data = arq.readlines()
    arq.close()
    
    return data


def read_trabalhos_alocados(path_chico):

    with open(path_chico) as file:
        data = json.load(file)
    
    return data

def main():
    data_trabalhos = read_orien(path_orien) # Todos os trabalhos possíveis
    data_bin = read_bin(path_bin) # Arquivo contendo os dados binários
    data_alocados = read_trabalhos_alocados(path_chico) # Todos os 955 trabalhos alocados

    list_aloc = list()

    # Criação de uma lista única de orientadores contendo os dados relevantes
    orientadores = list()
    orientadores_visited = list()
    for project in data_trabalhos:
        if project["Orientador:"] not in orientadores_visited:
            data = dict()
            data['Orientador'] = project["Orientador:"]
            data["Area"] = project["Area:"]
            data["SubArea"] = project["SubArea:"]
            orientadores.append(data)
            orientadores_visited.append(project["Orientador:"])
    
    

    
    alocados_a_mesma_subarea = 0
    alocados_a_mesma_area = 0
    

    # Como a quantia de linhas de data_bin representa o indice do orientador
    # Entao podemos percorrer os seus valores e suas linhas e verificar se o orientador i
    # foi alocado de forma correta aqueles trabalhos 
    for i, line in enumerate(data_bin):
        line = line.rstrip()
        trabalhos = line.split()
        
        for trabalho in trabalhos:
            

    print(alocados_a_mesma_area)
    print(alocados_a_mesma_subarea)
    

    

    return 0





















if __name__== '__main__':

    main()
