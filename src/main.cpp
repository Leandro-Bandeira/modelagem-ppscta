#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include "ilcplex/ilocplex.h"
#include <chrono>
#include <sstream>

#define NA 2 // Numero maximo de avaliadores por trabalho

#define LMini  2// Limite minimo de trabalhos por professor i
#define LMaxi  4 // Limite maximo de trabalhos por professor i


typedef struct {
	std::vector < int > trabalhosInteresse; // Trabalhos de interesse de um determinado orientador
} Orientador;


typedef struct {
	std::vector < int > orientadoresAptos; // Vector de orientadores que podem avaliar determinado trabalho
}Trabalho;


double **matrizBeneficios(const std::string& caminho, int& quantiaOrientadores, int& quantiaTrabalhos) {
	
	std::fstream* ptrArquivo = new std::fstream(caminho, std::ios::in); // Abre o arquivo para entrada de dados
	
	std::string linha; // Linha lida no arquivo
	
	std::vector < double > valoresLinha; // Valores que vão estar na linha



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
	double** matriz = new double*[quantiaOrientadores];

	for(int i = 0; i < quantiaOrientadores; i++) {

		matriz[i] = new double[quantiaTrabalhos];
	}
	
	
	int indiceLinha = 0;
	while(1) {
		

		std::getline(*ptrArquivo, linha); // Ler a linha

		if(ptrArquivo->eof())
			break;


		std::stringstream dados(linha); // Crima uma stream de string
		
		// Separa os dados da string de stream pelo espaço e então armazena no vector de valores
		while(std::getline(dados, palavra, ' ')) {

			std::string::size_type sz;
			if(palavra.size() >  0) {
				//std::cout << palavra << " " << palavra.size();
				valoresLinha.push_back(std::stod(palavra, &sz));
			}
			
			
			
		}
		
		// Percorre em relação a coluna, mantendo o indice da linha fixo
		for(int j = 0; j < valoresLinha.size(); j++) {
			
			/* Garantir q iremos armazenar apenas a quantia de trabalhos	*/
			if(j == quantiaTrabalhos) {
				break;
			}
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




void resolveModelo(double** beneficios, int quantiaOrientadores, int quantiaTrabalhos, std::vector < Orientador >& orientadores, std::vector < Trabalho >& trabalhos, const char * saidaNome, const char* resultadoNome) {

	
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
	
		
			
		if(trabalhosInteresseOrientador.size() < 3) {
			
		for(int j = 0; j < quantiaTrabalhos; j++) {

				exp0 += beneficios[i][j] * x[i][j]; // Adição de penalidade caso ele não tenha nenhum trabalho de interesse 
			}
		}
		
		

		//Percorre o vector de trabalho de interesse do orientador i e retorna os indices armazenados	
		//Que são os trabalhos de interesse
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
	/* Alguns orientadores nao tem interesse em nenhum trabalho, então x2 sairia vazio da setença e nao pode, vamos fazer isso apenas com quem não tem interesse	*/
	for(int i = 0; i < quantiaOrientadores; i++) {

		IloExpr exp2(env);

		
		/* Retorna os trabalhos de interesse de um determinado orientador i	*/
		std::vector < int > trabalhosInteresseOrientador = orientadores[i].trabalhosInteresse;
		
		if(trabalhosInteresseOrientador.size() < 3) {

			for(int j = 0; j < quantiaTrabalhos; j++){

				exp2 += x[i][j];
			}
		}
		
		else{
			/* Pega os índices de trabalho de interesse do orientador e realiza o somatório	*/
			for(int j = 0; j < trabalhosInteresseOrientador.size(); j++) {

				int indiceTrabalhoInteresseOrientador = trabalhosInteresseOrientador[j];
				exp2 += x[i][indiceTrabalhoInteresseOrientador];
			}
		}
		Model.add(exp2 <= LMaxi);
		Model.add(exp2 >= LMini);
	}

	
	IloCplex cplex(Model);

	cplex.exportModel(saidaNome); // Exporta o modelo no formato lp

	
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
	
	int quantiaSimilaridadeMaior20 = 0;
	bool similaridadeMaior30 = false;

	int quantiaSimilaridadeMaior50 = 0;
	bool similaridadeMaior50 = false;

	
	int alocadosAoProprioTrabalho = 0;

	int quantiaSimilaridadeMenor20 = 0;
	bool similaridadeMenor30 = false;

	int orientadorNaoAlocado = 0;

	std::fstream* saidaBinario = new std::fstream("binario14.txt", std::ios::out);
	
	
	int quantiaAlocados = 0;
	for(int i = 0; i < quantiaOrientadores; i++) {
		
		int number_aloc = 0;
		for(int j = 0; j < quantiaTrabalhos; j++) {
			
			if(cplex.getValue(x[i][j]) == 1){
				*saidaBinario << j << " ";
				number_aloc++;
			}
			
		}
		if(number_aloc > 4){
			quantiaAlocados++;
		}
		*saidaBinario << "\n";

	}

	*saidaBinario << "Superaram o limite de alocacoes: " << quantiaAlocados << std::endl;
	delete saidaBinario;

	for(int j  = 0; j < quantiaTrabalhos; j++) {

		bool alocado = false;
		similaridadeMaior30 = false;
		similaridadeMaior50 = false;
		similaridadeMenor30 = false;
		
		
		for(int i = 0; i < quantiaOrientadores; i++) {

			int xValue = cplex.getValue(x[i][j]);

			if(xValue == 1) {

				alocado = true;			
				if(beneficios[i][j] >= 0.5) {
					similaridadeMaior50 = true;
				}
				else if(beneficios[i][j] >= 0.3) {
					similaridadeMaior30 = true;
				}
				else if(beneficios[i][j] == -1) {
					alocadosAoProprioTrabalho;
				}
				else {
					similaridadeMenor30 = true;
				}

			}
		}
		if(!alocado) {
			orientadorNaoAlocado++;
		}
		if(!similaridadeMaior50) {
			quantiaSimilaridadeMaior50++;
		}
		if(!similaridadeMaior30) {

			quantiaSimilaridadeMaior20++;
		}
		if(!similaridadeMenor30) {
			quantiaSimilaridadeMenor20++;
		}
	}
	

	std::fstream *resultado = new std::fstream(resultadoNome, std::ios::out);

	std::stringstream result;
	result << "Alocados a similaridade maior que 50: " << quantiaSimilaridadeMaior50 << '\n' <<
	"Alocados a similaridade maior que 30: " << quantiaSimilaridadeMaior20 << '\n' <<
	"Alocados a similaridade menor que 30: " << quantiaSimilaridadeMenor20 << '\n' << 
	"Alocados ao proprio trabalho: " << alocadosAoProprioTrabalho << '\n' << 
	"orientador nao alocado: " << orientadorNaoAlocado << '\n' <<
	"Limite Minimo: " << LMini << " " << "Limite Maximo: " << LMaxi << '\n';
	*resultado << result.str();
	resultado->close();
	delete resultado;

	env.end();
}





int main(int argc, char** argv) {
	
	/* O primeiro argumento é a instancia, segundo o nome do arquivo em formato lp e o terceiro a saida do resultado*/
	//
	if(argc <  4) {

		std::cout << "Digite mais argumentos" << '\n';
		exit(1);
	}

	int quantiaOrientadores = 0;
	int quantiaTrabalhos = 0;

	
	double** beneficios = matrizBeneficios(argv[1], quantiaOrientadores, quantiaTrabalhos);

	/* Inicializando vetor de orientadores	*/
	std::vector < Orientador > orientadores;
	std::vector < int > trabalhosInteresse;
	
	/* Debugado (v)
	std::cout << "QuantiaOrientadores: " << quantiaOrientadores << std::endl;
	std::cout << "QuantiaTrabalhos: " << quantiaTrabalhos << std::endl;
	
	for(int i = 0; i < quantiaOrientadores; i++) {

		for(int j = 0; j < quantiaTrabalhos; j++) {

			std::cout << beneficios[i][j] << " ";
		}
		getchar();
	}
	*/

	/* Criação da matriz de trabalhos percentes a área de interesse de um professor/orientador i	*/

	
	/* Devemos avaliar o menor valor do beneficio para que o trabalho seja considerado de interesse do orientador, 0.1 indica que são pelo menos da mesma área e subárea*/
	/* Se aumentarmos o limite do beneficio para ser trabalho de interesse, resolvemos o problema	*/
	for(int i = 0; i < quantiaOrientadores; i++) {

		Orientador orientador; // Instancia de um orientador
		for(int j = 0; j < quantiaTrabalhos; j++) {

			/* Adiciona os trabalhos de interesse do avaliador i ao vector trabalhosDeInteresse	*/ 	
			if(beneficios[i][j] >=10) {

				/* Insere o índice do trabalho que é da área de interesse do professor i	*/
				trabalhosInteresse.push_back(j);
			}
		}
		/* Adiciona os trabalhos de interesse do orientador i ao seus dados na struct	*/
		orientador.trabalhosInteresse = trabalhosInteresse;

		orientadores.push_back(orientador); // Adiciona o orientador

		trabalhosInteresse.clear(); // Limpa o vector
	}
	
	int nao_interesse = 0; // Indica a quantia de orientadores que não possuem interesse em trabalhos
	/* Debugado (v)	*/		
	for(int i = 0; i < orientadores.size(); i++) {
			
		/*
		if(orientadores[i].trabalhosInteresse.size() >= 1) {
			//std::cout << "indice: " << i << std::endl;
			//std::cout << "tam: " << orientadores[i].trabalhosInteresse.size() << std::endl;	
			for(int j = 0; j < orientadores[i].trabalhosInteresse.size(); j++) {

				std::cout << orientadores[i].trabalhosInteresse[j] << " ";
			}
			std::cout << std::endl;
		}
		*/
		if(!orientadores[i].trabalhosInteresse.size()){

			nao_interesse++;
		}
	}
	
	std::cout << "Orientadores não interessados: " << nao_interesse << std::endl;
	
	/* Inicializando vector de trabalhos e seus dados	*/
	std::vector < Trabalho > trabalhos;
	std::vector < int > orientadoresAptos;

	for(int j = 0; j < quantiaTrabalhos; j++) {

		Trabalho trabalho; // Inicializa um trabalho
		for(int i = 0; i < quantiaOrientadores; i++) {
			
			/* Se o beneficio é diferente de zero, é porque o orientador está apto para avaliar aquele projeto */
			if(beneficios[i][j] != -1) {
				orientadoresAptos.push_back(i);
			}
		}
		trabalho.orientadoresAptos = orientadoresAptos;
		trabalhos.push_back(trabalho);
		orientadoresAptos.clear();
	}

	
	resolveModelo(beneficios, quantiaOrientadores, quantiaTrabalhos, orientadores, trabalhos, argv[2], argv[3]);
	


	
	
	for(int i = 0; i < quantiaOrientadores; i++) {

		delete beneficios[i];
	}

	delete beneficios;

	return 0;
}
