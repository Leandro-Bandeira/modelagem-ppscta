#Codigo responsável por realizar a leitura do resumo dos orientadores
#E leitura do binário gerado pelo cplex para ver quais trablhos foram alocados
#Precisamos do caminho do arquivo json e do binario
import json

path_bin = "../src/binario14.txt"
path_orien = "../Criador-Instancia2.0/resumoOrientadores/resumoOrientadores14.json"
path_out_json = "relacao14.json"

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


def main():
    data_trabalhos = read_orien(path_orien)
    data_bin = read_bin(path_bin)


    list_aloc = list()

    # Criação de uma lista de orientadores unica com area e subarea
    # Na lista de alocação temos uma matriz orientadores x trabalhos
    # Como ele nunca será alocado ao proprio trabalho e a matriz de similaridade
    # Possui -1 como beneficio para os mesmos trabalhos, então podemos pegar pelo indice diretamente
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
    
   
    alocados_proprio_trabalho = 0
    alocados_a_mesma_subarea = 0
    alocados_a_mesma_area = 0
    # Percorre as linhas do arquivo binário e verifica para onde o orientador i foi alocado
    for i, line in enumerate(data_bin):
        line = line.rstrip()
        trabalhos = line.split()
        
        
        for trabalho in trabalhos:
            if orientadores[i]["Area"] == data_trabalhos[int(trabalho)]["Area:"]:
                alocados_a_mesma_area += 1
                
            if orientadores[i]["SubArea"] == data_trabalhos[int(trabalho)]["SubArea:"]:
                alocados_a_mesma_subarea += 1
            
    print(alocados_a_mesma_area)
    print(alocados_a_mesma_subarea)
    #for i, line in enumerate(data_bin):
    #    line = line.rstrip()
    #    data_dict = dict()
    #    trabalhos = line.split()
    #    data_dict['Area Primeiro'] = orientadores[i]['Area']
    #    data_dict['SubArea Primeiro'] = orientadores[i]['SubArea']

        # A partir daqui pegamos de data_orien que indica o total de trabalhos
    #    for j, trabalho in enumerate(trabalhos):
    #        data_dict[f'Area {j}'] = data_orien[int(trabalho)]["Area:"]
    #        data_dict[f"SubArea {j}"] = data_orien[int(trabalho)]["SubArea:"]

    #   list_aloc.append(data_dict)

    # Responsável por criar o json do resumo dos orientadores
    #with open(path_out_json, 'w') as bin_js:
    #    json.dump(list_aloc, bin_js, indent = 4, ensure_ascii=False)
    #bin_js.close()

    

    return 0





















if __name__== '__main__':

    main()
