#include "StringAlgorithm.h"







 std::vector < std::string > *StringAlgorithm::retornaStringSeparada(std::string& linha, char separador) {
	
	/* Aloca a região de memória	*/
	std::vector < std::string > *ptrVector = new std::vector < std::string > ();

	std::string valor;

	ptrVector->clear();

	for(auto constIterator = linha.cbegin(); constIterator != linha.cend(); ++constIterator) {

		/*Quando achar achar o separador, coloca todos os valores dentro da string e limpar a string*/	
		if(*constIterator == separador) {
			
			ptrVector->push_back(valor);
			valor.clear();
			continue;

		}
		valor.push_back(*constIterator);
	
	}
	return ptrVector;

}
