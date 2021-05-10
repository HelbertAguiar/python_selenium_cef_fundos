from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def inicia_driver(time, website, ancora):
    options = Options()
    options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"
    browser = webdriver.Firefox(options=options, executable_path="geckodriver.exe")
    browser.implicitly_wait(time)
    acessa_pagina(browser, website, ancora)
    return browser

def acessa_pagina(browser, website, ancora):
    browser.get(website)

def printTable(table):
    
    # Captura primeiro
    tr = table.tr
    nome_fundo = (tr.td.a.text).strip().upper().replace('Õ', 'O').replace('Ç','C').replace('Á','A').replace('É','E').replace('Ã','A')
    nome_fundo = nome_fundo.encode("ascii", errors="ignore").decode()
    taxa_adm = tr.findAll('td')[4].text
    perfil = tr.findAll('td')[8].text
    cota = ((tr.td.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td')).text).strip()
    patrimonio = ((tr.td.find_next_sibling('td').find_next_sibling('td')\
                        .find_next_sibling('td').find_next_sibling('td')\
                        .find_next_sibling('td').find_next_sibling('td')\
                        .find_next_sibling('td').find_next_sibling('td')).text).strip()

    print('{} Taxa Adm.: {} Perfil: {} Cota: {} Patr. Liquido: {}' \
            .format(    nome_fundo.ljust(45, ' ') , taxa_adm.rjust(5, ' ') , perfil.rjust(12, ' ') ,\
                        cota.ljust(20, ' ') , patrimonio.rjust(10, ' ')))
    
    # Captura demais da lista
    for tr in table.tr.next_siblings:
        nome_fundo = (tr.td.a.text).strip().upper().replace('Õ', 'O').replace('Ç','C').replace('Á','A').replace('É','E').replace('Ã','A')
        nome_fundo = nome_fundo.encode("ascii", errors="ignore").decode()
        taxa_adm = tr.findAll('td')[4].text
        perfil = tr.findAll('td')[8].text
        cota = ((tr.td.find_next_sibling('td').find_next_sibling('td').find_next_sibling('td')).text).strip()
        patrimonio = ((tr.td.find_next_sibling('td').find_next_sibling('td')\
                            .find_next_sibling('td').find_next_sibling('td')\
                            .find_next_sibling('td').find_next_sibling('td')\
                            .find_next_sibling('td').find_next_sibling('td')).text).strip()

        print('{} Taxa Adm.: {} Perfil: {} Cota: {} Patr. Liquido: {}' \
            .format(    nome_fundo.ljust(45, ' ') , taxa_adm.rjust(5, ' ') , perfil.rjust(12, ' ') ,\
                        cota.ljust(20, ' ') , patrimonio.rjust(10, ' ')))
        
    
temp = 12
dataInserir = '05052021'
browser = inicia_driver(temp, 'http://www.fundos.caixa.gov.br/sipii/pages/public/listar-fundos-internet.jsf', 'Fundos de Investimento')

# Seleciona todos os fundos
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "a4")) )
tab.click()
time.sleep((2/3)*temp)

# Inserindo data
inputElement = browser.find_element_by_id("dtBusca")
inputElement.click()
time.sleep((1/5)*temp)
inputElement.send_keys(dataInserir)
btn = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "btn-consultar")) )
btn.click()
time.sleep((2/3)*temp)

# Captura classe de SIMPLES
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-1")) )
tab.click()
time.sleep((2/3)*temp)
# tab = WebDriverWait(browser, temp).until( EC.presence_of_element_located((By.ID, 'j_idt88:0:gridPesquisar')) )
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de RENDA FIXA
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-2")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de REFERENCIADO
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-3")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de RENDA FIXA CURTO PRAZO
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-4")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de MULTIMERCADO
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-5")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de MULTIMERCADO
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-6")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de AÇÕES
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-7")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Captura classe de ETF - FUNDO DE INDICE
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-8")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

# Seleciona todos os fundos
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "a1")) )
tab.click()
time.sleep((2/3)*temp)

# Captura classe de FMP - FUNDO MUTUO DE PRIVATIZACAO
tab = WebDriverWait(browser, temp).until( EC.element_to_be_clickable((By.ID, "ui-id-9")) )
tab.click()
time.sleep((2/3)*temp)
soup = BeautifulSoup(browser.page_source, "html.parser")
table = soup.findAll("table")[2].find('tbody')
printTable(table)

browser.quit()