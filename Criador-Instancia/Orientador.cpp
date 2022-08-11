#include "Orientador.h"









Orientador::Orientador(std::string& nome, std::string& area, std::string& subArea) {

	setNome(nome);
	setArea(area);
	setSubArea(subArea);
}



void Orientador::setNome(std::string& nomeValor) {

	this->nome = nomeValor;
}

void Orientador::setArea(std::string& areaValor) {

	this->area = areaValor;
}

void Orientador::setSubArea(std::string& subAreaValor) {

	this->subArea = subAreaValor;
}


std::string Orientador::getNome() {

	return this->nome;
}

std::string Orientador::getArea() {

	return this->area;
}

std::string Orientador::getSubArea() {

	return this->subArea;
}
