"""Codigo responsável por ler o arquivo binario gerado pelo txt"""
import json
import pandas as pd
from unidecode import unidecode

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



class Projects():
    def __init__(self, id):
        self.id = id
        self.revisors = None

    def get_id(self):
        return self.id
    
    def set_revisors(self, revisors):
        self.revisors = revisors


    def get_revisors(self):
        return self.revisors

def open_similarity(caminho):

    """Abre o arquivo de similaridade """

    with open(caminho) as file:
        data = json.load(file)

    return data
  

def main():
    
    path_projetos = "../DadosTrabalhos/projetos2017.json"
    path_orien = "../Criador-Instancia/orientadores17.json"
    path_bin = "../src/binario17.txt"
    path_aloc = "2014.csv"
    path_similarity = "../DadosTrabalhos/similarityOrientadores17AliDoc2Vec.json"
    ### Todos os dados para ver o resultado do modelo ###
    data_projetos = read_projetos(path_projetos)
    data_orien = read_orien(path_orien)
    data_bin = read_bin(path_bin)
    data_simi = open_similarity(path_similarity)

    alocados_area = 0
    alocados_subArea = 0
    alocados_nenhuma_area = 0
    alocados_mesmo_trabalho = 0
    alocados_maximo_trabalho = 0
    
    avaliadores_por_trabalho = list()
    avaliadores_trabalho = list() # Para cada trabalhos teremos uma lista de avaliadores que não estão relacionados a area e subarea do trabalho
    projects = list()

    # Inicializa em 0 os avaliadores para cada trabalho, o indice de cada trabalho é dado pelo indice do vetor
    for i in range(len(data_projetos)):
        projects.append(Projects(i))
        avaliadores_por_trabalho.append(0)
        avaliadores_trabalho.append(list())
    
    
    
    

    
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
            #print(f'O orientador {indice_orientador} foi alocado ao trabalho {trabalho} cujo não bateu área e subarea')
            avaliadores_trabalho[int(trabalho)].append(indice_orientador)
             
            
        
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

    aloc_df = pd.read_csv(path_aloc, sep=',', encoding='UTF-8')
    output_csv = open("results.csv", "w+")

    first_advisor = aloc_df["Avaliador 1:"].to_list()
    second_advisor = aloc_df["Avaliador 2:"].to_list()


    output_csv.write("Projeto\tAvaliador1\tAvaliador2\tAvaliador1 Novo\tAvaliador2 Novo\n")

    for project in data_projetos:
        id = int(project["id"])
        # Aquele projeto teve pelo menos 1 avaliador que não tem nem área e subárea alocado
        if len(avaliadores_trabalho[id]) >= 1:
            project_name = project["Projeto:"].lower()
            advisor1 = first_advisor[id]
            advisor2 = second_advisor[id]
            new_advisors = avaliadores_trabalho[id]
            name_newAdvisor = list()
            for advisor in new_advisors:
                name_newAdvisor.append(data_orien[advisor]["Nome"])
            
            similarity_advisors = list()
            best_simi = 0
            for advisor in data_orien:

                if advisor1.lower().rstrip().lstrip() == advisor["Nome"].lower().rstrip().lstrip():
                    projects_advisor = advisor["Projetos"]
                    
                    first_project = projects_advisor[0]
                    simi_data = data_simi[first_project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                    best_simi = float(simi_data[id])

                    for project in projects_advisor:
                        simi_data = data_simi[project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                        simi = float(simi_data[id])
                        if simi > best_simi:
                            best_simi = simi
                
                    
                    break
            similarity_advisors.append(best_simi)
            
            best_simi = 0
            for advisor in data_orien:

                if advisor2.lower().rstrip().lstrip() == advisor["Nome"].lower().rstrip().lstrip():
                    projects_advisor = advisor["Projetos"]
                    first_project = projects_advisor[0]
                    simi_data = data_simi[first_project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                    best_simi = float(simi_data[id])

                    for project in projects_advisor:
                        simi_data = data_simi[project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                        simi = float(simi_data[id])
                        if simi > best_simi:
                            best_simi = simi

                    
                    break
            similarity_advisors.append(best_simi)

            best_simi = 0
            for advisor in data_orien:

                if name_newAdvisor[0].lower().rstrip().lstrip() == advisor["Nome"].lower().rstrip().lstrip():
                    projects_advisor = advisor["Projetos"]
                    first_project = projects_advisor[0]
                    simi_data = data_simi[first_project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                    best_simi = float(simi_data[id])

                    for project in projects_advisor:
                        simi_data = data_simi[project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                        simi = float(simi_data[id])
                        if simi > best_simi:
                            best_simi = simi

                    
                    break
            similarity_advisors.append(best_simi)

            best_simi = 0
            if len(avaliadores_trabalho[id]) > 1:
                for advisor in data_orien:

                    if name_newAdvisor[1].lower().rstrip().lstrip() == advisor["Nome"].lower().rstrip().lstrip():
                        projects_advisor = advisor["Projetos"]
                        first_project = projects_advisor[0]
                        simi_data = data_simi[first_project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                        best_simi = float(simi_data[id])

                        for project in projects_advisor:
                            simi_data = data_simi[project]["similaridade"].split(' ') # similaridade do primeiro projeto do orientador com aquele trabalho
                            simi = float(simi_data[id])
                            if simi > best_simi:
                                best_simi = simi

                        
                        break
                similarity_advisors.append(best_simi)

            if len(avaliadores_trabalho[id]) == 1:
                output_csv.write(f'{unidecode(project_name)}\t{advisor1} {similarity_advisors[0]}\t{advisor2} {similarity_advisors[1]}\t{name_newAdvisor[0]} {similarity_advisors[2]}\t\n')
            else:
                output_csv.write(f'{unidecode(project_name)}\t{advisor1} {similarity_advisors[0]}\t{advisor2} {similarity_advisors[1]}\t{name_newAdvisor[0]} {similarity_advisors[2]}\t{name_newAdvisor[1]} {similarity_advisors[3]}\n')

    output_csv.close()


if __name__ == "__main__":
    main()
