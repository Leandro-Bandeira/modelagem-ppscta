A função main.py cria uma matriz[orientadores][trabalhos] que indica o benefício dos orientadores em relação aos trabalhos
. Em seguida é criada uma variável que indica em quais trabalhos o orientador foi alocado no Enic. Após isso o solver
fica responsável por alocar os orientadores a relatórios de trabalhos e tenta chegar a uma paridade mais próxima de 100%
, porém isso não é possível, porque no Enic pode ocorrer de um orientador estar alocado a um trabalho que ele não possui afinidade
e seu benefício no arquivo de instância está zerado. Quando o orientador é alocado no Enic, seu benefício é multiplicado por 10000
para tentar chegar a paridade.
