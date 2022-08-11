#ifndef ORIENTADOR_H
#define ORIENTADOR_H
#include <string>






class Orientador {


public:
	Orientador(std::string& nome, std::string& area, std::string& subArea);
	
	/* Métodos set e gets 	*/
	void setNome(std::string& nome);
	void setArea(std::string& area);
	void setSubArea(std::string& subArea);
	

	std::string getNome();
	std::string getArea();
	std::string getSubArea();


private:
	std::string nome;
	std::string area, subArea;
};



















#endif
