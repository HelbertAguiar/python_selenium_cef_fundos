from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time , sys

def inicia_driver( website , temp ):

    try:
        options = Options()
        options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
        browser = webdriver.Firefox( options = options, executable_path = "geckodriver.exe" )
    except:
        sys.exit("Falha no carregamento do driver ou localizacao do path firefox")
    
    browser.implicitly_wait(temp)
    browser.get(website)
    
    if browser.title == '502 Bad Gateway':
        browser.quit()
        sys.exit("Falha no carregamento da pagina, error: 502 BAD GATEWAY")
        
    return browser 

def print_table( table , dataInserir):
    
    tags_tr = table.findChildren("tr", recursive=False)

    for tr in tags_tr:
        nome_fundo = (tr.td.a.text).strip().upper().replace('Õ', 'O').replace('Ç','C').replace('Á','A').replace('É','E').replace('Ã','A')
        nome_fundo = nome_fundo.encode("ascii", errors="ignore").decode()
        taxa_adm = tr.findAll('td')[4].text

        try:
            perfil = tr.find(text='Risco:').findNext('td').text
        except:
            perfil = 'Unknown'
        
        cota = tr.findChildren("td", recursive=False)[3].text.strip()
        patrimonio = tr.findChildren("td", recursive=False)[8].text.strip()

        print('{}{}{}{}{}{}'.format( dataInserir.ljust(12, ' '), nome_fundo.ljust(45, ' ') , taxa_adm.ljust(10, ' '), \
                                    perfil.ljust(15, ' ') , cota.rjust(15, ' ') , patrimonio.rjust(15, ' ') ) )

def print_table_csv( table , dataInserir):
    
    tags_tr = table.findChildren("tr", recursive=False)

    for tr in tags_tr:
        nome_fundo = (tr.td.a.text).strip().upper().replace('Õ', 'O').replace('Ç','C').replace('Á','A').replace('É','E').replace('Ã','A')
        nome_fundo = nome_fundo.encode("ascii", errors="ignore").decode()
        taxa_adm = tr.findAll('td')[4].text

        try:
            perfil = tr.find(text='Risco:').findNext('td').text
        except:
            perfil = 'Unknown'
        
        cota = tr.findChildren("td", recursive=False)[3].text.strip()
        patrimonio = tr.findChildren("td", recursive=False)[8].text.strip()

        print('{};{};{};{};{};{}'.format( dataInserir, nome_fundo , taxa_adm, perfil , cota, patrimonio ) )

def print_linha_inicial():
    print('{}{}{}{}{}{}'.format( 'DATA'.ljust(12, ' '), 'NOME FUNDO'.ljust(45, ' ') , 'TAXA ADM'.ljust(10, ' '), \
                                    'PERFIL DE INVEST.'.ljust(15, ' ') , 'COTA'.rjust(15, ' ') , 'PATRIM.'.rjust(15, ' ') ) )

def print_linha_inicial_csv():
    print('{};{};{};{};{};{}'.format( 'DATA', 'NOME FUNDO', 'TAXA ADM', 'PERFIL DE INVEST.' , 'COTA' , 'PATRIM.' ) )

def captura_classe_fundos( browser , temp , id_classe , dataInserir):

    tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, id_classe)) )
    tab.click()
    time.sleep((2/3)*temp)
    # tab = WebDriverWait(browser, temp).until( EC.presence_of_element_located((By.ID, 'j_idt88:0:gridPesquisar')) )
    soup = BeautifulSoup(browser.page_source, "html.parser")
    table = soup.findAll("table")[2].find('tbody')
    print_table_csv(table, dataInserir)

def insere_data( browser , temp , dataInserir ):
    inputElement = browser.find_element_by_id("dtBusca")
    inputElement.click()
    time.sleep((1/5)*temp)
    inputElement.send_keys(dataInserir.replace('/',''))
    btn = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "btn-consultar")) )
    btn.click()
    time.sleep((2/3)*temp)

def seleciona_segmentacao( browser , temp , cod ):
    tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, cod)) )
    tab.click()
    time.sleep((2/3)*temp)

def leitura_arquivo_data():
    
    lista_datas = []
    with open('input_datas', 'r') as reader:
        for line in reader.readlines():
            lista_datas.append(line.split())

    return lista_datas

temp = 12 # segundos
lista_datas = leitura_arquivo_data() # dataInserir = '05/05/2021'

# instancia navegador
browser = inicia_driver('http://www.fundos.caixa.gov.br/sipii/pages/public/listar-fundos-internet.jsf', temp)
print_linha_inicial_csv()

for data in lista_datas:

    dataInserir = str(data).replace('\'', '').replace('[', '').replace(']','')

    # Inserindo data
    insere_data(browser, temp, dataInserir)
    # Seleciona todos os segmentos (PF, PJ, GOV, RPPS)
    seleciona_segmentacao(browser, temp, 'a4')
    # Captura classe de SIMPLES
    captura_classe_fundos(browser, temp, "ui-id-1", dataInserir)
    # Captura classe de RENDA FIXA
    captura_classe_fundos(browser, temp, "ui-id-2", dataInserir)
    # Captura classe de REFERENCIADO
    captura_classe_fundos(browser, temp, "ui-id-3", dataInserir)
    # Captura classe de RENDA FIXA CURTO PRAZO
    captura_classe_fundos(browser, temp, "ui-id-4", dataInserir)
    # Captura classe de MULTIMERCADO
    captura_classe_fundos(browser, temp, "ui-id-5", dataInserir)
    # Captura classe de MULTIMERCADO
    captura_classe_fundos(browser, temp, "ui-id-6", dataInserir)
    # Captura classe de AÇÕES
    captura_classe_fundos(browser, temp, "ui-id-7", dataInserir)
    # Captura classe de ETF - FUNDO DE INDICE
    captura_classe_fundos(browser, temp, "ui-id-8", dataInserir)
    # Seleciona segmentos PF para buscar aba dos FMPs
    seleciona_segmentacao(browser, temp, 'a1')
    # Captura classe de FMP - FUNDO MUTUO DE PRIVATIZACAO
    captura_classe_fundos(browser, temp, "ui-id-9", dataInserir)

browser.quit()