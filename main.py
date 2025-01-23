import time
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from versionamento import Versionamento

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")
#Change chrome driver path accordingly
#Executar no CMD: chrome.exe --remote-debugging-port=9111 --user-data-dir="C:\selenum\ChromeProfile"
chrome_driver = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(options=chrome_options)
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

tabela = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table")
linhas = tabela.find_elements(By.TAG_NAME,"tr")
print(tabela.text)

lista_versionamentos = []

print("Imprimindo linha a linha")
for linha in linhas[1:]:
    texto_linha = linha.text
    lista_colunas = texto_linha.split('\n')
    produto = lista_colunas[0]
    tipo = lista_colunas[1]
    if produto == "SDK Android" and tipo == "Versionamento":
        nome_aplicacao = lista_colunas[2]
        parceiro = lista_colunas[4]
        status = lista_colunas[9]
        versionamento = Versionamento(nome_aplicacao, parceiro, status)
        lista_versionamentos.append(versionamento)

print(lista_versionamentos[0].__str__())
print("Fim")

#https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
#https://googlechromelabs.github.io/chrome-for-testing/#stable
#https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
#https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/

