import time
from threading import Thread

import pandas as pd
import versionamento

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from versionamento import Versionamento

#Encontrar como fazer o Webscrapping da tabela do Hub

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")
#Change chrome driver path accordingly
#Executar no CMD: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9111 --user-data-dir="C:\selenum\ChromeProfile"
chrome_driver = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options)
##print(driver.title)
##print(driver.session_id)
driver.get("https://partnerhub.stone.com.br/#/integration")
time.sleep(3)

xpath_setup = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[1]/ul[2]/li/a/span")
xpath_setup.click()

status_versao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/div[2]/select")
status_versao.click()

validacao_integracao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/div[2]/select/option[2]")
validacao_integracao.click()

time.sleep(3)
botao_buscar = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[2]/button[1]")
botao_buscar.click()
time.sleep(3)
#tabela = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table").get_attribute('outerHTML')
tabela = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table")
linhas = tabela.find_elements(By.TAG_NAME,"tr")
print(tabela.text)

lista_versionamentos = []
'''dados = []
for linha in linhas:
    celulas = linha.find_elements(By.TAG_NAME, "td")
    dados.append([celula.text] for celula in celulas)'''

print("Imprimindo linha a linha")
for linha in linhas[1:]:
    #print(linha.text)
    texto_linha = linha.text
    lista_colunas = texto_linha.split('\n')
    #print(lista_colunas)
    print(lista_colunas[2], lista_colunas[4], lista_colunas[9])
    versionamento = Versionamento(lista_colunas[2], lista_colunas[4], lista_colunas[9])
    lista_versionamentos.append(versionamento)


print(lista_versionamentos[0])


'''
Extraí diretamente da página já carregada via xpath e estou convertendo os dados via Pandas
Entender como pegar linha a linha
Split dos valores por /n
Salvar no objeto versionamento
'''

