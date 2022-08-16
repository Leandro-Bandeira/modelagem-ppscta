#include "InstanceDados.h"
#include <iostream>



std::vector < Orientador* >  *InstanceDados::orientadoresPtr; //Declaração para dizer que todos os nomes dado como orientadoresPtr é o membro da classe
std::vector < Trabalho * >   *InstanceDados::trabalhos;

InstanceDados::InstanceDados(std::vector < Orientador * > *orientadores, std::vector < Trabalho * > *trabalhosPtr) {

	orientadoresPtr = orientadores;
	trabalhos = trabalhosPtr;
}


InstanceDados::~InstanceDados() {

}


void InstanceDados::adicionaOrientador(Orientador& orientadorDados) {

	bool existe = false;
	
	/* Verifica a existencia no vector do autor, caso não exista adiciona ele */
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

void InstanceDados::adicionaTrabalho(Orientador& orientadorDados) {
	
	/* O trabalho não precisa ter a mesma logica dos orientadores, pegamos todos os trabalhos	*/
	Trabalho* trabalhoptr = new Trabalho(orientadorDados);
	trabalhos->push_back(trabalhoptr);
}
