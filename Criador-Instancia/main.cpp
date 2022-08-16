#include <iostream>
#include <fstream>
#include "Arquivo.h"
#include "Resultado.h"





int main(int argc, char** argv) {
	
	if(argc < 3) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}


	Arquivo input(argv[1]);
	Resultado output(argv[2]);

	input.lerArquivo();

	output.geraResultado();

	return 0;
}
