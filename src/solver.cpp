#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include "ilcplex/ilocplex.h"
#include <chrono>
#include <sstream>
#include <algorithm>
#include <cmath>

#define NA 2 // Numero maximo de avaliadores por trabalho

//#define LMini  0 // Limite minimo de trabalhos por professor i
//#define LMaxi  2 // Limite maximo de trabalhos por professor i

int LMini, LMaxi = 0;


/* O modelo abaixo tenta achar a maior paridade entre a alocação do Enic original e essa alocação 
 * Porém pode ocorrer no enic um orientador ser alocado a um trabalho que ele possua zero afinidade
 * Então ele não será alocado resultando em uma diminuição da paridade */
typedef struct {
	std::vector < int > trabalhosInteresse; // Trabalhos de interesse de um determinado orientador
} Orientador;


typedef struct {
	std::vector < int > orientadoresAptos; // Vector de orientadores que podem avaliar determinado trabalho
}Trabalho;


int **lerVariavelAuxiliar(const std::string& caminho, int quantiaOrientadores, int quantiaTrabalhos){
		

	/* Criação da variável auxiliar w, inicializa inicialmente todas com zero	*/
	int **w = new int*[quantiaOrientadores];

	for(int i = 0; i < quantiaOrientadores; i++){

		for(int j = 0; j < quantiaTrabalhos; j++){

			w[i] = new int[quantiaTrabalhos];
			w[i][j] = 0;
		}
	}
	

	std::fstream* ptrArquivo = new std::fstream(caminho, std::ios::in); // Abre o arquivo para entrada de dados
	std::string linha; // linha para ler o arquivo
	std::string palavra;

	int indiceOrientador = 0;
	
	std::vector < int > valoresLinha;
	valoresLinha.clear();

	while(1){
		std::getline(*ptrArquivo, linha);
		
		if(ptrArquivo->eof())
			break;
		if(linha == "\n"){
			continue;
		}
		std::stringstream dados(linha); // Criacao de uma sstream

		// Separa os dados da string de stream pelo espaço e então armazena no vector de valores
		while(std::getline(dados, palavra, ' ')) {

			std::string::size_type sz;
			if(palavra.size() >  0) {
				valoresLinha.push_back(std::stoi(palavra, &sz));
			}
			
			
			
		}
		
		// EStamos na linha que indica o minimo e maximo
		if(indiceOrientador == quantiaOrientadores){
			LMini = valoresLinha[0];
			LMaxi = valoresLinha[1];
			std::cout << "Valor Minimo de trabalhos por orientador: " << LMini << std::endl;
			std::cout << "Valor Maximo de trabalhos por orientador: " << LMaxi << std::endl;
			break;
		}
		/* Os valores em valoresLinha representa os trabalhos que o orientador i foram alocados
		 * Como cada linha representa um orientador, vamos acessar o indice do trabalho
		 * e então dar 1 para a variável*/
		for(int i = 0; i < valoresLinha.size(); i++){
			int indiceTrabalho = valoresLinha[i];
			w[indiceOrientador][indiceTrabalho] = 1;
			
		}

		indiceOrientador++;
		valoresLinha.clear();
		palavra.clear();
		linha.clear();


	}
	
	return w;

}
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

			std::string::size_type sz;
			if(palavra.size() >  0) {
				valoresLinha.push_back(std::stoi(palavra, &sz));
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




void resolveModelo(int** beneficios, int** w, int quantiaOrientadores, int quantiaTrabalhos, std::vector < Orientador >& orientadores, std::vector < Trabalho >& trabalhos, const char * saidaNome, const char* resultadoNome) {

	
	auto start = std::chrono::high_resolution_clock::now(); // Pega o tempo do relogio

	
	IloEnv env; // Cria o ambiente de modelagem

	/* Criação do modelo, responsável por função objetivo e restrições	*/
	/* Precisa de um ambiente de modelagem para ser iniciado	*/
	IloModel Model(env);


	/* Criação da variavel de decisão	*/
	// Devemos enviar os parametros de ambiente  e quantia de linha inicial


	IloArray < IloNumVarArray > x(env, quantiaOrientadores);

	// Acessamos cada valor dessa linha inicial, e iniciamos um array com o ambiente, tamanho, indice incial e assim	
	for(int i = 0; i < quantiaOrientadores; i++) {
		x[i] = IloNumVarArray(env, quantiaTrabalhos, 0, 1, ILOINT);
	}
	
	// Adicionando nome das variaveis	
	char var[100];

	for(int i = 0; i < quantiaOrientadores; i++) {
		for(int j = 0; j < quantiaTrabalhos; j++) {
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
	
		//Percorre o vector de trabalho de interesse do orientador i e retorna os indices armazenados	
		//Que são os trabalhos de interesse
		for(int j = 0; j < trabalhosInteresseOrientador.size(); j++) {
			
			int trabalhoIndice = trabalhosInteresseOrientador[j];

			exp0 += beneficios[i][trabalhoIndice] * x[i][trabalhoIndice];
		}
		
		
		trabalhosInteresseOrientador.clear();
	}
	Model.add(IloMaximize(env,exp0)); // Adiciona ao modelo para maximizar a função
	

	/* Restrições do problema 	*/

	
	/* Mantém fixo o valor de j e varia os valores de i	*/
	/* Como x[i][j] é uma variável binária que indica se o professor i foi alocado ao trabalho j ou não	*/
	/* Mantém fixo um determinado trabalho j e verifica se a soma dos professores que irão avaliar aquele trabalho	*/
	/* é igual ao número de avaliadores por trabalho	*/
	
	for(int j = 0; j < quantiaTrabalhos; j++) {
		IloExpr exp1(env); // Inicializa uma expressão
		//Retorna o vector contendo os indices dos orientadores aptos a avaliares o trabalho j	
		std::vector < int > orientadoresAptos = trabalhos[j].orientadoresAptos;
		
		// Percorre o vector e armazena os índices dos orientadores aptos e realiza o somatório 
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
		
		for(int j = 0; j < quantiaTrabalhos; j++){
			// Se ele não for um trabalho de interesse a gente pula
			if(find(trabalhosInteresseOrientador.begin(), trabalhosInteresseOrientador.end(), j) == trabalhosInteresseOrientador.end())
				continue;
			exp2 += x[i][j];
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

	std::cout << "Duracao(s): " << elapsed.count() / 1000 << '\n';
	std::cout << "O valor da função objetivo eh: " << obj << std::endl;
	
	
	/* Gera o arquivo binario para leitura	*/
	std::fstream* saidaBinario = new std::fstream("../results22/comparativo.txt", std::ios::out);
  std::fstream* outputModel = new std::fstream("../results22/outputModel.txt", std::ios::out);
  

	std::vector <int> porcentagemComparativa;
	int quantia_total_iguais = 0; // Quantia que representa que houve 100% de igualdade
	int pelo_menos_unico_igual = 0;
	int quantia_total_diferentes = 0;

	for(int i = 0; i < quantiaOrientadores; i++) {
		
		std::vector <int> trabalhosIguais;;

		*saidaBinario << i << " ";
		
		
		for(int j = 0; j < quantiaTrabalhos; j++) {
			
			if(cplex.getValue(x[i][j]) == 1 and cplex.getValue(x[i][j]) == w[i][j]){
				trabalhosIguais.push_back(j);
			}
			
		}
		
	
		int quantia_trabalhos_alocados_enic = 0; // Variavel que indica a quantia de trabalhos que o orientador i foi alocado no enic

		for(int l = 0; l < quantiaTrabalhos; l++){
			if(w[i][l] == 1){
				quantia_trabalhos_alocados_enic += 1;
			}
		}
		
		int porcentagem = -1; // -1 indica que ambos nao foram alocados a nenhum trabalho

		/* Para realizar a leitura do comparativo	*;
		 * Se em ambos tanto no enic como nesse modelo, não foram alocados trabalhos
		 * está escrito como -1
		 * caso não foi alocado no enic mas aqui, estará como -2
		 * caso contrario será a porcentagem seguido pelos trabalhos iguais	*/
		
		if(quantia_trabalhos_alocados_enic != 0){
			porcentagem = (trabalhosIguais.size() / (float)quantia_trabalhos_alocados_enic) * 100;
			
			porcentagemComparativa.push_back(porcentagem);
			if(porcentagem == 100){
				quantia_total_iguais += 1;
			}
			else if(porcentagem != 0){
				pelo_menos_unico_igual += 1;
				std::cout << "O orientador  " << i << " nao foi alocado a todos os trabalhos" << std::endl;
				//getchar();
			}
			else{
				quantia_total_diferentes += 1;
			}
			*saidaBinario << porcentagem << " ";
		}else{
			
			if(trabalhosIguais.size() == 0){
				*saidaBinario << "-1" << " ";

			}
			else{
				*saidaBinario << "-2" << " ";
			}
		}
		
		for(int k = 0; k < trabalhosIguais.size(); k++){
			*saidaBinario << trabalhosIguais[k] << " ";
		}
		
		*saidaBinario << "\n";

	}
	
  for(int j = 0; j < quantiaTrabalhos; j++){

    for(int i = 0; i < quantiaOrientadores; i++){
      
      if(cplex.getValue(x[i][j]) == 1){
        *outputModel << i << " ";
      }
    }
    *outputModel << "\n";
  }

	std::cout << "Quantia de Orientadores: " << quantiaOrientadores << std::endl;
	std::cout << "Houveram trabalhos alocados iguais: " << quantia_total_iguais << std::endl;
	std::cout << "Houverem pelo menos 1 trabalho igual: " << pelo_menos_unico_igual << std::endl;
	std::cout << "Porcentagem de igualdade: " << ((quantia_total_iguais * 1.0 / quantiaOrientadores) * 100.0) << std::endl; 
	std::cout << "Quantia de orientadores alocados a diferentes trabalhos: " << quantia_total_diferentes << std::endl;
	*saidaBinario << *min_element(porcentagemComparativa.begin(), porcentagemComparativa.end()) << " "
			<< *max_element(porcentagemComparativa.begin(), porcentagemComparativa.end()) << "\n";
	delete saidaBinario;
  delete outputModel;

	env.end();
}





int main(int argc, char** argv) {
	
	/* O primeiro argumento é a instancia, segundo o nome do arquivo em formato lp e o terceiro a saida do resultado*/
	if(argc <  4) {

		std::cout << "Digite os argumentos na ordem: instancia.txt variavel.txt modelo.lp" << '\n';
		exit(1);
	}

	int quantiaOrientadores = 0;
	int quantiaTrabalhos = 0;

	
	int** beneficios = matrizBeneficios(argv[1], quantiaOrientadores, quantiaTrabalhos);
	int** w = lerVariavelAuxiliar(argv[2], quantiaOrientadores, quantiaTrabalhos);
	
	

	std::cout << "QuantiaOrientadores: " << quantiaOrientadores << std::endl;
	std::cout << "QuantiaTrabalhos: " << quantiaTrabalhos << std::endl;

	/* Inicializando vetor de orientadores	*/
	std::vector < Orientador > orientadores;
	std::vector < int > trabalhosInteresse;
	



	/* A ideia é aumentar o beneficio se w[i][j] == 1, multiplica em 1000x */

	for(int i = 0; i < quantiaOrientadores; i++){
		
		for(int j = 0; j < quantiaTrabalhos; j++){
				
			if(w[i][j]){
				
				beneficios[i][j] *= 1000000;
			}
		}
	}

	/* Criação da matriz de trabalhos percentes a área de interesse de um professor/orientador i	*/

	/* Como a afinidade de um orientador é 10 caso
	 * ele tenha a mesma area que o trabalho, então
	 * consideramos qualquer beneficio acima ou igual disso
	 * como um trabalho de interesse	*/
	for(int i = 0; i < quantiaOrientadores; i++) {

		Orientador orientador; // Instancia de um orientador
		for(int j = 0; j < quantiaTrabalhos; j++) {

			/* Adiciona os trabalhos de interesse do avaliador i ao vector trabalhosDeInteresse	*/ 	
			if(beneficios[i][j] >= 1) {

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
	for(int i = 0; i < quantiaOrientadores; i++) {
			
		if(orientadores[i].trabalhosInteresse.size() == 0){

			nao_interesse++;
		}
	}
	
	trabalhosInteresse.clear(); // Limpeza do vetor

	/* Como temos orientadores sem interesse de trabalho, vamos
	 * fazer ele ter interesse em todos os trabalhos
	 * que não são o dele*/
	for(int i = 0; i < quantiaOrientadores; i++){

		if(orientadores[i].trabalhosInteresse.size() == 0){
			for(int j = 0; j < quantiaTrabalhos; j++){
				
				if(beneficios[i][j] != -1){
					trabalhosInteresse.push_back(j);
				}
			}
			orientadores[i].trabalhosInteresse = trabalhosInteresse;

			trabalhosInteresse.clear();
		}
	}

	std::cout << "Orientadores não interessados: " << nao_interesse << std::endl;
	
	/* Inicializando vector de trabalhos e seus dados	*/
	std::vector < Trabalho > trabalhos;
	std::vector < int > orientadoresAptos;

	for(int j = 0; j < quantiaTrabalhos; j++) {

		Trabalho trabalho; // Inicializa um trabalho
		for(int i = 0; i < quantiaOrientadores; i++) {
			
			/* Se o beneficio é diferente de -1, é porque o orientador está apto para avaliar aquele projeto */
			if(beneficios[i][j] != -1) {
				orientadoresAptos.push_back(i);
			}
		}
		trabalho.orientadoresAptos = orientadoresAptos;
		trabalhos.push_back(trabalho);
		orientadoresAptos.clear();
	}

	
	resolveModelo(beneficios, w, quantiaOrientadores, quantiaTrabalhos, orientadores, trabalhos, argv[3], argv[4]);	
	for(int i = 0; i < quantiaOrientadores; i++) {

		delete beneficios[i];
	}

	delete beneficios;

	return 0;
}
