#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include "ilcplex/ilocplex.h"
#include <chrono>
#include <sstream>

#define NA 3 // Numero maximo de avaliadores por trabalho

#define LMini  0// Limite minimo de trabalhos por professor i
#define LMaxi  3 // Limite maximo de trabalhos por professor i


typedef struct {
	std::vector < int > trabalhosInteresse; // Trabalhos de interesse de um determinado orientador
} Orientador;


typedef struct {
	std::vector < int > orientadoresAptos; // Vector de orientadores que podem avaliar determinado trabalho
}Trabalho;


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




IloCplex* resolveModelo(int** beneficios, int quantiaOrientadores, int quantiaTrabalhos, std::vector < Orientador >& orientadores, std::vector < Trabalho >& trabalhos, const char * saidaNome, const char* resultadoNome) {

	
	auto start = std::chrono::high_resolution_clock::now(); // Pega o tempo do relogio

	
	IloEnv env; // Cria o ambiente de modelagem

	/* Criação do modelo, responsável por função objetivo e restrições	*/
	/* Precisa de um ambiente de modelagem para ser iniciado	*/
	IloModel Model(env);


	/* Criação da variavel de decisão	*/
	// Devemos enviar os parametros de ambiente  e quantia de linha inicial

	/* Utilização do template de classe IloArray para criar um	array de duas dimensões*/
	/* Do tipo IloNumVarArray, chamado x	*/
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
		
		/*	Retorna o vector contendo os indices dos trabalhos de interesse do orientador i	*/
		std::vector < int > trabalhosInteresseOrientador = orientadores[i].trabalhosInteresse;

		/* Percorre o vector de trabalho de interesse do orientador i e retorna os indices armazenados	*/
		/* Que são os trabalhos de interesse*/
		for(int j = 0; j < trabalhosInteresseOrientador.size(); j++) {
			
			int trabalhoIndice = trabalhosInteresseOrientador[j];
			exp0 += beneficios[i][trabalhoIndice] * x[i][trabalhoIndice];
		}
		trabalhosInteresseOrientador.clear();

	}

	Model.add(IloMaximize(env, exp0)); // Adiciona ao modelo para maximizar a função


	

	/* Restrições do problema 	*/

	
	/* Mantém fixo o valor de j e varia os valores de i	*/
	/* Como x[i][j] é uma variável binária que indica se o professor i foi alocado ao trabalho j ou não	*/
	/* Mantém fixo um determinado trabalho j e verifica se a soma dos professores que irão avaliar aquele trabalho	*/
	/* é igual ao número de avaliadores por trabalho	*/
	
	
	for(int j = 0; j < quantiaTrabalhos; j++) {
		IloExpr exp1(env); // Inicializa uma expressão

		/* Retorna o vector contendo os indices dos orientadores aptos a avaliares o trabalho j	*/
		std::vector < int > orientadoresAptos = trabalhos[j].orientadoresAptos;

		/* Percorre o vector e armazena os índices dos orientadores aptos e realiza o somatório */
		for(int i = 0; i < orientadoresAptos.size(); i++) {

			int indiceOrientadoresAptos = orientadoresAptos[i];
			exp1 += x[indiceOrientadoresAptos][j];
		}
		
		orientadoresAptos.clear();

		Model.add(exp1 == NA); // Adiciona ao modelo
	}

	

	/* Mantém fixo um determinado avaliador e verificamos em relação ao trabalho se ele possui os valores minimos e máximos	*/
	/* de Trabalhos para avaliar	*/
	for(int i = 0; i < quantiaOrientadores; i++) {

		IloExpr exp2(env);

		/* Retorna os trabalhos de interesse de um determinado orientador i	*/
		std::vector < int > trabalhosInteresseOrientador = orientadores[i].trabalhosInteresse;

		/* Pega os índices de trabalho de interesse do orientador e realiza o somatório	*/
		for(int j = 0; j < trabalhosInteresseOrientador.size(); j++) {

			int indiceTrabalhoInteresseOrientador = trabalhosInteresseOrientador[j];
			exp2 += x[i][indiceTrabalhoInteresseOrientador];
		}
		


		Model.add(exp2 <= LMaxi);
		Model.add(exp2 >= LMini);
	}

	
	IloCplex* cplexPtr = new IloCplex(Model);

	cplexPtr->exportModel(saidaNome); // Exporta o modelo no formato lp

	
	if(!cplexPtr->solve()) {

		env.error() << "Erro ao otimizar o problema" << '\n';
		throw(-1);
	}
	else {
		env.out() << "Otimizavel" << '\n';
	}

	double obj = cplexPtr->getObjValue();
	

	auto end = std::chrono::high_resolution_clock::now();

	auto elapsed = std::chrono::duration_cast < std::chrono::milliseconds > (end - start);

	std::cout << "Duracao(ms): " << elapsed.count() << '\n';
	std::cout << "O valor da função objetivo eh: " << obj << std::endl;
	
	int alocadosAreaEpecialidade = 0;
	int alocadosSubAreaEspecialidade = 0;
	int alocadosAreaDesconhecida = 0;
	int alocadosAoProprioTrabalho = 0;
	int alocadosANenhumaArea = 0;


	for(int j  = 0; j < quantiaTrabalhos; j++) {

		for(int i = 0; i < quantiaOrientadores; i++) {

			int xValue = cplexPtr->getValue(x[i][j]);

			if(xValue == 1) {
				
				if(beneficios[i][j] == 100) {
					alocadosSubAreaEspecialidade++;
				}
				else if(beneficios[i][j] == 10) {
					alocadosAreaEpecialidade++;
				}
				else if(beneficios[i][j] == 1) {
					alocadosANenhumaArea++;
				}
				else {
					alocadosAoProprioTrabalho;
				}

			}
		}
	}
	

	std::fstream *resultado = new std::fstream(resultadoNome, std::ios::out);

	std::stringstream result;
	result << "Alocados a sub area de especialidade: " << alocadosSubAreaEspecialidade << '\n' <<
	"Alocados a area de especialidade: " << alocadosAreaEpecialidade << '\n' <<
	"Alocados a nenhuma area de sua especialidade: " << alocadosANenhumaArea << '\n' << 
	"Alocados ao proprio trabalho: " << alocadosAoProprioTrabalho << '\n';

	*resultado << result.str();
	resultado->close();
	delete resultado;

	return cplexPtr;
}





int main(int argc, char** argv) {
	
	if(argc <  4) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}

	int quantiaOrientadores = 0;
	int quantiaTrabalhos = 0;

	
	int** beneficios = matrizBeneficios(argv[1], quantiaOrientadores, quantiaTrabalhos);

	/* Inicializando vetor de orientadores	*/
	std::vector < Orientador > orientadores;
	std::vector < int > trabalhosInteresse;

	/* Criação da matriz de trabalhos percentes a área de interesse de um professor/orientador i	*/
	for(int i = 0; i < quantiaOrientadores; i++) {

		Orientador orientador; // Instancia de um orientador
		for(int j = 0; j < quantiaTrabalhos; j++) {

			/* Adiciona os trabalhos de interesse do avaliador i ao vector trabalhosDeInteresse	*/ 	
			if(beneficios[i][j] == 10 || beneficios[i][j] == 100) {

				/* Insere o índice do trabalho que é da área de interesse do professor i	*/
				trabalhosInteresse.push_back(j);
			}
		}
		/* Adiciona os trabalhos de interesse do orientador i ao seus dados na struct	*/
		orientador.trabalhosInteresse = trabalhosInteresse;

		orientadores.push_back(orientador); // Adiciona o orientador

		trabalhosInteresse.clear(); // Limpa o vector
	}

	/* Inicializando vector de trabalhos e seus dados	*/
	std::vector < Trabalho > trabalhos;
	std::vector < int > orientadoresAptos;

	for(int j = 0; j < quantiaTrabalhos; j++) {

		Trabalho trabalho; // Inicializa um trabalho
		for(int i = 0; i < quantiaOrientadores; i++) {
			
			/* Se o beneficio é diferente de zero, é porque o orientador está apto para avaliar aquele projeto */
			if(beneficios[i][j] != 0) {
				orientadoresAptos.push_back(i);
			}
		}
		trabalho.orientadoresAptos = orientadoresAptos;
		trabalhos.push_back(trabalho);
		orientadoresAptos.clear();
	}


	IloCplex* cplex = resolveModelo(beneficios, quantiaOrientadores, quantiaTrabalhos, orientadores, trabalhos, argv[2], argv[3]);
	


	
	cplex->getEnv().end();
	delete cplex;
	
	for(int i = 0; i < quantiaOrientadores; i++) {

		delete beneficios[i];
	}

	delete beneficios;

	return 0;
}
