#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdlib.h>

void matrizBeneficios(const std::string& caminho) {
	
	std::fstream* ptrArquivo = new std::fstream(caminho, std::ios::in);
	
	int colunas, linhas;

	std::string linha;
	
	std::vector < int > valoresLinha; // Valores que vão estar na linha
	
	while(1) {

		std::getline(*ptrArquivo, linha);
		if(ptrArquivo->eof()) {

			break;
		}
			

		std::stringstream dadosLinha(linha);
		std::string palavra;

		while(std::getline(dadosLinha, palavra, ' ')) {
			
			valoresLinha.push_back(atoi(palavra.c_str()));


		}

		for(int i  = 0; i < valoresLinha.size(); i++) {

			std::cout << valoresLinha[i] << " ";
		}
		std::cout << std::endl;
		valoresLinha.clear();
		break;

	}

	ptrArquivo->close();
	delete ptrArquivo;



}








int main(int argc, char** argv) {
	
	if(argc <  2) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}

	int quantiaOrientadores = 0;
	int quantiaTrabalhos = 0;

	
	matrizBeneficios(argv[1]);


	return 0;
}
