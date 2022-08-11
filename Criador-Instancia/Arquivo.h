#ifndef ARQUIVO_H
#define ARQUIVO_H
 
#include <string>
#include <fstream>
#include "Orientador.h" 
#include <vector> 
#include "StringAlgorithm.h"
#include "InstanceDados.h"

class Arquivo {
	 
public:
 
	Arquivo(const std::string& nomeArquivo); /* Abertura do arquivo */
	virtual ~Arquivo();



	void lerArquivo();
  
private:

	std::fstream* ptrInput;
};













#endif
