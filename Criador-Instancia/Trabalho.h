#ifndef TRABALHO_H
#define TRABALHO_H


#include "Orientador.h"
#include <vector>



class Trabalho {

/* Um trabalho tem que ter apenas um orientador */
public:
	Trabalho(Orientador& orientador);
	Orientador *getOrientador();
	virtual ~Trabalho();


private:
	Orientador *orientador;

};








#endif
