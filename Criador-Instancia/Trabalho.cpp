#include "Trabalho.h"





Trabalho::Trabalho(Orientador& orientador) {

    std::string nome = orientador.getNome();
    std::string area = orientador.getArea();
    std::string subarea = orientador.getSubArea();

    this->orientador = new Orientador(nome, area, subarea);

}


Orientador* Trabalho::getOrientador() {

    return orientador;
}

Trabalho::~Trabalho() {

    delete this->orientador;
}


