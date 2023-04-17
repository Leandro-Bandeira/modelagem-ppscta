"""Codigo responsável por criar o modelo de chico
baseado em area e subarea"
"""
import json


def open_projetos(caminho):
    """Abre arquivo de projetos e retorna
    a lista de dicionarios"""
    with open(caminho) as file:
        data = json.load(file)
    return data


def read_orientadores(data_projetos):
    """Funcao responsável por retornar
    lista de orientadores junto com sua area e sub
    Verifica se um orientador ja foi visitado ou não
    Caso nao, cria um dicionario com seus dados importantes
    E entao o adiciona como visitado"""

    orientadores_visitado = list()
    orientadores_data = list()
    for i, projeto in enumerate(data_projetos):
        data_orientadores = dict()
        if projeto["Orientador:"] not in orientadores_visitado:
            orientadores_visitado.append(projeto["Orientador:"])
            data_orientadores["Indice"] = i
            data_orientadores["Orientador"] = projeto["Orientador:"]
            data_orientadores["Area"] = projeto["Area:"]
            data_orientadores["SubArea"] = projeto["SubArea:"]
            orientadores_data.append(data_orientadores)
    return orientadores_data


def write_instance(data_projetos, data_orientadores, path_instance):
    """Funcao responsavel por dado a lista de projetos
    e a lista de orientadores, podemos então criar a sua instancia
    Se o orientador avalia o trabalho na mesma area 100
    mesma subarea eh 10, caso nenhuma vale 1 alem disso,
    caso oriente o trabalho será -1"""

    with open(path_instance, 'w+') as instance:
        text = f'{len(data_orientadores)} {len(data_projetos)}\n'
        instance.write(text)
        for orientador in data_orientadores:
            beneficios = ''
            for projeto in data_projetos:
                if projeto["Orientador:"] == orientador["Orientador"]:
                    beneficios += "-1 "
                    continue
                if projeto["Area:"] == orientador["Area"]:
                    beneficios += "100 "
                elif projeto["SubArea:"] == orientador["SubArea"]:
                    beneficios += "10 "
                else:
                    beneficios += "1 "
            beneficios = beneficios.rstrip() + '\n'
            instance.write(beneficios)
    instance.close()


def main():
    """Funcao main responsável pelo codigo"""
    path_projetos = "../../DadosTrabalhos/projetos2014.json"
    path_instance = "instance14Chico.txt"
    path_orientadores = "orientadores14.json"

    data_projetos = open_projetos(path_projetos)
    data_orientadores = read_orientadores(data_projetos)
    write_instance(data_projetos, data_orientadores, path_instance)
    
    with open(path_orientadores, 'w') as file:
        json.dump(data_orientadores, file, indent=4, ensure_ascii=False)
    file.close()


if __name__ == "__main__":
    main()
