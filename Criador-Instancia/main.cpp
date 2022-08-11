#include <iostream>
#include <fstream>
#include "Arquivo.h"






int main(int argc, char** argv) {
	
	if(argc < 2) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}


	Arquivo input(argv[1]);

	input.lerArquivo();
	return 0;
}
