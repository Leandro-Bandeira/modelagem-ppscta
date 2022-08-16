#ifndef INSTANCE_DADOS_H
#define INSTANCE_DADOS_H
 
 
 
#include "Orientador.h"
#include <vector>
#include "Trabalho.h"
  
class InstanceDados { 
  
public: 
	InstanceDados(std::vector < Orientador* > *orientadores, std::vector < Trabalho * > *trabalhos);
  
	void adicionaOrientador(Orientador& orientadorDados);
	void adicionaTrabalho(Orientador& orientadorDados);
  
	virtual ~InstanceDados(); 
	static std::vector < Orientador* > * orientadoresPtr; //Devemos deixar como public, pois ele é um dado da classe e é unico
	static std::vector < Trabalho * > * trabalhos;
	static int tamanhoLinhas;

	void adicionaLinha(int valor);
};











#endif
