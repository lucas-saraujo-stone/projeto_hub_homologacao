import time
from threading import Thread

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from versionamento import Versionamento

#Padronizar a pasta de downloads e entender porque o debuggerAddress não funciona corretamente em conjunto

chrome_options = Options()
'''chrome_options.debugger_address = "127.0.0.1:9111"
chrome_prefs = {
    "download.default_directory": "C:\Downloads",  # Altere para a pasta desejada
    "download.prompt_for_download": False,  # Desativa o pop-up de confirmação
    "download.directory_upgrade": True,    # Permite atualização de diretório
    "safebrowsing.enabled": True,           # Evita bloqueios do Chrome para downloads
}
chrome_options.add_experimental_option("prefs", chrome_prefs)'''
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9111")
#Change chrome driver path accordingly
#Executar no CMD: "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9111 --user-data-dir="C:\selenum\ChromeProfile"
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
    location = linha.location
    size = linha.size
    print(location)
    print(size)
    produto = lista_colunas[0]
    tipo = lista_colunas[1]
    if produto == "SDK Android" and tipo == "Versionamento":
        nome_aplicacao = lista_colunas[2]
        parceiro = lista_colunas[4]
        status = lista_colunas[9]
        eixo_x = location['x'] + size['width'] / 2  # Centro do elemento no eixo X
        eixo_y = location['y'] + size['height'] / 2  # Centro do elemento no eixo Y
        actions = ActionChains(driver)
        actions.move_by_offset(eixo_x, eixo_y).click().perform()

        versionamento = Versionamento(nome_aplicacao, parceiro, status)
        lista_versionamentos.append(versionamento)

        botao_app_download = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table/tbody[1]/tr[2]/td/app-application-approval-detailed-information/div/div[2]/div/div/div/div[2]/div[1]/div[4]/button/i")
        botao_app_download.click()

#print(lista_versionamentos[0].__str__())

for versionamento in lista_versionamentos:
    ##label_nome_aplicacao = driver.find_element(By.XPATH, ".//span[text()='" + versionamento.nome_aplicacao

    ##       + "']")
    print(lista_versionamentos.index(versionamento))

    #XPATH fixo até o momento
    label_nome_aplicacao = driver.find_element(By.XPATH, "/html/body/app-root/app-base-layout/div/app-application-approvals/div/div/div[2]/div[4]/app-application-approvals-grid/div/div[3]/table/tbody[1]/tr/td[3]/div/span")

    label_nome_aplicacao.click()

print("Fim")

#https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test
#https://googlechromelabs.github.io/chrome-for-testing/#stable
#https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
#https://cosmocode.io/how-to-connect-selenium-to-an-existing-browser-that-was-opened-manually/

