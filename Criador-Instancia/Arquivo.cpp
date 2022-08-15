#include "Arquivo.h"
#include <iostream>


Arquivo::Arquivo(const std::string& nomeArquivo) {

	/* Aponta para a região	*/
	ptrInput = new std::fstream(nomeArquivo, std::ios::in);


}

Arquivo::~Arquivo() {
	
	ptrInput->close();
	delete ptrInput;
}

void Arquivo::lerArquivo() {

	std::string linha;

	std::vector < Orientador* > *orientadoresVec = new std::vector < Orientador * > (); // Ponteiro para um vector de Orientador
	InstanceDados dados(orientadoresVec); // Inicializa o objeto static que será padrão para todos os objetos

	std::string buffer;
	std::getline(*ptrInput, buffer); //Armazena o lixo do buffer inicial

	int i = 0;
	while(1) {

		
		std::getline(*ptrInput, linha);
		if(ptrInput->eof()) {
			break;
		}
		
		
		
		std::vector < std::string > *ptrString = StringAlgorithm::retornaStringSeparada(linha, ',');

		/* Verifica se existe algo	*/
		if(ptrString == NULL) {
			continue;
		}
		
		/*Queremos os indices 3, 5, 6 que são os orientadores, areas e subAreas*/
		Orientador orientador1((*ptrString)[3], (*ptrString)[5], (*ptrString)[6]);
		dados.adicionaOrientador(orientador1);
		
	
		delete ptrString;
	
	
	}

}
