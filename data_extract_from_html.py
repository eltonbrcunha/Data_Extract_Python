from tkinter import Tk
from tkinter.filedialog import askopenfilename
import codecs
from bs4 import BeautifulSoup
import re
import pyodbc as con

# Conexão Banco de Dados
string_conexao = ('''DRIVER={SQL Server}; Server=127.0.0.1; UID=sa; PWD=********; DataBase=DB_MELHOR_COMPRA''')
conexao = con.connect(string_conexao)

# Criando o cursor da conexão.
cursor = conexao.cursor()


# Habilitando selecionar arquivo.
open_window = Tk().withdraw()
caminho_do_arquivo = askopenfilename(filetypes = (("Arquivos de texto", "*.html"), ("Arquivos csv", "*.csv")))

if caminho_do_arquivo:
    with open(caminho_do_arquivo, encoding='utf-8') as arquivo:

# Composição do Arquivo HTML
        try:
            HTMLFile = codecs.open(caminho_do_arquivo, encoding='utf-8')
            site  = BeautifulSoup(HTMLFile, 'html.parser')
        
# Nós Filhos
            attr = site.html
        finally:
            print('Processando')
else:
    print('Selecione um arquivo')





def LimparCamposNumerico(campo):
    campo_formatado = re.sub('[^0-9,,]', '', campo)
    return campo_formatado

def LimparCampoCNPJ(campo):
    campo_formatado = re.sub('[^0-9,.,-,/,-]', '', campo)
    return campo_formatado


# Pega um Elemento Específico
#  for tag in attr.find_all('tr',id='Item + 1'):

# Pega todos os elementos Começando pelo nome do Atributo da Tag THML
#for tag in attr.select('tr[id*= "Item + "]'):

# Método Inserir a Chave no Banco de Dados
def Insert_Nota(chave_nota):
    
    # Criando o cursor da conexão
    cursor_chave_nota = conexao.cursor()
    comando_procedure_nota = f"""EXEC PRC_INSERIR_HISTORICO_NOTA '{chave_nota}','Inserção Automática', 0"""
    try:
        cursor_chave_nota.execute(comando_procedure_nota)
        row_nota = cursor_chave_nota.fetchone()
        token_nota = row_nota[0]
        cursor_chave_nota.commit()
        return token_nota
    except con.Error:
        print('Erro ao inserir Nota.')   
    finally:
        cursor_chave_nota.close()


# Método Inserir Fornecedor
def InsertFornecedor(nome_fornecedor,cnpj_fornecedor):
    
    # Criando o cursor da conexão do Fornecedor
    cursor_fornecedor = conexao.cursor()
    comando_procedure_fornecedor =f"""
    EXEC PRC_INSERIRFORNECEDOR '{nome_fornecedor}', '{cnpj_fornecedor}', 0
    """
    try:
        cursor_fornecedor.execute(comando_procedure_fornecedor)
        row = cursor_fornecedor.fetchone()
        token_fornecedor =row[0]
        cursor_fornecedor.commit()
        return token_fornecedor
    except con.Error:
        print('Erro ao cadastrar o Fornecedor.')
    finally:
        cursor_fornecedor.close()


# Dados da Chave de Acesso
chave_de_acesso = attr.find('span', class_= 'chave')

# Inserindo a Nota
id_chave_acesso = Insert_Nota(chave_de_acesso.get_text().replace(' ',''))

# Dados do Fornecedor
nome_fornecedor = attr.find('div',class_= 'txtTopo')
cnpj_fornecedor = attr.find('div', class_='text')

# Inserindo o Fornecedor
id_fornecedor = InsertFornecedor(nome_fornecedor.get_text(),str(LimparCamposNumerico(cnpj_fornecedor.get_text())))


# Método Inserir Produto
def InseriProduto(codigo_produto, nome_produto, token_fornecedor ):

    # Criando o cursor da conexão dos Produtos
    cursor_produto_fornecedor = conexao.cursor()
    comando_prc_produto_fornecedor = f"""
    EXEC PRC_INSERIR_PRODUTO '{codigo_produto}', '{nome_produto}', '{token_fornecedor}', 0
    """
    try:
        cursor_produto_fornecedor.execute(comando_prc_produto_fornecedor)
        row = cursor_produto_fornecedor.fetchone()
        token_produto_fornecedor = row[0]
        cursor_produto_fornecedor.commit()
        return token_produto_fornecedor
    except con.Error:
        print('Erro ao lançar o produto.')
    finally:
        cursor_produto_fornecedor.close()

# Método Inserir Itens Nota
def InserirItemNota(token_fornecedor, codigo_produto, vl_unitario, quantidade_produto, vl_total_item, id_chave_de_acesso):

    # Criando o cursor da conexão dos items da nota fiscal
    cursor_item_nota = conexao.cursor()
    comando_prc_item_nota =  f"""
    EXEC PRC_ITEM_NOTA_FISCAL '{token_fornecedor}', '{codigo_produto}' ,'{vl_unitario}', '{quantidade_produto}'
    ,'{vl_total_item}', '{id_chave_de_acesso}', '0'"""
    try:

        cursor_item_nota.execute(comando_prc_item_nota)
        # row = cursor_item_nota.fetchone()
        # token_item_nota = row[0]
        cursor_item_nota.commit()
        # return token_item_nota
    except con.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate) 
    finally:
        cursor_item_nota.close()

# Dados dos Produtos
for tag in attr.select('tr[id*= "Item + "]'): 
    item = tag.find('span', class_='txtTit')
    codigo_produto = tag.find('span', class_= 'RCod')
    quantidade_produto = tag.find('span', class_= 'Rqtd')
    valor_unitario_produto = tag.find('span',class_= 'RvlUnit')
    valor_total_produto = tag.find('td',class_= 'txtTit noWrap')  


    # Inserindo os Produtos no Banco
    id_produto = InseriProduto(LimparCamposNumerico(codigo_produto.get_text()), item.get_text(),id_fornecedor)
    InserirItemNota( id_fornecedor
                    ,int(id_produto)
                    ,LimparCamposNumerico(valor_unitario_produto.get_text()).replace(',','.')
                    ,LimparCamposNumerico(quantidade_produto.get_text()).replace(',','.')
                    ,LimparCamposNumerico(valor_total_produto.get_text()).replace(',','.')
                    ,id_chave_acesso)
   

   
    print(' ')
    print('Item Inserido')
    print(' ')
    print('Produto: ', item.get_text())
    print('Código: ',LimparCamposNumerico(codigo_produto.get_text()))
    print('Quantidade: ' ,LimparCamposNumerico(quantidade_produto.get_text()))
    print('Valor Unitário: ',LimparCamposNumerico(valor_unitario_produto.get_text()))
    print('Valor Total Item: ',LimparCamposNumerico(valor_total_produto.get_text()))
