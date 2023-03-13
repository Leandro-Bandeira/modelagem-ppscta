#Codigo responsável por realizar a leitura do resumo dos orientadores
#E leitura do binário gerado pelo cplex para ver quais trablhos foram alocados
#Precisamos do caminho do arquivo json e do binario
import json

path_bin = input("Digite o caminho do arquivo binario: ")
path_orien = input("Digite o caminho do arquivo dos orientadores: ")
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
    data_orien = read_orien(path_orien)
    data_bin = read_bin(path_bin)

    list_aloc = list()
    
    for i, line in enumerate(data_bin):
        line = line.rstrip()
        data_dict = dict()
        trabalhos = line.split()
        data_dict['Area Primeiro'] = data_orien[i]['Area:']
        data_dict['SubArea Primeiro'] = data_orien[i]['SubArea:']

        for j, trabalho in enumerate(trabalhos):
            data_dict[f'Area {j}'] = data_orien[int(trabalho)]["Area:"]
            data_dict[f"SubArea {j}"] = data_orien[int(trabalho)]["SubArea:"]

        list_aloc.append(data_dict)

    # Responsável por criar o json do resumo dos orientadores
    with open(path_out_json, 'w') as bin_js:
        json.dump(list_aloc, bin_js, indent = 4, ensure_ascii=False)
    bin_js.close()

    

    return 0





















if __name__== '__main__':

    main()
