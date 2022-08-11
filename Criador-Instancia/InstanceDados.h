#ifndef INSTANCE_DADOS_H
#define INSTANCE_DADOS_H



#include "Orientador.h"
#include <vector>

class InstanceDados {

public:
	InstanceDados(std::vector < Orientador* > *orientadores);

	void adicionaOrientador(Orientador& orientadorDados);

	virtual ~InstanceDados();
	static std::vector < Orientador* > * orientadoresPtr; //Devemos deixar como public, pois ele é um dado da classe e é unico
	
};











#endif
