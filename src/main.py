import pandas as pd
import sys
import os

class Advisor:

    def __init__(self, name, area, grande_area, sub_area, especiality):
        self.name = name
        self.area = area
        self.grande_area = grande_area
        self.sub_area = sub_area
        self.especiality = especiality

    def get_name(self):
        
        return self.name

    def get_advisor(self):
        
        return self.name_advisor
        
    def get_area(self):
        
        return self.area

    def get_sub_area(self):
        
        return self.sub_area

    def get_grande_area(self):
        
        return self.grande_area

    def get_especiality(self):
        
        return self.especiality




class Resume:
        def __init__(self, name_author, name_advisor, area, grande_area, sub_area, especiality):
            self.name_author = name_author
            self.name_advisor = name_advisor
            self.area = area
            self.grande_area = grande_area
            self.sub_area = sub_area
            self.especiality = especiality
        
        def get_name_author(self):

            return self.name_author

        def get_advisor(self):

            return self.name_advisor
        
        def get_area(self):
            
            return self.area

        def get_sub_area(self):
            
            return self.sub_area

        def get_grande_area(self):
            
            return self.grande_area

        def get_especiality(self):
            
            return self.especiality


class Data:

    def __init__(self, resumes_df, dia):
        self.advisors = list()
        self.resumes = list()
        for index in range(resumes_df.shape[0]):
            row = resumes_df.iloc[index]

            if dia == int(row['DIA']) :
                advisor_name = row['nome_orientador']
                if not find_advisor(self.advisors, advisor_name): # Verifica se o orientador não já foi adicionado
                    # Criação de um advisor junto com seu nome e suas áreas
                    self.advisors.append(Advisor(row['nome_orientador'], row['area_cnpq'
                        ], row['grande_area_cnpq'], row['sub_area'], row['especialidade']))
                # Criação da lista de resumos
                self.resumes.append(Resume(row['nome_aluno_autor'], row['nome_orientador'],
                        row['area_cnpq'], row['grande_area_cnpq'], row['sub_area'],
                        row['especialidade']))
    

    # Função responsável por calcular as porcentagem de similaridade
    def calculate_datas(self, path_model):

        file = open(path_model, "r")
        file_lines = file.readlines();
        count_same_especiality = 0
        count_same_subarea = 0
        count_same_area = 0
        count_same_grand_area = 0
        count_nt = 0

        # Vamos ler cada linha que representa um trabalho
        # e verificar se aquele revisor foi alocado a um trabalho com o qual possui 
        # especialidade, subárea, área ou grande_area em comum
        for id_project,line in enumerate(file_lines):
            line = line.strip()
            advisors_allocated = line.split()

            for id_advisor in advisors_allocated:

                if self.resumes[id_project].get_especiality() == self.advisors[int(id_advisor)].get_especiality():
                    count_same_especiality += 1
                elif self.resumes[id_project].get_sub_area() == self.advisors[int(id_advisor)].get_sub_area():
                    count_same_subarea += 1
                elif self.resumes[id_project].get_area() == self.advisors[int(id_advisor)].get_area():
                    count_same_area += 1 
                elif self.resumes[id_project].get_grande_area() == self.advisors[int(id_advisor)].get_grande_area():
                    count_same_grand_area += 1 
                else:
                    count_nt += 1


        print(f'Foram alocados a mesma especialidade, subárea, área e grande área e a nenhum, respectivamente: {count_same_especiality}, {count_same_subarea}, {count_same_area}, {count_same_grand_area}, {count_nt}')

    # Cria o arquivo de instancia estruturado da seguinte forma
    # Quantia de orientadores |  Quantia de trabalhos
    # A partir do primeiro orientador verifica a relação dele com todos os trabalhos
    # Se ele avalia o proprio trabalho seu benefício é -1 e vai seguindo por ordem de prioridade
    # 1000 para especialidade igual, 100 para mesma subárea, 10 para mesma área, 1 para mesma grande área
    # e beneficio 0 caso não tenha nenhuma área igual
    def create_instance(self, output_path):
        
        instance = open(output_path, 'w')
        instance.write(str(len(self.advisors))+' '+str(len(self.resumes))+'\n')
        
        for advisor in self.advisors:
            for resume in self.resumes:
                if advisor.get_name() == resume.get_advisor():
                    instance.write('-1 ')
                elif advisor.get_especiality() == resume.get_especiality():
                    instance.write("1000 ")
                elif advisor.get_sub_area() == resume.get_sub_area():
                    instance.write("100 ")
                elif advisor.get_area() == resume.get_area():
                    instance.write("10 ")
                elif advisor.get_grande_area() == resume.get_grande_area() :
                    instance.write("1 ")
                else:
                    instance.write("0 ")
            instance.write("\n")

    # Criação do arquivo que contém todos os dados dos orientadores em relação a lista inicial
    def create_advisor_data(self, advisor_path):
        advisor_csv = open(advisor_path, "w")

        advisor_csv.write("NOME\tGRANDE_AREA\tAREA\tSUB_AREA\tESPECIALIDADE\n")

        for advisor in self.advisors:

            advisor_csv.write("{nome}\t{garea}\t{area}\t{subarea}\t{especialidade}\n".format(nome=advisor.get_name()
                , garea=advisor.get_grande_area(),
                area=advisor.get_area(),subarea=advisor.get_sub_area(),
                especialidade=advisor.get_especiality()))
        
        advisor_csv.close()

    # Criação do arquivo que contém os dados dos trabalhos
    def create_resumes_data(self, resumes_path):
        resumes_csv = open(resumes_path, "w")

        resumes_csv.write("NOME_AUTOR\tNOME_ORIENTADOR\tGRANDE_AREA\tAREA\tSUB_AREA\tESPECIALIDADE\n")

        for resume in self.resumes:

            resumes_csv.write("{nome_autor}\t{nome_advisor}\t{garea}\t{area}\t{subarea}\t{especialidade}\n".format(nome_autor=resume.get_name_author()
                , nome_advisor=resume.get_advisor(),garea=resume.get_grande_area(),
                area=resume.get_area(),subarea=resume.get_sub_area(),
                especialidade=resume.get_especiality()))
        
        resumes_csv.close()

    # Criação do arquivo que contém a variável w[i][j]
    # Ela será 1 ou 0 caso o orientador foi alocado ao trabalho j no enic
    def create_variable_file(self, variable_path, enic_df):
        variable_file = open(variable_path, "w")
        

        trabalhos_alocados_orientadores = list()
        for advisor in self.advisors:
            trabalhos_alocados = 0
            
            for index in range(enic_df.shape[0]):
                row = enic_df.iloc[index]
                author_name = row['ALUNO']

                avaliador1 = row['AVALIADOR1']
                avaliador2 = row['AVALIADOR2']
                # Primeiro checa se o valor é nan e depois se a linha tem aluno
                if author_name != author_name or author_name  == "ALUNO": 
                    continue
                
                # Se ele foi alocado como avaliador, vamos achar
                # o indice correspondente no array padrão e salvar no arquivo
                if advisor.get_name().rstrip() == avaliador1.rstrip() or advisor.get_name() == avaliador2.rstrip():
                    trabalhos_alocados += 1

                    for id,resume in enumerate(self.resumes):
                        
                        if resume.get_name_author().rstrip() == author_name.rstrip():
                            variable_file.write(str(id) + ' ')
                            break
                    
            
            trabalhos_alocados_orientadores.append(trabalhos_alocados)
            variable_file.write('\n')
        variable_file.write(str(min(trabalhos_alocados_orientadores)) + ' ' + str(max(trabalhos_alocados_orientadores)) + '\n')
        variable_file.close()
                


def find_advisor(advisors, name):
    for advisor in advisors:
        if name == advisor.get_name():
            return True

    return False



def main():
    
    if len(sys.argv) < 4:
        print("Digite a entrada: python3 leitor.py dia ano campus_numero")
        exit(1)
    
    dia = int(sys.argv[1])
    ano = int(sys.argv[2])
    campus_numero = int(sys.argv[3])

    input_path = f'../DadosTrabalhos/dadosEnic{ano}.csv' # Dados de entrada
    enic_path  = f'../DadosTrabalhos/campus{campus_numero}_{dia}.csv'

    # Configuração do caminho de saída dos arquivos
    output_path = "../results/instancia_{dia}.txt".format(dia=dia)
    variable_path = "../results/variable_{dia}.txt".format(dia=dia)
    advisor_path = "../results/advisor_{dia}.csv".format(dia=dia)
    resumes_path = "../results/resumes_{dia}.csv".format(dia=dia)
    

    
    resume_df = pd.read_csv(input_path, sep=',', encoding='UTF-8') # Criação do dataFrame em relação aos dados do enic
    enic_df = pd.read_csv(enic_path, sep=',', encoding='UTF-8') # Criaçãod o dataFrame em relação aos resultados doe nic



    data_df = Data(resume_df, dia) # Criação da lista de resumos e advisors em relação aos dados do Enic
    data_df.create_advisor_data(advisor_path) # Cria o arquivo que contém os dados dos orientadores
    data_df.create_resumes_data(resumes_path) # Cria o arquivo que contém os dados dos trabalhos
    data_df.create_instance(output_path) # Cria o arquivo de instancia do modelo
    data_df.create_variable_file(variable_path, enic_df)

    # Após a criação dos arquivos podemos executar a aplicação em c++
    os.chdir("../")
    os.system("make")
    os.chdir("src")
    os.system(f'./solver ../results/instancia_{dia}.txt ../results/variable_{dia}.txt ../results/modelo_{dia}.lp')
    
    data_df.calculate_datas("../results/outputModel.txt")






if __name__=="__main__":
    main()
