# Data_Extract_Python

<h2> PT/BR  </h2>
<h2>Apresentação  :speech_balloon:	</h2> 
Aplicação em Python para consumir e salvar no banco de dados, informações dos produtos de notas fiscais de consumo, direto de um arquivo estático HTML, 
com layout pré definido.

<h2>Cenário Motivador </h2> 
A utilização de XML seria a opção mais simples e comum, devida a sua estruturação simples, porém as notas de consumos, que são as que recebemos após uma compra 
comum, exige um certificado digital para que o consumidor tenha acesso ao arquivo integral, com todas as informações, sendo possível acessar as informações
atráves do navegador pelo site </br> (http://nfe.sefaz.ba.gov.br/servicos/nfce/Modulos/Geral/NFCEC_consulta_chave_acesso.aspx) com a <strong>chave de acesso.</strong>

<IMAGEM>



<h2>Ideias de utilização dos dados </h2>
:rocket: <strong> Prever comportamento de consumo </strong> </br>
:rocket: <strong> Estimar gastos passados e futuros </strong> </br>
:rocket: <strong> Melhorar a personalização de demanda de acordo com o perfil de compra </strong> </br>
:rocket:<strong> Direcionar campanhas por perfil de consumo </strong> </br>
:rocket: <strong> Etc...</strong> 

<h2>Instruções de Uso :blue_book:	</h2>

:white_check_mark: 1 - Execução da criação das tabelas (Create_table.sql) </br> 
:white_check_mark: 2 - Execução da rotina das procedures(create_procedure.sql) </br>
:white_check_mark: 3 - Em anexo dois arquivos de exemplos compactados, para ser usado no python. (arquivos_html.rar) </br>
:white_check_mark: 4 - Executar o arquivo (data_extract_from_html.py) no VSCode ou outro compilador desejado.

Execução: 



<h2>Observações</h2>
A abstração do banco de dados se encontra na tabela <strong>Models</strong>, onde as tabelas a serem replicadas para o banco destino se encontram lá, em anexo também está um script 
adicional para reprodução do banco completo, com <strong>triggers e procedures </strong>

<h2>Sobre a Tecnologia usada</h2>
:white_check_mark: <strong>Linguagem de Programação: Python </strong> </br>
:white_check_mark: <strong>Banco de Dados:  SQL Server </strong> </br>

<h2> EN </h2>



<h2> Desenvolvedor :technologist:</h2>
Elto Cunha </br>
Linkedin: (https://www.linkedin.com/in/eltonbrcunha/)
