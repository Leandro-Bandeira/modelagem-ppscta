#include <iostream>
#include <fstream>
#include "Arquivo.h"
#include "Resultado.h"





int main(int argc, char** argv) {
	
	if(argc < 3) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}


	Arquivo input(argv[1]); // Abre o arquivo para leitura de dados
	Resultado output(argv[2]); // Abre o arquivo para inserção de dados

	input.lerArquivo();

	output.geraResultado();

	return 0;
}
