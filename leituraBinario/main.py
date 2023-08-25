"""Codigo responsável por criar as tabelas tanto da alocação de Chico como aquela de Leandro
Baseada em trabalho, Quantia de orientadores na area do trabalho, Quantia de orientadores na subArea, Em nenhuma, similaridade 1, 2, media da similaridade"""
import sys
import json
import pandas as pd
from unidecode import unidecode

class Advisor:
    
    def __init__(self, id, name, area, subarea, projects):
        self.id = id
        self.name = name
        self.area = area
        self.subarea = subarea
        self.projects = projects

    def get_id(self):
        return self.id
    
    def get_projects(self):
        return self.projects
    

    def get_name(self):
        return self.name

    def get_area(self):
        return self.area
    
    def get_subarea(self):
        return self.subarea
    



class Project:
    
    def __init__(self, id, name, advisor, area, subarea):
        self.advisor = advisor
        self.revisors = None
        self.id = id
        self.name = name
        self.area = area
        self.subarea = subarea
        self.similarity = None # Similaridade dos 4 avaliadores

    def get_advisor(self):
        return self.advisor
    
    def get_revisors(self):
        return self.revisors
    
    def set_similarity(self, similarity):
        self.similarity = similarity


    def get_similarity(self):
        return self.similarity
    

    def get_id(self):
        return self.id

    # Adiciona os avaliadores, os 2 primeiros são referentes ao de chico e os 2 ultimos referentes ao similaridade
    def append_revisor(self, revisor):
        self.revisors.append(revisor)

    def get_name(self):
        return self.name

    def get_area(self):
        return self.area
    
    def get_subarea(self):
        return self.subarea




"""Função responsável por ler todos os projetos e iniciar as instancias de projetos"""
def extract_projects(path):
     
    with open(path) as file:
        data = json.load(file)

    data_project = list()
    for i, project in enumerate(data):
        name = unidecode(project["Projeto:"]).lower().lstrip().rstrip()
        advisor = unidecode(project["Orientador:"].lower().lstrip().rstrip())
        area = unidecode(project["Area:"].lower().lstrip().rstrip())
        sub_area = unidecode(project["SubArea:"].lower().lstrip().rstrip())

        data_project.append(Project(i, name, advisor, area, sub_area))

    
    return data_project


"""Função responsável por ler todos os orientadores e iniciar as instancias de orientadores"""
def extract_advisors(path):

    with open(path) as file:
        data = json.load(file)

    data_revisors = list()

    for i, revisor in enumerate(data):
        name = unidecode(revisor["Nome"].lower().rstrip().lstrip())
        area = unidecode(revisor["Area"].lower().rstrip().lstrip())
        sub_area = unidecode(revisor["SubArea"].lower().rstrip().lstrip())
        projects = revisor["Projetos"]
        data_revisors.append(Advisor(i, name, area, sub_area, projects))
    
    return data_revisors


def read_bin(path_bin):
    """Funcao responsável por ler o binario do modelo"""
    data = list()
    with open(path_bin) as file:
        data = file.readlines()
    return data


def extract_simi(path):

    with open(path) as file:
        data = json.load(file)
    return data


def add_revisors_aloc_to_projects(path_aloc, path_simi, data_projects, data_advisors):

    aloc_df = pd.read_csv(path_aloc, sep=',', encoding='UTF-8')
    projects = aloc_df['Projeto:'].to_list()
    first_revisor = aloc_df['Avaliador 1'].to_list()
    second_revisor = aloc_df['Avaliador 2'].to_list()

    # Percorre os projetos da alocação e verifica qual sua posição em data_projects pelo nome
    # Quando achado adiciona-se os revisores, procurando-os em data_advisors
    for i, project_aloc in enumerate(projects):
        for project in data_projects:
            project_aloc_name = unidecode(project_aloc).lower().rstrip().lstrip()
            if project_aloc_name == project.get_name():
                revisor_first = first_revisor[i].lower().rstrip().lstrip()
                revisor_second = second_revisor[i].lower().rstrip().lstrip()
                for advisor in data_advisors:
                    if revisor_first == advisor.get_name():
                        project.append_revisor(advisor)
                    if revisor_second == advisor.get_name():
                        project.append_revisor(advisor)


    
    data_simi = read_bin(path_simi)

    for line in data_simi:
        line = line.lstrip().rstrip().split()
        
        # O arquivo binario está organizado da forma: idProjeto IdRevisor1 IdRevisor2
        id_project  = int(line.pop(0))
        advisor_one = int(line.pop(0))
        advisor_second = int(line.pop(0))

        data_projects[id_project].append_revisor(data_advisors[advisor_one])
        data_projects[id_project].append_revisor(data_advisors[advisor_second])



def add_similarity_to_projects(data_projects, data_advisors, data_similarity):

    for project in data_projects:
        id_project = project.get_id()
        revisors = project.get_revisors()
        similarities = data_similarity[id_project]["similaridade"].split()
        # Como cada adivsor orienta um conjunto de projetos, devemos pegar a maior similaridade referente aos trabalhos que ele avalia
        # Em relação a esse projeto da iteração
        similarities_project = list()
        
        for revisor in revisors:            
            projects_revisor = revisor.get_projects()
            best_similarity = float(similarities[projects_revisor[0]]) # Considera inicialmente a maior similaridade do primeiro projetado orientado por ele
        
            for id_project_revisor in projects_revisor:
                similarity  = float(similarities[id_project_revisor])

                if similarity > best_similarity:
                    best_similarity = similarity        
            
            similarities_project.append(best_similarity)
        
        project.set_similarity(similarities_project)        


#Isso deve funcionar, talvez
def write_csv(path, data_projects):
    output_csv = open(path, "w+")
    output_csv.write(f'Trabalho, Avaliador 1, Avaliador 2, Avaliador 3, Avaliador 4, Similaridade 1, Similaridade 2\n')
    
    for i, project in enumerate(data_projects):
        project_revisors = project.get_revisors()
        project_similarities = project.get_similarity()
        
        line_output = f'{i},'
        
        for revisor in project_revisors:
            line_output += f'{revisor.get_name(),}'
        
        for i, similarity in enumerate(project_similarities):
            
            line_output += f'{similarity}\n' if i == len(project_similarities) - 1 else f'{similarity},'
    
        
        
        output_csv.write(line_output)            
            
        
    
def main():
    if len(sys.argv) < 7:
        print("Insira as entradas corretamente: python3 main.py projetos.json orientadores.json alocacaoChicho.csv alocacaoSimi.csv similaridade.json saida.csv ano")

    path_projects = sys.argv[1]
    path_advisors = sys.argv[2]
    path_aloc = sys.argv[3]
    path_aloc_simi = sys.argv[4]
    path_simi = sys.argv[5]
    path_out = sys.argv[6]
    year = sys.argv[7]

    

    data_project = extract_projects(path_projects)
    data_advisors = extract_advisors(path_advisors)
    data_similarity = extract_simi(path_simi)

    add_revisors_aloc_to_projects(path_aloc, path_aloc_simi, data_project, data_advisors)    
    add_similarity_to_projects(data_project, data_advisors, data_similarity)
    write_csv(path_out, data_project)






















if __name__ == '__main__':
    main()