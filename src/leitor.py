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



def find_advisor(advisors, name):
    for advisor in advisors:
        if name == advisor.get_name():
            return True

    return False



def main():
    
    if len(sys.argv) < 6:
        print("Digite a entrada: python3 leitor.py arquivo.csv dia instancia.txt advisor.csv resumes.csv")
        exit(1)
    
    input_path = str(sys.argv[1]) # Dados de entrada
    output_path = str(sys.argv[3])
    advisor_path = str(sys.argv[4])
    resumes_path = str(sys.argv[5])

    dia = int(sys.argv[2])


    resume_df = pd.read_csv(input_path, sep=',', encoding='UTF-8')
    data_df = Data(resume_df, dia)
    
    data_df.create_advisor_data(advisor_path)
    data_df.create_resumes_data(resumes_path)
    data_df.create_instance(output_path)
    
    






if __name__=="__main__":
    main()
