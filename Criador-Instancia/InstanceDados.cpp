#include "InstanceDados.h"
#include <iostream>



std::vector < Orientador* >  *InstanceDados::orientadoresPtr; //Declaração para dizer que todos os nomes dado como orientadoresPtr é o membro da classe


InstanceDados::InstanceDados(std::vector < Orientador * > *orientadores) {

	orientadoresPtr = orientadores;
}


InstanceDados::~InstanceDados() {

	for(auto iterator = orientadoresPtr->begin(); iterator != orientadoresPtr->end(); ++iterator) {
		
		std::cout << (*iterator)->getNome() << std::endl;
		delete *iterator;
	}
	delete this->orientadoresPtr;
}


void InstanceDados::adicionaOrientador(Orientador& orientadorDados) {

	bool existe = false;

	for(auto iterator = orientadoresPtr->begin(); iterator != orientadoresPtr->end(); ++iterator) {

		if(orientadorDados.getNome() == (*iterator)->getNome()) {

			existe = true;
		}
	
	}

	if(!existe) {
			
			std::string nome = orientadorDados.getNome();
			std::string area = orientadorDados.getArea();
			std::string subArea = orientadorDados.getSubArea();

			Orientador* ptrOrientador = new Orientador(nome, area, subArea);
			orientadoresPtr->push_back(ptrOrientador);
	}
}
