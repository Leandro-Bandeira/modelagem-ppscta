#include "StringAlgorithm.h"
#include <iostream>
#include <ctype.h>





 std::vector < std::string > *StringAlgorithm::retornaStringSeparada(std::string& linha, char separador) {
	
	/* Aloca a região de memória	*/
	std::vector < std::string > *ptrVector = new std::vector < std::string > ();
	

	std::string valor;

	ptrVector->clear();
	valor.clear();
	
	
	for(int i = 0; i < linha.size() - 1; i++) {

		/*Quando achar achar o separador, coloca todos os valores dentro da string e limpar a string*/
		if(linha[i] == separador) {
			
			ptrVector->push_back(valor);
			valor.clear();
			continue;

		}
		valor.push_back(linha[i]);
		
	
	}

	
	if(ptrVector->size() != 0) {	
		return ptrVector;
	}

	
	delete ptrVector;
	return NULL;
		
	

}
