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
    path_orien = "../Criador-Instancia/orientadores14.json"
    path_bin = "../src/binario14.txt"
     
    ### Todos os dados para ver o resultado do modelo ###
    data_projetos = read_projetos(path_projetos)
    data_orien = read_orien(path_orien)
    data_bin = read_bin(path_bin)

    alocados_area = 0
    alocados_subArea = 0
    alocados_nenhuma_area = 0
    alocados_mesmo_trabalho = 0
    alocados_maximo_trabalho = 0
    
    avaliadores_por_trabalho = list()
    
    # Inicializa em 0 os avaliadores para cada trabalho, o indice de cada trabalho é dado pelo indice do vetor
    for i in range(len(data_projetos)):
        avaliadores_por_trabalho.append(0)
    
    
    
    

    
    for i, line in enumerate(data_bin):
        line = line.lstrip().rstrip().split()
        
        indice_orientador = int(line.pop(0))
        trabalhos = line
        quantia_alocados = 0
        
        alocado_conhecido = False
        trabalhos_avaliados_por_orientador = list()

        for trabalho in trabalhos:
            quantia_alocados +=1 
            avaliadores_por_trabalho[data_projetos[(int(trabalho))]["id"]] += 1

            """Dados dos trabalhos"""
            area_trabalho = data_projetos[int(trabalho)]["Area:"]
            subArea_trabalho = data_projetos[int(trabalho)]["SubArea:"]
            orientador_trabalho = data_projetos[int(trabalho)]["Orientador:"]
            
            """Dados do orientador"""
            nome_orientador = data_orien[indice_orientador]["Nome"]
            area_orientador = data_orien[indice_orientador]["Area"]
            subArea_orientador = data_orien[indice_orientador]["SubArea"]


            texto_trabalho = f'{trabalho}, {orientador_trabalho}, {area_trabalho}, {subArea_trabalho}'
            trabalhos_avaliados_por_orientador.append(texto_trabalho) # armazena o trabalho avaliado por aquele orientador
            
            if nome_orientador == orientador_trabalho:
                alocados_mesmo_trabalho += 1
                continue

            if subArea_orientador == subArea_trabalho:
                alocados_subArea += 1
                continue

            if area_orientador == area_trabalho:
                alocados_area += 1
                continue    
            
            alocados_nenhuma_area += 1
            print(f'O orientador {indice_orientador} foi alocado ao trabalho {trabalho} cujo não bateu área e subarea')
            a = input()   
            
        
        data_orien[indice_orientador]["Trabalhos Avaliados"] = trabalhos_avaliados_por_orientador    

        if quantia_alocados > 4:
            alocados_maximo_trabalho


    trabalho_alocados_mais2 = 0
    for i in range(len(data_projetos)):
        if avaliadores_por_trabalho[i] > 2:
            trabalho_alocados_mais2 += 1
        
        
            


    print(f'Alocados a sub_area: {alocados_subArea}')
    print(f'Alocados a area: {alocados_area}')
    print(f'Alocados a nenhuma area desconhecida: {alocados_nenhuma_area}')
    print(f'Alocados ao mesmo trabalho: {alocados_mesmo_trabalho}')
    print(f'alocados a mais de 4 trabalhos: {alocados_maximo_trabalho}')
    print(f'Trabalhos alocados para mais de 2 avaliadores: {trabalho_alocados_mais2}')

    path_trabalhos_avaliados = "orientadores14Projetos.json"

    with open(path_trabalhos_avaliados, 'w') as file:
        json.dump(data_orien, file, indent=4, ensure_ascii=False)




if __name__ == "__main__":
    main()
