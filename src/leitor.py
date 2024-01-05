import pandas as pd
import sys
import os
import math


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
                if not find_advisor(self.advisors, advisor_name):
                    self.advisors.append(Advisor(row['nome_orientador'], row['area_cnpq'
                        ], row['grande_area_cnpq'], row['sub_area'], row['especialidade']))

                self.resumes.append(Resume(row['nome_aluno_autor'], row['nome_orientador'],
                        row['area_cnpq'], row['grande_area_cnpq'], row['sub_area'],
                        row['especialidade']))
        
    def create_instance(self, output_path):
        
        instance = open(output_path, 'w')
        instance.write(str(len(self.advisors))+'\n'+str(len(self.resumes))+'\n')
        
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

    def create_advisor_data(self, advisor_path):
        advisor_csv = open(advisor_path, "w")

        advisor_csv.write("NOME\tGRANDE_AREA\tAREA\tSUB_AREA\tESPECIALIDADE\n")

        for advisor in self.advisors:

            advisor_csv.write("{nome}\t{garea}\t{area}\t{subarea}\t{especialidade}\n".format(nome=advisor.get_name()
                , garea=advisor.get_grande_area(),
                area=advisor.get_area(),subarea=advisor.get_sub_area(),
                especialidade=advisor.get_especiality()))
        
        advisor_csv.close()

        
    def create_resumes_data(self, resumes_path):
        resumes_csv = open(resumes_path, "w")

        resumes_csv.write("NOME_AUTOR\tNOME_ORIENTADOR\tGRANDE_AREA\tAREA\tSUB_AREA\tESPECIALIDADE\n")

        for resume in self.resumes:

            resumes_csv.write("{nome_autor}\t{nome_advisor}\t{garea}\t{area}\t{subarea}\t{especialidade}\n".format(nome_autor=resume.get_name_author()
                , nome_advisor=resume.get_advisor(),garea=resume.get_grande_area(),
                area=resume.get_area(),subarea=resume.get_sub_area(),
                especialidade=resume.get_especiality()))
        
        resumes_csv.close()

    
    def create_variable_file(self, variable_path, enic_df):
        variable_file = open(variable_path, "w")
        

        for advisor in self.advisors:
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
                    for id,resume in enumerate(self.resumes):
                        
                        if resume.get_name_author().rstrip() == author_name.rstrip():
                            variable_file.write(str(id) + ' ')
                            break
                    

            
            variable_file.write('\n')

        variable_file.close()
                


def find_advisor(advisors, name):
    for advisor in advisors:
        if name == advisor.get_name():
            return True

    return False



def main():
    
    if len(sys.argv) < 4:
        print("Digite a entrada: python3 leitor.py DadosEnic.csv dia ResultadosEnic.csv")
        exit(1)
    
    input_path = str(sys.argv[1]) # Dados de entrada
    dia = int(sys.argv[2])
    enic_path = str(sys.argv[3])

    output_path = "../results/instancia_{dia}.txt".format(dia=dia)
    variable_path = "../results/variable_{dia}.txt".format(dia=dia)
    advisor_path = "../results/advisor_{dia}.csv".format(dia=dia)
    resumes_path = "../results/resumes_{dia}.csv".format(dia=dia)
    





    resume_df = pd.read_csv(input_path, sep=',', encoding='UTF-8')
    enic_df = pd.read_csv(enic_path, sep=',', encoding='UTF-8')



    data_df = Data(resume_df, dia)
    data_df.create_advisor_data(advisor_path)
    data_df.create_resumes_data(resumes_path)
    data_df.create_instance(output_path)
    data_df.create_variable_file(variable_path, enic_df)

    
    






if __name__=="__main__":
    main()
