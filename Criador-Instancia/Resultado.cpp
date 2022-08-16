#include "Resultado.h"
#include <iostream>


Resultado::Resultado(const std::string& caminho) {
	
	this->resultado = new std::fstream(caminho, std::ios::out);


}


Resultado::~Resultado() {

	resultado->close();
	delete resultado;

	std::vector < Orientador * > *orientadoresPtr = InstanceDados::orientadoresPtr;
	std::vector < Trabalho * > *trabalhos= InstanceDados::trabalhos;

	
	for(auto iterator = orientadoresPtr->begin(); iterator != orientadoresPtr->end(); ++iterator) {
		
		delete *iterator;
	}
	delete orientadoresPtr;

	
	for(auto iterator = trabalhos->begin(); iterator != trabalhos->end(); ++iterator) {
		
		
		delete *iterator;
	}

	
	delete trabalhos;
	
}


void Resultado::geraResultado() {

	std::vector < std::vector < double > > matriz;
	
	std::vector < double > linha;

	/* Alocação de dados	*/
	std::vector < Orientador * > *ptrOrientador = InstanceDados::orientadoresPtr;
	std::vector < Trabalho * > *ptrTrabalhos = InstanceDados::trabalhos;

	
	for(auto constIteratorOrientador = ptrOrientador->cbegin(); constIteratorOrientador != ptrOrientador->cend(); ++constIteratorOrientador) {
		
		linha.clear();
		int numero = 0;

		for(auto constIteratorTrabalhos = ptrTrabalhos->cbegin(); constIteratorTrabalhos != ptrTrabalhos->cend(); ++constIteratorTrabalhos) {


				/* Caso seja os mesmos orientadores, indicamos que sao inaptos	*/
				if((*constIteratorOrientador)->getNome() == (*constIteratorTrabalhos)->getOrientador()->getNome()) {

					linha.push_back(0);
				}

				else if((*constIteratorOrientador)->getSubArea() ==  (*constIteratorTrabalhos)->getOrientador()->getSubArea()) {
					
					
					linha.push_back(100);

				}
				else if((*constIteratorOrientador)->getArea() == (*constIteratorTrabalhos)->getOrientador()->getArea()) {

					linha.push_back(10);
				}
				else {

					linha.push_back(1);
				}
				
			
			numero++;

		}
		matriz.push_back(linha);
	}

	for(std::vector < double > linha : matriz) {

		std::stringstream string;
	

		for(auto constIterator = linha.cbegin(); constIterator != linha.cend(); ++constIterator) {

				
				string << *constIterator  <<  ' ';
		}
		string << '\n';

		*resultado  << string.str();
		string.clear();
	}

}
