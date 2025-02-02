"""Codigo responsável por criar o modelo de chico
baseado em area e subarea, caso tenham a mesma subarea
o beneficio eh 100 caso não o beneficio eh 10,
além disso, caso um orientador oriente mais de um trabalho vamos considerar a maior similaridade dele
por exemplo, caso ele oriente os trabalhos 1 e 2, mas a similaridade de 1 com 3 é 20% e a similaridade de 2 com 3 é 60%, então iremos pegar 60"
caso ele oriente o trabalho seu beneficio é jogado para zero
"""
import json


def open_projetos(caminho):
    """Abre arquivo de projetos e retorna
    a lista de dicionarios"""
    with open(caminho) as file:
        data = json.load(file)
    return data



def open_similarity(caminho):

    """Abre o arquivo de similaridade """

    with open(caminho) as file:
        data = json.load(file)

    return data
  
def read_orientadores(path_orientadores):
    """Funcao responsável por retornar
    lista de orientadores junto com sua area e sub
    Verifica se um orientador ja foi visitado ou não
    Caso nao, cria um dicionario com seus dados importantes
    E entao o adiciona como visitado"""

    with open(path_orientadores) as file:
        data = json.load(file)
    
    return data


def write_instance(data_projetos, data_orientadores, path_instance, data_similarity):
    """Funcao responsavel por dado a lista de projetos
    e a lista de orientadores, podemos então criar a sua instancia
    Se o orientador avalia o trabalho na mesma area 100
    mesma subarea eh 10, caso nenhuma vale 1 alem disso,
    caso oriente o trabalho será -1"""
    is_instance_chico = False

    with open(path_instance, 'w+') as instance:
        text = f'{len(data_orientadores)} {len(data_projetos)}\n'
        instance.write(text)
        for i, orientador in enumerate(data_orientadores):
            projetos_orientados = orientador["Projetos"]
            
            beneficios_string = ''
            beneficios = float()

            for j, projeto in enumerate(data_projetos):

                similarity_list = data_similarity[projetos_orientados[0]]["similaridade"].split(' ') # Conjunto de similaridade entre todos os trabalhos do primeiro projeto do orientador
                best_similarity = float(similarity_list[j]) # Retira a similaridade entre o primeiro projeto e aquele trabalho j

                # Retorna a melhor similaridade em relação ao trabalho j de todos os trabalhos que o orientador orienta
                for id_projetos_orientados in projetos_orientados:
                    similarity_list = data_similarity[id_projetos_orientados]["similaridade"].split(' ')
                    similarity_atual = float(similarity_list[j])

                    if similarity_atual > best_similarity:
                        best_similarity = similarity_atual  
                
                similarity = best_similarity
                if similarity < 0:
                    similarity = 0

                if projeto["Orientador:"] == orientador["Nome"] or projeto["id"] in projetos_orientados:
                    beneficios_string += "0 "
                    continue
                #Se for a instancia de chico vamos apenas deixar beneficios como zero
                if is_instance_chico:
                    beneficios = 0
                else:
                    beneficios = round((similarity * 100), 2)
                
                if projeto["SubArea:"] == orientador["SubArea"]:
                    beneficios_string += str(beneficios + 1000) + ' '

                elif projeto["Area:"] == orientador["Area"]:
                    beneficios_string += str(beneficios + 100) + ' '
                else:
                    beneficios_string += str(beneficios + 1) + ' '
                    
                    
                    
            beneficios_string = beneficios_string.rstrip() + '\n'
            instance.write(beneficios_string)
    instance.close()


def main():
    """Funcao main responsável pelo codigo"""
    path_projetos = "../DadosTrabalhos/projetos2017.json"
    path_instance = "instance17Chico.txt"
    path_orientadores = "orientadores17.json"
    path_similarity = "../DadosTrabalhos/similarityOrientadores17AliDoc2Vec.json"

    data_projetos = open_projetos(path_projetos)
    data_orientadores = read_orientadores(path_orientadores)
    data_similarity = open_similarity(path_similarity)


    write_instance(data_projetos, data_orientadores, path_instance, data_similarity)
    
    with open(path_orientadores, 'w') as file:
        json.dump(data_orientadores, file, indent=4, ensure_ascii=False)
    file.close()


if __name__ == "__main__":
    main()
