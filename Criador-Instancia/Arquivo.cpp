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

	std::string linha; // Linha do arquivo

	std::vector < Orientador* > *orientadoresVec = new std::vector < Orientador * > (); // Ponteiro para um vector de Orientador
	std::vector < Trabalho * > *trabalhosVec = new std::vector < Trabalho * > (); // Ponteiro para um vector de trabalhos

	InstanceDados dados(orientadoresVec, trabalhosVec); // Inicializa o objeto static que será padrão para todos os objetos

	std::string buffer;
	std::getline(*ptrInput, buffer); //Armazena o lixo do buffer inicial

	while(1) {

		
		std::getline(*ptrInput, linha);
		if(ptrInput->eof()) {
			break;
		}
		
		
		
		std::vector < std::string > *ptrString = StringAlgorithm::retornaStringSeparada(linha, ','); // Retorna a linha separada

		/* Verifica se existe algo	*/
		if(ptrString == NULL) {
			continue;
		}
		
		/*Queremos os indices 3, 5, 6 que são os orientadores, areas e subAreas*/
		Orientador orientador1((*ptrString)[3], (*ptrString)[5], (*ptrString)[6]);
		Orientador orientador2((*ptrString)[3], (*ptrString)[5], (*ptrString)[6]);
		
		/* Adiciona tanto os orientadores como os trabalhos em dados	*/
		dados.adicionaOrientador(orientador1);
		dados.adicionaTrabalho(orientador2);
		
	
		/* Deleta a região de memória criada pelo ptrString	*/
		delete ptrString;
	
	
	}

}
