#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include "ilcplex/ilocplex.h"
#include <chrono>
#include <sstream>

#define NA 4 // Numero maximo de avaliadores por trabalho
<<<<<<< HEAD
#define LMini  4// Limite minimo de trabalhos por professor i
#define LMaxi  5 // Limite maximo de trabalhos por professor i
=======
#define LMini  3// Limite minimo de trabalhos por professor i
#define LMaxi  4 // Limite maximo de trabalhos por professor i
>>>>>>> eb527e2f9664a7ebc3f139556998e1034e1a654c


 


int **matrizBeneficios(const std::string& caminho, int& quantiaOrientadores, int& quantiaTrabalhos) {
	
	std::fstream* ptrArquivo = new std::fstream(caminho, std::ios::in); // Abre o arquivo para entrada de dados
	
	std::string linha; // Linha lida no arquivo
	
	std::vector < int > valoresLinha; // Valores que vão estar na linha



	int repeticoes = 0;



	std::getline(*ptrArquivo, linha);

	std::stringstream dadosLinha(linha); // Cria uma stream de string da linha
	std::string palavra; // Variável onde será armazenada temporariamente a palavra

	while(std::getline(dadosLinha, palavra, ' ')) {
			
		valoresLinha.push_back(atoi(palavra.c_str())); // Converte para inteiro e colocar no vector valores da linha
	}
		
			
	quantiaOrientadores = valoresLinha[0];
	quantiaTrabalhos = valoresLinha[1];

		
		

	
	valoresLinha.clear(); // Limpa o vector
	linha.clear();

	/* Criação da matriz de beneficios	*/
	int** matriz = new int*[quantiaOrientadores];

	for(int i = 0; i < quantiaOrientadores; i++) {

		matriz[i] = new int[quantiaTrabalhos];
	}
	

	int indiceLinha = 0;
	while(1) {
		

		std::getline(*ptrArquivo, linha); // Ler a linha

		if(ptrArquivo->eof())
			break;


		std::stringstream dados(linha); // Crima uma stream de string
		
		// Separa os dados da string de stream pelo espaço e então armazena no vector de valores
		while(std::getline(dados, palavra, ' ')) {

			valoresLinha.push_back(atoi(palavra.c_str()));
		}
		
		// Percorre em relação a coluna, mantendo o indice da linha fixo
		for(int j = 0; j < valoresLinha.size(); j++) {
			
			matriz[indiceLinha][j] = valoresLinha[j];

		}

		/* Limpeza de todos os dados	*/
		valoresLinha.clear();
		linha.clear();
		indiceLinha++;

	} 
		 

	ptrArquivo->close();
	delete ptrArquivo;
	

	return matriz;


}




void resolveModelo(int** beneficios, int quantiaOrientadores, int quantiaTrabalhos) {

	auto start = std::chrono::high_resolution_clock::now(); // Pega o tempo do relogio

	IloEnv env; // Cria o ambiente de modelagem

	/* Criação do modelo, responsável por função objetivo e restrições	*/
	/* Precisa de um ambiente de modelagem para ser iniciado	*/
	IloModel Model(env);


	/* Criação da variavel de decisão	*/
	// Devemos enviar os parametros de ambiente  e quantia de linha inicial

	/* Utilização do template de classe IloArray para criar um	array de duas dimensões*/
	/* Do tipo IloNumVarArray, chamado x*/
	IloArray < IloNumVarArray > x(env, quantiaOrientadores);

	/* Acessamos cada valor dessa linha inicial, e iniciamos um array com o ambiente, tamanho, indice incial e assim	*/
	for(int i = 0; i < quantiaOrientadores; i++) {
		
		// Criamos um array com numero de colunas igual a quantia de trabalho
		// Limite inferior 0 e limite superior 1, todos como inteiro
		x[i] = IloNumVarArray(env, quantiaTrabalhos, 0, 1, ILOINT);
	}


	/* Adicionando nome das variaveis	*/
	char var[100];

	for(int i = 0; i < quantiaOrientadores; i++) {

		for(int j = 0; j < quantiaTrabalhos; j++) {

			/* Armazena a string formatada  na variável var e seta o nome	*/
			sprintf(var, "x[%d][%d]", i, j);
			x[i][j].setName(var);
			Model.add(x[i][j]);

		}
	}



	/* Criação da função objetivo	*/
	IloExpr exp0(env); // Inicializa uma expressão

	
	for(int i = 0; i < quantiaOrientadores; i++) {

		for(int j = 0; j < quantiaTrabalhos; j++) {
			
			exp0 += beneficios[i][j] * x[i][j];

		}
	}

	Model.add(IloMaximize(env, exp0)); // Adiciona ao modelo para maximizar a função


	

	/* Restrições do problema 	*/

	
	/* Mantém fixo o valor de j e varia os valores de i	*/
	/* Como x[i][j] é uma variável binária que indica se o professor i foi alocado ao trabalho j ou não	*/
	/* Mantém fixo um determinado trabalho j e verifica se a soma dos professores que irão avaliar aquele trabalho	*/
	/* é igual ao número de avaliadores por trabalho	*/

	for(int j = 0; j < quantiaTrabalhos; j++) {
		IloExpr exp1(env); // Inicializa uma expressão

		for(int i = 0; i < quantiaOrientadores; i++) {
			exp1 += x[i][j];
		}
		Model.add(exp1 == NA); // Adiciona ao modelo
	}

	/* Mantém fixo um determinado avaliador e verificamos em relação ao trabalho se ele possui os valores minimos e máximos	*/
	/* de Trabalhos para avaliar	*/
	for(int i = 0; i < quantiaOrientadores; i++) {

		IloExpr exp2(env);

		for(int j = 0; j < quantiaTrabalhos; j++) {

			exp2 += x[i][j];
		}

		//Model.add(LMini <= exp2 <= LMaxi);
		Model.add(exp2 >= LMini);
		Model.add(exp2 <= LMaxi);
		
	}

	
	IloCplex cplex(Model);
<<<<<<< HEAD
	cplex.exportModel("modelo5.lp"); // Exporta o modelo no formato lp
=======
	cplex.exportModel("modeloName.lp"); // Exporta o modelo no formato lp
>>>>>>> eb527e2f9664a7ebc3f139556998e1034e1a654c

	cplex.setParam(IloCplex::Param::WorkMem,  6000);

	
	if(!cplex.solve()) {

		env.error() << "Erro ao otimizar o problema" << '\n';
		throw(-1);
	}
	else {
		env.out() << "Otimizavel" << '\n';
	}

	double obj = cplex.getObjValue();
	

	auto end = std::chrono::high_resolution_clock::now();

	auto elapsed = std::chrono::duration_cast < std::chrono::milliseconds > (end - start);

	std::cout << "Duracao(ms): " << elapsed.count() << '\n';
	std::cout << "O valor da função objetivo eh: " << obj << std::endl;

	
	for(int i = 0; i < quantiaOrientadores; i++) {

		for(int j = 0; j < quantiaTrabalhos; j++) {
 
			int xValue = cplex.getValue(x[i][j]);

			std::cout << "x[ " << i << "]" << "[" << j << "]" << " = " << xValue << '\n';
		}
	}
	
	
	env.end();

}





int main(int argc, char** argv) {
	
	if(argc <  2) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}

	int quantiaOrientadores = 0;
	int quantiaTrabalhos = 0;

	
	int** beneficios = matrizBeneficios(argv[1], quantiaOrientadores, quantiaTrabalhos);
	
	resolveModelo(beneficios, quantiaOrientadores, quantiaTrabalhos);

	
	for(int i = 0; i < quantiaOrientadores; i++) {

		delete beneficios[i];
	}

	delete beneficios;

	return 0;
}
