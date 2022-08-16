#ifndef RESULTADO_H
#define RESULTADO_H

#include "InstanceDados.h"
#include <fstream>
#include <string>
#include <vector>
#include <sstream>


class Resultado {

public:
	/* Recebe o caminho que vai escrever os dados	*/
	Resultado(const std::string& caminho);
	virtual ~Resultado();

	void geraResultado();

private:

	std::fstream* resultado;

};














#endif
